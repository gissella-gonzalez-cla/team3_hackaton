#!/usr/bin/env python3
"""Generate one portfolio account plan document per owned-entity group."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Set


NULL_TOKENS = {"", "null", "none", "na", "n/a"}


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


def slugify(value: str) -> str:
    safe = []
    for ch in value.lower():
        if ch.isalnum():
            safe.append(ch)
        elif ch in {" ", "-", "_"}:
            safe.append("-")
    slug = "".join(safe)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "group"


def to_client_lookup(clients: Iterable[Dict[str, Optional[str]]]) -> Dict[str, Dict[str, Optional[str]]]:
    lookup: Dict[str, Dict[str, Optional[str]]] = {}
    for client in clients:
        cid = (client.get("customer_id") or "").upper()
        if cid:
            lookup[cid] = client
    return lookup


def build_ownership_map(
    relationships: Iterable[Dict[str, Optional[str]]],
) -> DefaultDict[str, Set[str]]:
    ownership_map: DefaultDict[str, Set[str]] = defaultdict(set)
    for rel in relationships:
        if (rel.get("relationship_type") or "").upper() != "OWNERSHIP":
            continue
        owner = (rel.get("client_1_id") or "").upper()
        child = (rel.get("client_2_id") or "").upper()
        if owner and child:
            ownership_map[owner].add(child)
    return ownership_map


def build_project_maps(
    projects: Iterable[Dict[str, Optional[str]]],
) -> tuple[DefaultDict[str, List[Dict[str, Optional[str]]]], DefaultDict[str, Set[str]]]:
    projects_by_client: DefaultDict[str, List[Dict[str, Optional[str]]]] = defaultdict(list)
    services_by_client: DefaultDict[str, Set[str]] = defaultdict(set)
    for project in projects:
        cid = (project.get("customer_id") or "").upper()
        if not cid:
            continue
        projects_by_client[cid].append(project)
        service = project.get("project_service_line_level_2")
        if service:
            services_by_client[cid].add(service)
    return projects_by_client, services_by_client


def status_counts(projects: Iterable[Dict[str, Optional[str]]]) -> Counter:
    counts: Counter = Counter()
    for p in projects:
        counts[(p.get("project_status") or "Unknown")] += 1
    return counts


def render_plan(
    owner_id: str,
    children: List[str],
    client_lookup: Dict[str, Dict[str, Optional[str]]],
    projects_by_client: Dict[str, List[Dict[str, Optional[str]]]],
    services_by_client: Dict[str, Set[str]],
) -> str:
    owner = client_lookup.get(owner_id, {})
    owner_name = owner.get("customer_name") or "Unknown Owner"
    owner_status = owner.get("customer_status") or "Unknown"
    owner_industry = owner.get("customer_industry_level_2") or "Unknown"
    owner_state = owner.get("state_iso_code") or "Unknown"

    portfolio_ids = [owner_id] + children
    portfolio_services: Set[str] = set()
    for cid in portfolio_ids:
        portfolio_services.update(services_by_client.get(cid, set()))

    lines: List[str] = []
    lines.append(f"# Portfolio Account Plan - {owner_name} ({owner_id})")
    lines.append("")
    lines.append("## Group Overview")
    lines.append("")
    lines.append(f"- Owner: {owner_name} ({owner_id})")
    lines.append(f"- Status: {owner_status}")
    lines.append(f"- Industry: {owner_industry}")
    lines.append(f"- Geography: {owner_state}")
    lines.append(f"- Owned entities: {len(children)}")
    lines.append(f"- Portfolio service line coverage (L2): {len(portfolio_services)}")
    lines.append("")
    lines.append("## Owned-Entity Coverage")
    lines.append("")
    lines.append("| Entity | Status | Industry | State | Active Projects | Total Projects | Current Services (L2) | Adjacent Service Opportunities |")
    lines.append("|---|---|---|---|---:|---:|---|---|")

    for cid in children:
        client = client_lookup.get(cid, {})
        name = client.get("customer_name") or "Unknown"
        status = client.get("customer_status") or "Unknown"
        industry = client.get("customer_industry_level_2") or "Unknown"
        state = client.get("state_iso_code") or "Unknown"
        entity_projects = projects_by_client.get(cid, [])
        active = sum(1 for p in entity_projects if (p.get("project_status") or "").lower() == "active")
        total = len(entity_projects)
        current_services = sorted(services_by_client.get(cid, set()))
        adjacent = sorted(portfolio_services - set(current_services))

        current_services_text = ", ".join(current_services) if current_services else "None"
        adjacent_text = ", ".join(adjacent) if adjacent else "None"

        lines.append(
            f"| {name} ({cid}) | {status} | {industry} | {state} | {active} | {total} | {current_services_text} | {adjacent_text} |"
        )

    owner_projects = projects_by_client.get(owner_id, [])
    owner_status_counts = status_counts(owner_projects)
    owner_services = sorted(services_by_client.get(owner_id, set()))

    lines.append("")
    lines.append("## Owner Account Snapshot")
    lines.append("")
    lines.append(f"- Owner projects: {len(owner_projects)}")
    lines.append(f"- Owner active projects: {owner_status_counts.get('Active', 0)}")
    lines.append(f"- Owner completed projects: {owner_status_counts.get('Completed', 0)}")
    lines.append(f"- Owner current services (L2): {', '.join(owner_services) if owner_services else 'None'}")

    lines.append("")
    lines.append("## Coordinated 30-Day Plan")
    lines.append("")
    lines.append("1. Confirm relationship lead, executive sponsor, and entity owners for this group.")
    lines.append("2. Prioritize top 3 adjacent service introductions across entities.")
    lines.append("3. Launch a weekly cross-entity review with one shared pursuit list.")
    lines.append("4. Track introductions-to-opportunities and wins in one portfolio tracker.")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate one portfolio plan per ownership group")
    parser.add_argument("--client-csv", default="data/client.csv")
    parser.add_argument("--relationship-csv", default="data/relationship.csv")
    parser.add_argument("--projects-csv", default="data/projects.csv")
    parser.add_argument("--output-dir", default="outputs/portfolio_account_plans")
    args = parser.parse_args()

    clients = load_csv(Path(args.client_csv))
    relationships = load_csv(Path(args.relationship_csv))
    projects = load_csv(Path(args.projects_csv))

    client_lookup = to_client_lookup(clients)
    ownership_map = build_ownership_map(relationships)
    projects_by_client, services_by_client = build_project_maps(projects)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    index_lines = [
        "# Portfolio Account Plans",
        "",
        "One document per ownership-based entity group.",
        "",
    ]

    created = 0
    for owner_id, children_set in sorted(ownership_map.items()):
        children = sorted(children_set)
        owner_name = (client_lookup.get(owner_id, {}).get("customer_name") or owner_id)
        file_name = f"{owner_id.lower()}-{slugify(owner_name)}.md"
        output_path = output_dir / file_name

        output_path.write_text(
            render_plan(
                owner_id,
                children,
                client_lookup,
                projects_by_client,
                services_by_client,
            ),
            encoding="utf-8",
        )
        index_lines.append(f"- [{owner_name} ({owner_id})]({file_name})")
        created += 1

    (output_dir / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"Created {created} portfolio account plan documents in {output_dir}")
    print(f"Index: {output_dir / 'README.md'}")


if __name__ == "__main__":
    main()
