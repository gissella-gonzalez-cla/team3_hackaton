#!/usr/bin/env python3
"""Build a shared, trusted relationship view for leadership decision-making.

This script connects client, relationship, and project data to produce:
- A validated relationship model
- Portfolio-level growth/risk indicators
- Priority account snapshots for leaders
- Reusable markdown + JSON outputs
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Set, Tuple


NULL_TOKENS = {"", "null", "none", "na", "n/a"}
ALLOWED_RELATIONSHIP_TYPES = {
    "PARENT_CHILD",
    "OWNERSHIP",
    "AFFILIATE",
    "SHARED_LEADERSHIP",
    "SUCCESSOR",
}
SYMMETRIC_TYPES = {"AFFILIATE", "SHARED_LEADERSHIP"}


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


def ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round((numerator / denominator) * 100.0, 2)


def relationship_key(c1: str, rel_type: str, c2: str) -> Tuple[str, str, str]:
    if rel_type in SYMMETRIC_TYPES:
        left, right = sorted([c1, c2])
        return (left, rel_type, right)
    return (c1, rel_type, c2)


def validate_relationships(
    relationships: Iterable[Dict[str, Optional[str]]],
    client_lookup: Dict[str, Dict[str, Optional[str]]],
) -> Tuple[List[Dict[str, Optional[str]]], Counter, List[Dict[str, str]]]:
    valid: List[Dict[str, Optional[str]]] = []
    issues: Counter = Counter()
    issue_rows: List[Dict[str, str]] = []
    seen: Set[Tuple[str, str, str]] = set()

    for rel in relationships:
        c1 = (rel.get("client_1_id") or "").upper()
        c2 = (rel.get("client_2_id") or "").upper()
        rtype = (rel.get("relationship_type") or "").upper()
        rid = rel.get("id") or "unknown"

        row_issue: Optional[str] = None

        if not c1 or not c2:
            row_issue = "missing_client_id"
        elif rtype not in ALLOWED_RELATIONSHIP_TYPES:
            row_issue = "invalid_relationship_type"
        elif c1 == c2:
            row_issue = "self_reference"
        elif c1 not in client_lookup or c2 not in client_lookup:
            row_issue = "unknown_client_reference"
        else:
            rel_key = relationship_key(c1, rtype, c2)
            if rel_key in seen:
                row_issue = "duplicate_relationship"
            else:
                seen.add(rel_key)

        if row_issue:
            issues[row_issue] += 1
            issue_rows.append(
                {
                    "relationship_id": str(rid),
                    "client_1_id": c1,
                    "relationship_type": rtype,
                    "client_2_id": c2,
                    "issue": row_issue,
                }
            )
        else:
            valid.append(
                {
                    "id": str(rid),
                    "client_1_id": c1,
                    "relationship_type": rtype,
                    "client_2_id": c2,
                }
            )

    return valid, issues, issue_rows


def build_graph(
    valid_relationships: Iterable[Dict[str, Optional[str]]],
) -> Tuple[DefaultDict[str, Set[str]], DefaultDict[str, List[Dict[str, Optional[str]]]]]:
    adjacency: DefaultDict[str, Set[str]] = defaultdict(set)
    by_client: DefaultDict[str, List[Dict[str, Optional[str]]]] = defaultdict(list)

    for rel in valid_relationships:
        c1 = rel.get("client_1_id")
        c2 = rel.get("client_2_id")
        if not c1 or not c2:
            continue
        adjacency[c1].add(c2)
        adjacency[c2].add(c1)
        by_client[c1].append(rel)
        by_client[c2].append(rel)

    return adjacency, by_client


def component_sizes(adjacency: Dict[str, Set[str]]) -> List[int]:
    seen: Set[str] = set()
    sizes: List[int] = []

    for node in adjacency:
        if node in seen:
            continue
        queue: deque[str] = deque([node])
        seen.add(node)
        size = 0
        while queue:
            current = queue.popleft()
            size += 1
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        sizes.append(size)

    return sorted(sizes, reverse=True)


def client_label(client: Dict[str, Optional[str]]) -> str:
    return f"{client.get('customer_id') or 'Unknown'} - {client.get('customer_name') or 'Unknown'}"


def build_project_indexes(
    projects: Iterable[Dict[str, Optional[str]]],
) -> Tuple[DefaultDict[str, List[Dict[str, Optional[str]]]], DefaultDict[str, Set[str]]]:
    projects_by_client: DefaultDict[str, List[Dict[str, Optional[str]]]] = defaultdict(list)
    service_lines_by_client: DefaultDict[str, Set[str]] = defaultdict(set)

    for project in projects:
        cid = (project.get("customer_id") or "").upper()
        if not cid:
            continue
        projects_by_client[cid].append(project)

        service_l2 = project.get("project_service_line_level_2")
        if service_l2:
            service_lines_by_client[cid].add(service_l2)

    return projects_by_client, service_lines_by_client


def compute_priority_accounts(
    clients: List[Dict[str, Optional[str]]],
    client_lookup: Dict[str, Dict[str, Optional[str]]],
    adjacency: Dict[str, Set[str]],
    relationships_by_client: Dict[str, List[Dict[str, Optional[str]]]],
    projects_by_client: Dict[str, List[Dict[str, Optional[str]]]],
    service_lines_by_client: Dict[str, Set[str]],
    priority_ids: List[str],
    top_n: int,
) -> List[Dict[str, object]]:
    if priority_ids:
        chosen = [pid.upper() for pid in priority_ids if pid.upper() in client_lookup]
    else:
        scored: List[Tuple[int, int, str]] = []
        for client in clients:
            cid = (client.get("customer_id") or "").upper()
            if not cid:
                continue
            active_projects = sum(
                1
                for p in projects_by_client.get(cid, [])
                if (p.get("project_status") or "").lower() == "active"
            )
            degree = len(adjacency.get(cid, set()))
            scored.append((active_projects, degree, cid))
        scored.sort(reverse=True)
        chosen = [cid for _, _, cid in scored[:top_n]]

    account_rows: List[Dict[str, object]] = []

    for cid in chosen:
        client = client_lookup[cid]
        relationships = relationships_by_client.get(cid, [])
        neighbors = adjacency.get(cid, set())
        projects = projects_by_client.get(cid, [])

        rel_type_counts = Counter((r.get("relationship_type") or "Unknown") for r in relationships)
        own_services = service_lines_by_client.get(cid, set())

        neighbor_services: Set[str] = set()
        neighbor_industries: Set[str] = set()
        neighbor_geos: Set[str] = set()
        for nbr in neighbors:
            neighbor_services.update(service_lines_by_client.get(nbr, set()))
            nbr_client = client_lookup.get(nbr, {})
            industry = nbr_client.get("customer_industry_level_2")
            state = nbr_client.get("state_iso_code")
            if industry:
                neighbor_industries.add(industry)
            if state:
                neighbor_geos.add(state)

        active_projects = sum(1 for p in projects if (p.get("project_status") or "").lower() == "active")
        completed_projects = sum(
            1 for p in projects if (p.get("project_status") or "").lower() == "completed"
        )

        growth_score = 0
        if len(own_services) <= 1 and active_projects > 0:
            growth_score += 2
        if len(neighbors) >= 3 and len(own_services) < 3:
            growth_score += 1
        if len(neighbor_industries) >= 2:
            growth_score += 1

        risk_score = 0
        if len(neighbors) == 0 and active_projects > 0:
            risk_score += 2
        if rel_type_counts.get("SUCCESSOR", 0) > 0:
            risk_score += 2
        if rel_type_counts.get("OWNERSHIP", 0) > 0 and len(own_services) == 0:
            risk_score += 1
        if (client.get("customer_status") or "").lower() == "prospect" and active_projects > 0:
            risk_score += 1

        account_rows.append(
            {
                "client_id": cid,
                "client_name": client.get("customer_name") or "Unknown",
                "status": client.get("customer_status") or "Unknown",
                "industry_l2": client.get("customer_industry_level_2") or "Unknown",
                "state": client.get("state_iso_code") or "Unknown",
                "connected_entities": len(neighbors),
                "relationship_types": dict(rel_type_counts),
                "active_projects": active_projects,
                "completed_projects": completed_projects,
                "service_line_coverage": len(own_services),
                "network_service_line_coverage": len(own_services.union(neighbor_services)),
                "network_industry_span": len(neighbor_industries),
                "network_geography_span": len(neighbor_geos),
                "growth_score": growth_score,
                "risk_score": risk_score,
                "growth_signal": "High" if growth_score >= 3 else ("Medium" if growth_score >= 1 else "Low"),
                "risk_signal": "High" if risk_score >= 3 else ("Medium" if risk_score >= 1 else "Low"),
            }
        )

    account_rows.sort(key=lambda x: (int(x["growth_score"]) + int(x["risk_score"])), reverse=True)
    return account_rows


def build_portfolio_metrics(
    clients: List[Dict[str, Optional[str]]],
    valid_relationships: List[Dict[str, Optional[str]]],
    relationship_issues: Counter,
    adjacency: Dict[str, Set[str]],
    projects: List[Dict[str, Optional[str]]],
    projects_by_client: Dict[str, List[Dict[str, Optional[str]]]],
    service_lines_by_client: Dict[str, Set[str]],
) -> Dict[str, object]:
    total_clients = len(clients)
    active_clients = [c for c in clients if (c.get("customer_status") or "").lower() == "active"]
    active_client_ids = {(c.get("customer_id") or "").upper() for c in active_clients if c.get("customer_id")}

    clients_with_valid_relationship = {cid for cid, neighbors in adjacency.items() if len(neighbors) > 0}
    active_with_valid_relationship = len(active_client_ids.intersection(clients_with_valid_relationship))

    project_client_ids = {(p.get("customer_id") or "").upper() for p in projects if p.get("customer_id")}
    engaged_clients = len(project_client_ids)

    multi_service_clients = 0
    for cid in project_client_ids:
        if len(service_lines_by_client.get(cid, set())) >= 2:
            multi_service_clients += 1

    cross_sell_candidates = 0
    for cid in project_client_ids:
        if len(service_lines_by_client.get(cid, set())) == 1 and len(adjacency.get(cid, set())) > 0:
            cross_sell_candidates += 1

    prospects_connected_to_active = 0
    client_status: Dict[str, str] = {}
    for c in clients:
        cid = (c.get("customer_id") or "").upper()
        if cid:
            client_status[cid] = (c.get("customer_status") or "Unknown")

    for cid, status in client_status.items():
        if status.lower() != "prospect":
            continue
        if any(client_status.get(nbr, "").lower() == "active" for nbr in adjacency.get(cid, set())):
            prospects_connected_to_active += 1

    component_size_list = component_sizes(adjacency)
    relationship_records_total = len(valid_relationships) + sum(relationship_issues.values())

    billable_true = 0
    billable_false = 0
    for p in projects:
        val = (p.get("is_billable") or "").lower()
        if val == "true":
            billable_true += 1
        elif val == "false":
            billable_false += 1

    return {
        "total_clients": total_clients,
        "active_clients": len(active_clients),
        "total_relationship_records": relationship_records_total,
        "valid_relationship_records": len(valid_relationships),
        "relationship_data_quality_pct": ratio(len(valid_relationships), relationship_records_total),
        "validated_relationship_coverage_pct": ratio(active_with_valid_relationship, len(active_clients)),
        "engaged_clients": engaged_clients,
        "multi_service_penetration_pct": ratio(multi_service_clients, engaged_clients),
        "cross_sell_candidate_clients": cross_sell_candidates,
        "prospects_connected_to_active": prospects_connected_to_active,
        "network_components": len(component_size_list),
        "largest_component_size": component_size_list[0] if component_size_list else 0,
        "projects_total": len(projects),
        "billable_true": billable_true,
        "billable_false": billable_false,
        "report_generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }


def to_markdown_report(
    portfolio: Dict[str, object],
    quality_issues: Counter,
    accounts: List[Dict[str, object]],
    top_n: int,
) -> str:
    issue_rows = "\n".join(f"- {k}: {v}" for k, v in quality_issues.items())
    if not issue_rows:
        issue_rows = "- None"

    lines: List[str] = []
    lines.append("# Shared Trusted Relationship View")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(
        f"- Validated relationship coverage (active clients): {portfolio['validated_relationship_coverage_pct']}%"
    )
    lines.append(f"- Relationship data quality: {portfolio['relationship_data_quality_pct']}%")
    lines.append(f"- Multi-service penetration: {portfolio['multi_service_penetration_pct']}%")
    lines.append(f"- Cross-sell candidate clients: {portfolio['cross_sell_candidate_clients']}")
    lines.append(f"- Prospects connected to active accounts: {portfolio['prospects_connected_to_active']}")
    lines.append(
        f"- Network components: {portfolio['network_components']} (largest size: {portfolio['largest_component_size']})"
    )
    lines.append("")
    lines.append("## Data Validation")
    lines.append("")
    lines.append(issue_rows)
    lines.append("")
    lines.append(f"## Priority Account View (Top {top_n})")
    lines.append("")
    lines.append(
        "| Client | Status | Connected Entities | Active Projects | Service Lines | Network Service Lines | Growth | Risk |"
    )
    lines.append(
        "|---|---|---:|---:|---:|---:|---|---|"
    )

    for account in accounts[:top_n]:
        lines.append(
            "| "
            + f"{account['client_id']} - {account['client_name']}"
            + " | "
            + f"{account['status']}"
            + " | "
            + f"{account['connected_entities']}"
            + " | "
            + f"{account['active_projects']}"
            + " | "
            + f"{account['service_line_coverage']}"
            + " | "
            + f"{account['network_service_line_coverage']}"
            + " | "
            + f"{account['growth_signal']} ({account['growth_score']})"
            + " | "
            + f"{account['risk_signal']} ({account['risk_score']})"
            + " |"
        )

    lines.append("")
    lines.append("## Scale Path")
    lines.append("")
    lines.append("- Standardize relationship definitions and validation rules across all source systems.")
    lines.append("- Automate relationship coverage and quality KPIs as recurring pipeline checks.")
    lines.append("- Embed account growth/risk signals in leader workflows and account planning cadences.")
    lines.append("- Add financial measures (share of wallet, NRR, competitor displacement) when fields are available.")
    lines.append("")
    lines.append(f"Report generated at: {portfolio['report_generated_utc']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a shared, trusted relationship view with growth and risk indicators"
    )
    parser.add_argument("--client-csv", default="data/client.csv")
    parser.add_argument("--relationship-csv", default="data/relationship.csv")
    parser.add_argument("--projects-csv", default="data/projects.csv")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--top-n", type=int, default=12)
    parser.add_argument(
        "--priority-client-id",
        action="append",
        default=[],
        help="Optional: provide multiple times to pin specific strategic accounts",
    )

    args = parser.parse_args()

    client_path = Path(args.client_csv)
    relationship_path = Path(args.relationship_csv)
    projects_path = Path(args.projects_csv)

    for path in [client_path, relationship_path, projects_path]:
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")

    clients = load_csv(client_path)
    relationships = load_csv(relationship_path)
    projects = load_csv(projects_path)

    client_lookup = {}
    for client in clients:
        cid = (client.get("customer_id") or "").upper()
        if cid:
            client_lookup[cid] = client

    valid_relationships, issue_counts, issue_rows = validate_relationships(relationships, client_lookup)
    adjacency, relationships_by_client = build_graph(valid_relationships)
    projects_by_client, service_lines_by_client = build_project_indexes(projects)

    portfolio = build_portfolio_metrics(
        clients,
        valid_relationships,
        issue_counts,
        adjacency,
        projects,
        projects_by_client,
        service_lines_by_client,
    )

    accounts = compute_priority_accounts(
        clients,
        client_lookup,
        adjacency,
        relationships_by_client,
        projects_by_client,
        service_lines_by_client,
        priority_ids=args.priority_client_id,
        top_n=args.top_n,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_output = {
        "portfolio_metrics": portfolio,
        "validation_issues": dict(issue_counts),
        "validation_issue_rows": issue_rows,
        "priority_accounts": accounts,
    }

    json_path = output_dir / "shared_relationship_view.json"
    md_path = output_dir / "shared_relationship_view.md"

    json_path.write_text(json.dumps(json_output, indent=2), encoding="utf-8")
    md_path.write_text(
        to_markdown_report(portfolio, issue_counts, accounts, top_n=args.top_n),
        encoding="utf-8",
    )

    print("Shared Relationship View generated")
    print(f"- JSON: {json_path}")
    print(f"- Markdown: {md_path}")
    print(
        "- Key KPI: Validated relationship coverage "
        + f"{portfolio['validated_relationship_coverage_pct']}%"
    )


if __name__ == "__main__":
    main()
