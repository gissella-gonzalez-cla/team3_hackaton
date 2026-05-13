#!/usr/bin/env python3
"""Engagement View analysis for hackathon data.

Focus areas:
1) What services are clients using?
2) What projects exist?
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional


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


def filter_projects(
    projects: Iterable[Dict[str, Optional[str]]],
    client_id: Optional[str],
    client_name: Optional[str],
    project_status: Optional[str],
) -> List[Dict[str, Optional[str]]]:
    scoped = list(projects)

    if client_id:
        cid = client_id.strip().upper()
        scoped = [p for p in scoped if (p.get("customer_id") or "").upper() == cid]

    if client_name:
        needle = client_name.strip().lower()
        scoped = [p for p in scoped if needle in (p.get("customer_name") or "").lower()]

    if project_status:
        wanted = project_status.strip().lower()
        scoped = [p for p in scoped if (p.get("project_status") or "").lower() == wanted]

    return scoped


def count_field(rows: Iterable[Dict[str, Optional[str]]], field: str) -> Counter:
    counts: Counter = Counter()
    for row in rows:
        value = row.get(field)
        if value:
            counts[value] += 1
        else:
            counts["Unknown"] += 1
    return counts


def print_counter(title: str, counter: Counter, top_n: int) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    for label, count in counter.most_common(top_n):
        print(f"{label:<55} {count:>6}")


def print_projects_table(projects: List[Dict[str, Optional[str]]], max_rows: int) -> None:
    print("\nProject Inventory")
    print("-----------------")
    print(f"Showing up to {max_rows} projects")
    for p in projects[:max_rows]:
        pid = p.get("project_id") or "Unknown"
        pname = p.get("project_name") or "Unknown"
        cname = p.get("customer_name") or "Unknown"
        pstatus = p.get("project_status") or "Unknown"
        service_l2 = p.get("project_service_line_level_2") or "Unknown"
        start_date = p.get("project_start_date") or "Unknown"
        end_date = p.get("project_end_date") or "Unknown"
        print(
            f"{pid} | {pstatus:<10} | {service_l2:<12} | {start_date} -> {end_date} | {cname} | {pname}"
        )


def run_engagement_view(projects_all: List[Dict[str, Optional[str]]], projects_scoped: List[Dict[str, Optional[str]]], top_n: int) -> None:
    print("Engagement View Analysis")
    print("========================")
    print(f"Total projects in dataset: {len(projects_all)}")
    print(f"Projects in current scope: {len(projects_scoped)}")

    # Service usage summaries.
    service_l2 = count_field(projects_scoped, "project_service_line_level_2")
    service_l3 = count_field(projects_scoped, "project_service_line_level_3")
    service_l4 = count_field(projects_scoped, "project_service_line_level_4")
    project_types = count_field(projects_scoped, "project_type_name")
    print_counter("Services Used (Service Line L2)", service_l2, top_n=top_n)
    print_counter("Services Used (Service Line L3)", service_l3, top_n=top_n)
    print_counter("Services Used (Service Line L4)", service_l4, top_n=top_n)
    print_counter("Project Types", project_types, top_n=top_n)

    # Project inventory summaries.
    project_status = count_field(projects_scoped, "project_status")
    billable = count_field(projects_scoped, "is_billable")
    clients = count_field(projects_scoped, "customer_name")
    leaders = count_field(projects_scoped, "project_leader_name")
    print_counter("Project Status Distribution", project_status, top_n=top_n)
    print_counter("Billable Distribution", billable, top_n=top_n)
    print_counter("Projects By Client", clients, top_n=top_n)
    print_counter("Projects By Project Leader", leaders, top_n=top_n)

    print_projects_table(projects_scoped, max_rows=top_n)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze engagement view: services used and project inventory"
    )
    parser.add_argument(
        "--projects-csv",
        default="data/projects.csv",
        help="Path to projects.csv (default: data/projects.csv)",
    )
    parser.add_argument(
        "--client-id",
        default=None,
        help="Optional exact client ID filter (example: C100377)",
    )
    parser.add_argument(
        "--client-name",
        default=None,
        help="Optional case-insensitive partial client name filter",
    )
    parser.add_argument(
        "--project-status",
        default=None,
        help="Optional project status filter (example: Active, Completed)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Top N rows for summaries and project listing (default: 10)",
    )

    args = parser.parse_args()

    projects_path = Path(args.projects_csv)
    if not projects_path.exists():
        raise FileNotFoundError(f"Projects CSV not found: {projects_path}")

    projects_all = load_csv(projects_path)
    projects_scoped = filter_projects(
        projects_all,
        client_id=args.client_id,
        client_name=args.client_name,
        project_status=args.project_status,
    )

    if not projects_scoped:
        print("No projects match the provided filters.")
        return

    run_engagement_view(projects_all, projects_scoped, top_n=args.top_n)


if __name__ == "__main__":
    main()
