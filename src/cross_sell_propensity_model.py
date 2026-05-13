#!/usr/bin/env python3
"""Phase 2: Train a simple model for cross-sell propensity.

Model approach:
- Mixed Naive Bayes (numeric + categorical), implemented with Python stdlib only.

Training target (proxy label):
- 1 if a client currently uses 2+ service lines (L2), else 0.

Outputs:
- outputs/ml_cross_sell_metrics.json
- outputs/ml_cross_sell_ranked_candidates.csv
- outputs/ml_cross_sell_summary.md
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Sequence, Tuple


NULL_TOKENS = {"", "null", "none", "na", "n/a"}
EPS = 1e-9


def normalize(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    if cleaned.lower() in NULL_TOKENS:
        return None
    return cleaned


def load_csv(path: Path) -> List[Dict[str, Optional[str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [{k: normalize(v) for k, v in row.items()} for row in reader]


def mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def variance(values: Sequence[float]) -> float:
    if len(values) <= 1:
        return 1.0
    m = mean(values)
    v = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return v if v > 0 else 1.0


def to_float(value: Optional[str], default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


class MixedNaiveBayes:
    def __init__(self, numeric_features: List[str], categorical_features: List[str]) -> None:
        self.numeric_features = numeric_features
        self.categorical_features = categorical_features
        self.class_priors: Dict[int, float] = {}
        self.numeric_stats: Dict[int, Dict[str, Tuple[float, float]]] = {}
        self.cat_counts: Dict[int, Dict[str, Counter]] = {}
        self.cat_vocab: Dict[str, set[str]] = {f: set() for f in categorical_features}
        self.class_counts: Counter = Counter()

    def fit(self, rows: List[Dict[str, object]], labels: List[int]) -> None:
        grouped_numeric: Dict[int, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        grouped_cat: Dict[int, Dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))

        for row, y in zip(rows, labels):
            self.class_counts[y] += 1
            for f in self.numeric_features:
                grouped_numeric[y][f].append(float(row.get(f, 0.0)))
            for f in self.categorical_features:
                val = str(row.get(f, "Unknown") or "Unknown")
                grouped_cat[y][f][val] += 1
                self.cat_vocab[f].add(val)

        total = len(labels)
        self.class_priors = {c: self.class_counts[c] / total for c in self.class_counts}

        for c in self.class_counts:
            self.numeric_stats[c] = {}
            for f in self.numeric_features:
                vals = grouped_numeric[c][f]
                self.numeric_stats[c][f] = (mean(vals), variance(vals))

        self.cat_counts = {c: grouped_cat[c] for c in self.class_counts}

    def _gaussian_logpdf(self, x: float, m: float, var: float) -> float:
        v = var if var > EPS else 1.0
        return -0.5 * math.log(2.0 * math.pi * v) - ((x - m) ** 2) / (2.0 * v)

    def predict_proba(self, row: Dict[str, object]) -> float:
        log_probs: Dict[int, float] = {}

        for c in self.class_counts:
            prior = self.class_priors.get(c, EPS)
            logp = math.log(prior if prior > EPS else EPS)

            for f in self.numeric_features:
                x = float(row.get(f, 0.0))
                m, v = self.numeric_stats[c][f]
                logp += self._gaussian_logpdf(x, m, v)

            for f in self.categorical_features:
                val = str(row.get(f, "Unknown") or "Unknown")
                counts = self.cat_counts[c][f]
                vocab_size = max(1, len(self.cat_vocab[f]))
                numerator = counts.get(val, 0) + 1
                denominator = sum(counts.values()) + vocab_size
                logp += math.log(numerator / denominator)

            log_probs[c] = logp

        max_log = max(log_probs.values())
        exp_scores = {c: math.exp(lp - max_log) for c, lp in log_probs.items()}
        denom = sum(exp_scores.values())
        if denom <= 0:
            return 0.0
        return exp_scores.get(1, 0.0) / denom


def build_features(
    clients: List[Dict[str, Optional[str]]],
    relationships: List[Dict[str, Optional[str]]],
    projects: List[Dict[str, Optional[str]]],
) -> Tuple[List[Dict[str, object]], List[int], Dict[str, int], Dict[str, Dict[str, Optional[str]]]]:
    client_lookup: Dict[str, Dict[str, Optional[str]]] = {}
    for client in clients:
        cid = (client.get("customer_id") or "").upper()
        if cid:
            client_lookup[cid] = client

    degree: Counter = Counter()
    for rel in relationships:
        c1 = (rel.get("client_1_id") or "").upper()
        c2 = (rel.get("client_2_id") or "").upper()
        if c1 and c2:
            degree[c1] += 1
            degree[c2] += 1

    projects_by_client: DefaultDict[str, List[Dict[str, Optional[str]]]] = defaultdict(list)
    services_by_client: DefaultDict[str, set[str]] = defaultdict(set)
    for p in projects:
        cid = (p.get("customer_id") or "").upper()
        if not cid:
            continue
        projects_by_client[cid].append(p)
        service = p.get("project_service_line_level_2")
        if service:
            services_by_client[cid].add(service)

    rows: List[Dict[str, object]] = []
    labels: List[int] = []
    service_count_map: Dict[str, int] = {}

    for cid, client in client_lookup.items():
        proj = projects_by_client.get(cid, [])
        active_projects = sum(1 for p in proj if (p.get("project_status") or "").lower() == "active")
        completed_projects = sum(
            1 for p in proj if (p.get("project_status") or "").lower() == "completed"
        )
        service_count = len(services_by_client.get(cid, set()))
        service_count_map[cid] = service_count

        row: Dict[str, object] = {
            "client_id": cid,
            "client_name": client.get("customer_name") or "Unknown",
            "total_projects": float(len(proj)),
            "active_projects": float(active_projects),
            "completed_projects": float(completed_projects),
            "relationship_degree": float(degree.get(cid, 0)),
            "has_parent": 1.0 if client.get("parent_customer_id") else 0.0,
            "is_active_client": 1.0 if (client.get("customer_status") or "").lower() == "active" else 0.0,
            "industry_l2": client.get("customer_industry_level_2") or "Unknown",
            "state": client.get("state_iso_code") or "Unknown",
            "employee_band": client.get("customer_employee_category") or "Unknown",
            "revenue_band": client.get("annual_revenue") or "Unknown",
        }
        rows.append(row)

        # Proxy label for training: already multi-service adopted.
        labels.append(1 if service_count >= 2 else 0)

    return rows, labels, service_count_map, client_lookup


def split_train_test(
    rows: List[Dict[str, object]], labels: List[int], test_fraction: float, seed: int
) -> Tuple[List[Dict[str, object]], List[int], List[Dict[str, object]], List[int]]:
    indices = list(range(len(rows)))
    random.Random(seed).shuffle(indices)
    cut = max(1, int(len(indices) * (1 - test_fraction)))

    train_idx = indices[:cut]
    test_idx = indices[cut:]

    if not test_idx:
        test_idx = train_idx[-1:]
        train_idx = train_idx[:-1]

    train_rows = [rows[i] for i in train_idx]
    train_labels = [labels[i] for i in train_idx]
    test_rows = [rows[i] for i in test_idx]
    test_labels = [labels[i] for i in test_idx]
    return train_rows, train_labels, test_rows, test_labels


def evaluate_binary(y_true: List[int], y_prob: List[float], threshold: float = 0.5) -> Dict[str, float]:
    y_pred = [1 if p >= threshold else 0 for p in y_prob]

    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)

    total = max(1, len(y_true))
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def write_csv(path: Path, rows: List[Dict[str, object]], headers: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def recommend_service_line(industry_l2: str, active_projects: int) -> str:
    industry_map = {
        "Health Care": "Tax",
        "Financial Services and Real Estate": "Digital",
        "Industrials": "Assurance",
        "Public Sector": "Digital",
        "Service Industries": "Tax",
        "Other Industries": "Digital",
    }
    if active_projects == 0:
        return "Assurance"
    return industry_map.get(industry_l2, "Tax")


def estimate_value(score: float, active_projects: int, degree: int) -> int:
    base = 100000
    if score >= 0.9:
        base = 220000
    elif score >= 0.7:
        base = 190000
    elif score >= 0.4:
        base = 160000
    elif score >= 0.2:
        base = 140000
    if active_projects >= 2:
        base += 10000
    if degree >= 3:
        base += 10000
    return base


def risk_level(score: float, active_projects: int) -> str:
    if active_projects == 0 and score < 0.3:
        return "High"
    if score < 0.15:
        return "High"
    if score < 0.6:
        return "Medium"
    return "Low"


def next_action_text(score: float) -> str:
    if score >= 0.7:
        return "Schedule executive discovery and confirm scope"
    if score >= 0.25:
        return "Run qualification call and validate stakeholder map"
    return "Re-open relationship and run qualification call"


def blocker_text(score: float, active_projects: int) -> str:
    if active_projects == 0:
        return "No active engagement in current cycle"
    if score < 0.15:
        return "Low signal confidence, requires sponsor validation"
    return ""


def build_pursuit_rows(
    candidate_rows: List[Dict[str, object]],
    client_lookup: Dict[str, Dict[str, Optional[str]]],
    pursuit_top_n: int,
) -> List[Dict[str, object]]:
    now = datetime.now(timezone.utc)
    last_updated = now.isoformat(timespec="seconds").replace("+00:00", "Z")
    due_date = (now + timedelta(days=7)).date().isoformat()

    pursuit_rows: List[Dict[str, object]] = []
    for i, row in enumerate(candidate_rows[:pursuit_top_n], start=1):
        cid = str(row["client_id"])
        client = client_lookup.get(cid, {})
        score = float(row["cross_sell_propensity_score"])
        active_projects = int(row["active_projects"])
        degree = int(row["relationship_degree"])
        industry = str(row["industry_l2"])

        lead_name = client.get("customer_leader_name") or "Unassigned"
        parent_id = client.get("parent_customer_id") or cid
        service_line = recommend_service_line(industry, active_projects)

        pursuit_rows.append(
            {
                "pursuit_id": f"ML-{i:03d}",
                "parent_account_id": parent_id,
                "entity_client_id": cid,
                "entity_client_name": row["client_name"],
                "relationship_lead": "Jordan Patel",
                "service_line": service_line,
                "opportunity_name": (
                    f"{service_line} cross-sell opportunity from ML propensity score ({score})"
                ),
                "stage": "Prioritized",
                "estimated_value": estimate_value(score, active_projects, degree),
                "probability_pct": round(score * 100, 2),
                "risk_level": risk_level(score, active_projects),
                "blocker": blocker_text(score, active_projects),
                "next_action": next_action_text(score),
                "next_action_owner": lead_name,
                "next_action_due_date": due_date,
                "last_updated_utc": last_updated,
            }
        )

    return pursuit_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a simple cross-sell propensity model")
    parser.add_argument("--client-csv", default="data/client.csv")
    parser.add_argument("--relationship-csv", default="data/relationship.csv")
    parser.add_argument("--projects-csv", default="data/projects.csv")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument("--pursuit-top-n", type=int, default=10)
    parser.add_argument("--test-fraction", type=float, default=0.25)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    clients = load_csv(Path(args.client_csv))
    relationships = load_csv(Path(args.relationship_csv))
    projects = load_csv(Path(args.projects_csv))

    rows, labels, service_count_map, client_lookup = build_features(clients, relationships, projects)

    numeric_features = [
        "total_projects",
        "active_projects",
        "completed_projects",
        "relationship_degree",
        "has_parent",
        "is_active_client",
    ]
    categorical_features = ["industry_l2", "state", "employee_band", "revenue_band"]

    train_rows, train_labels, test_rows, test_labels = split_train_test(
        rows, labels, test_fraction=args.test_fraction, seed=args.seed
    )

    model = MixedNaiveBayes(numeric_features, categorical_features)
    model.fit(train_rows, train_labels)

    test_probs = [model.predict_proba(r) for r in test_rows]
    metrics = evaluate_binary(test_labels, test_probs)

    scored_rows: List[Dict[str, object]] = []
    for r in rows:
        cid = str(r["client_id"])
        score = model.predict_proba(r)
        current_service_count = service_count_map.get(cid, 0)
        scored_rows.append(
            {
                "client_id": cid,
                "client_name": r["client_name"],
                "cross_sell_propensity_score": round(score, 4),
                "current_service_line_count": current_service_count,
                "active_projects": int(r["active_projects"]),
                "relationship_degree": int(r["relationship_degree"]),
                "industry_l2": r["industry_l2"],
                "state": r["state"],
            }
        )

    # Prioritize clients that are not already multi-service.
    candidate_rows = [r for r in scored_rows if int(r["current_service_line_count"]) <= 1]
    candidate_rows.sort(key=lambda x: float(x["cross_sell_propensity_score"]), reverse=True)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = output_dir / "ml_cross_sell_metrics.json"
    ranked_path = output_dir / "ml_cross_sell_ranked_candidates.csv"
    summary_path = output_dir / "ml_cross_sell_summary.md"
    pursuit_path = output_dir / "action_plans" / "top10_ml_cross_sell_pursuits.csv"
    pursuit_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "model": "MixedNaiveBayes",
        "target": "client_has_2_or_more_service_lines",
        "dataset": {
            "rows": len(rows),
            "train_rows": len(train_rows),
            "test_rows": len(test_rows),
        },
        "metrics": metrics,
        "notes": [
            "Target is a proxy label from current service adoption.",
            "Use this as Phase 2 prioritization support, not sole decision logic.",
        ],
    }

    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    write_csv(
        ranked_path,
        candidate_rows[: args.top_n],
        headers=[
            "client_id",
            "client_name",
            "cross_sell_propensity_score",
            "current_service_line_count",
            "active_projects",
            "relationship_degree",
            "industry_l2",
            "state",
        ],
    )

    pursuit_rows = build_pursuit_rows(
        candidate_rows,
        client_lookup=client_lookup,
        pursuit_top_n=args.pursuit_top_n,
    )
    write_csv(
        pursuit_path,
        pursuit_rows,
        headers=[
            "pursuit_id",
            "parent_account_id",
            "entity_client_id",
            "entity_client_name",
            "relationship_lead",
            "service_line",
            "opportunity_name",
            "stage",
            "estimated_value",
            "probability_pct",
            "risk_level",
            "blocker",
            "next_action",
            "next_action_owner",
            "next_action_due_date",
            "last_updated_utc",
        ],
    )

    top_lines = []
    for row in candidate_rows[: args.top_n]:
        top_lines.append(
            f"- {row['client_id']} - {row['client_name']}: score={row['cross_sell_propensity_score']} "
            + f"(services={row['current_service_line_count']}, active_projects={row['active_projects']}, degree={row['relationship_degree']})"
        )

    summary = [
        "# Phase 2: Cross-Sell Propensity Model",
        "",
        "## Model",
        "",
        "- Type: Mixed Naive Bayes (stdlib implementation)",
        "- Target: client has 2+ service lines (proxy)",
        "",
        "## Test Metrics",
        "",
        f"- Accuracy: {metrics['accuracy']}",
        f"- Precision: {metrics['precision']}",
        f"- Recall: {metrics['recall']}",
        f"- F1: {metrics['f1']}",
        "",
        f"## Top {args.top_n} Cross-Sell Candidates",
        "",
        *top_lines,
        "",
        "## Output Files",
        "",
        "- outputs/ml_cross_sell_metrics.json",
        "- outputs/ml_cross_sell_ranked_candidates.csv",
        "- outputs/ml_cross_sell_summary.md",
        "- outputs/action_plans/top10_ml_cross_sell_pursuits.csv",
    ]
    summary_path.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print("Cross-sell propensity model artifacts generated")
    print(f"- Metrics: {metrics_path}")
    print(f"- Ranked candidates: {ranked_path}")
    print(f"- Summary: {summary_path}")
    print(f"- Pursuits: {pursuit_path}")


if __name__ == "__main__":
    main()
