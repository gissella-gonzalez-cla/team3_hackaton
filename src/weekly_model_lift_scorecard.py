#!/usr/bin/env python3
"""Generate a weekly model-lift scorecard (Top N vs Rest).

This scorecard is designed for leadership readouts to quantify whether
model-prioritized candidates are stronger than the remaining population.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def to_int(value: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def pct(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round((numerator / denominator) * 100.0, 2)


def avg(values: List[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 4)


def lift(top_value: float, rest_value: float) -> float:
    if rest_value <= 0:
        return 0.0
    return round(top_value / rest_value, 4)


def rate_active(rows: List[Dict[str, str]]) -> float:
    count = sum(1 for r in rows if to_int(r.get("active_projects", "0")) > 0)
    return pct(count, len(rows))


def rate_connected(rows: List[Dict[str, str]]) -> float:
    count = sum(1 for r in rows if to_int(r.get("relationship_degree", "0")) > 0)
    return pct(count, len(rows))


def rate_actionable(rows: List[Dict[str, str]]) -> float:
    count = sum(
        1
        for r in rows
        if to_int(r.get("active_projects", "0")) > 0 or to_int(r.get("relationship_degree", "0")) > 0
    )
    return pct(count, len(rows))


def summarize_execution(top_pursuits: List[Dict[str, str]]) -> Dict[str, float]:
    n = len(top_pursuits)
    owner_assigned = sum(1 for r in top_pursuits if (r.get("next_action_owner") or "").strip())
    due_date_set = sum(1 for r in top_pursuits if (r.get("next_action_due_date") or "").strip())
    stage_progressed = sum(
        1
        for r in top_pursuits
        if (r.get("stage") or "").strip().lower() not in {"", "prioritized"}
    )

    return {
        "rows": n,
        "owner_assigned_pct": pct(owner_assigned, n),
        "due_date_set_pct": pct(due_date_set, n),
        "stage_progressed_pct": pct(stage_progressed, n),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build weekly Top-N vs Rest model lift scorecard")
    parser.add_argument(
        "--ranked-candidates-csv",
        default="outputs/ml_cross_sell_ranked_candidates.csv",
        help="Ranked candidates produced by the cross-sell model",
    )
    parser.add_argument(
        "--top-pursuits-csv",
        default="outputs/action_plans/top10_ml_cross_sell_pursuits.csv",
        help="Execution tracker for Top-N candidates",
    )
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    ranked_path = Path(args.ranked_candidates_csv)
    pursuits_path = Path(args.top_pursuits_csv)

    if not ranked_path.exists():
        raise FileNotFoundError(f"Ranked candidates file not found: {ranked_path}")
    if not pursuits_path.exists():
        raise FileNotFoundError(f"Top pursuits file not found: {pursuits_path}")

    ranked = read_csv(ranked_path)
    if len(ranked) <= args.top_n:
        raise ValueError("Need more rows than top_n in ranked candidates to compute Top vs Rest")

    top = ranked[: args.top_n]
    rest = ranked[args.top_n :]

    top_scores = [to_float(r.get("cross_sell_propensity_score", "0")) for r in top]
    rest_scores = [to_float(r.get("cross_sell_propensity_score", "0")) for r in rest]

    top_score_avg = avg(top_scores)
    rest_score_avg = avg(rest_scores)
    top_active_rate = rate_active(top)
    rest_active_rate = rate_active(rest)
    top_connected_rate = rate_connected(top)
    rest_connected_rate = rate_connected(rest)
    top_actionable_rate = rate_actionable(top)
    rest_actionable_rate = rate_actionable(rest)

    execution = summarize_execution(read_csv(pursuits_path))
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    payload = {
        "generated_utc": generated_utc,
        "top_n": args.top_n,
        "population": {
            "top_count": len(top),
            "rest_count": len(rest),
            "total_ranked_count": len(ranked),
        },
        "lift_metrics": {
            "avg_propensity_score": {
                "top": top_score_avg,
                "rest": rest_score_avg,
                "lift": lift(top_score_avg, rest_score_avg),
            },
            "active_engagement_rate_pct": {
                "top": top_active_rate,
                "rest": rest_active_rate,
                "lift": lift(top_active_rate, rest_active_rate),
            },
            "network_connected_rate_pct": {
                "top": top_connected_rate,
                "rest": rest_connected_rate,
                "lift": lift(top_connected_rate, rest_connected_rate),
            },
            "actionable_rate_pct": {
                "top": top_actionable_rate,
                "rest": rest_actionable_rate,
                "lift": lift(top_actionable_rate, rest_actionable_rate),
            },
        },
        "execution_metrics": execution,
        "notes": [
            "This is a weekly decision-support scorecard.",
            "Lift indicates how much stronger Top-N is than Rest on selected indicators.",
            "Actionability proxy = active projects > 0 OR relationship degree > 0.",
        ],
    }

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "weekly_model_lift_scorecard.json"
    md_path = out_dir / "weekly_model_lift_scorecard.md"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md_lines = [
        "# Weekly Model Lift Scorecard",
        "",
        f"Generated: {generated_utc}",
        "",
        "## Scope",
        "",
        f"- Top-N segment: {len(top)}",
        f"- Rest segment: {len(rest)}",
        f"- Total ranked candidates: {len(ranked)}",
        "",
        "## Lift Metrics (Top-N vs Rest)",
        "",
        "| Metric | Top-N | Rest | Lift |",
        "|---|---:|---:|---:|",
        f"| Avg propensity score | {top_score_avg} | {rest_score_avg} | {lift(top_score_avg, rest_score_avg)} |",
        f"| Active engagement rate (%) | {top_active_rate} | {rest_active_rate} | {lift(top_active_rate, rest_active_rate)} |",
        f"| Network connected rate (%) | {top_connected_rate} | {rest_connected_rate} | {lift(top_connected_rate, rest_connected_rate)} |",
        f"| Actionable rate (%) | {top_actionable_rate} | {rest_actionable_rate} | {lift(top_actionable_rate, rest_actionable_rate)} |",
        "",
        "## Execution Metrics (Top-N Tracker)",
        "",
        f"- Owner assigned: {execution['owner_assigned_pct']}%",
        f"- Due date set: {execution['due_date_set_pct']}%",
        f"- Stage progressed beyond Prioritized: {execution['stage_progressed_pct']}%",
        "",
        "## Output Files",
        "",
        "- outputs/weekly_model_lift_scorecard.json",
        "- outputs/weekly_model_lift_scorecard.md",
    ]
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print("Weekly model lift scorecard generated")
    print(f"- JSON: {json_path}")
    print(f"- Markdown: {md_path}")


if __name__ == "__main__":
    main()
