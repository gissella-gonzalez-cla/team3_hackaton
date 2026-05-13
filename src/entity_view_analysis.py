#!/usr/bin/env python3
"""Entity View analysis for hackathon client data.

Focus areas:
1) Who is the client? (client profile)
2) Industry distribution
3) Geography distribution
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


def load_clients(client_csv_path: Path) -> List[Dict[str, Optional[str]]]:
    with client_csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [{k: normalize(v) for k, v in row.items()} for row in reader]


def filter_clients(
    clients: Iterable[Dict[str, Optional[str]]],
    client_id: Optional[str],
    client_name: Optional[str],
) -> List[Dict[str, Optional[str]]]:
    filtered = list(clients)

    if client_id:
        cid = client_id.strip().lower()
        filtered = [c for c in filtered if (c.get("customer_id") or "").lower() == cid]

    if client_name:
        needle = client_name.strip().lower()
        filtered = [c for c in filtered if needle in (c.get("customer_name") or "").lower()]

    return filtered


def count_field(rows: Iterable[Dict[str, Optional[str]]], field: str) -> Counter:
    counter: Counter = Counter()
    for row in rows:
        value = row.get(field)
        if value:
            counter[value] += 1
        else:
            counter["Unknown"] += 1
    return counter


def print_counter(counter: Counter, title: str, top_n: int = 10) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    for label, count in counter.most_common(top_n):
        print(f"{label:<50} {count:>6}")


def print_client_profile(client: Dict[str, Optional[str]]) -> None:
    print("\nClient Profile")
    print("--------------")

    fields = [
        ("Customer ID", "customer_id"),
        ("Customer Name", "customer_name"),
        ("Status", "customer_status"),
        ("Category", "customer_category"),
        ("Industry L2", "customer_industry_level_2"),
        ("Industry L3", "customer_industry_level_3"),
        ("Industry L4", "customer_industry_level_4"),
        ("SIC Code", "customer_sic_code"),
        ("SIC Description", "customer_sic_code_name"),
        ("City", "city"),
        ("State", "state_iso_code"),
        ("Country", "country_iso_code"),
        ("Parent Customer ID", "parent_customer_id"),
        ("Parent Customer Name", "parent_customer_name"),
    ]

    for label, key in fields:
        print(f"{label:<22}: {client.get(key) or 'Unknown'}")


def run_entity_view(
    all_clients: List[Dict[str, Optional[str]]],
    scoped_clients: List[Dict[str, Optional[str]]],
    top_n: int,
) -> None:
    print("Entity View Analysis")
    print("====================")
    print(f"Total clients in dataset: {len(all_clients)}")
    print(f"Clients in current scope: {len(scoped_clients)}")

    status_counts = count_field(scoped_clients, "customer_status")
    print_counter(status_counts, "Client Status Distribution", top_n=top_n)

    industry_l2 = count_field(scoped_clients, "customer_industry_level_2")
    industry_l3 = count_field(scoped_clients, "customer_industry_level_3")
    industry_l4 = count_field(scoped_clients, "customer_industry_level_4")
    print_counter(industry_l2, "Industry Distribution (Level 2)", top_n=top_n)
    print_counter(industry_l3, "Industry Distribution (Level 3)", top_n=top_n)
    print_counter(industry_l4, "Industry Distribution (Level 4)", top_n=top_n)

    country_counts = count_field(scoped_clients, "country_iso_code")
    state_counts = count_field(scoped_clients, "state_iso_code")
    city_counts = count_field(scoped_clients, "city")
    print_counter(country_counts, "Geography Distribution (Country)", top_n=top_n)
    print_counter(state_counts, "Geography Distribution (State)", top_n=top_n)
    print_counter(city_counts, "Geography Distribution (City)", top_n=top_n)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze entity view: client profile, industry, and geography"
    )
    parser.add_argument(
        "--client-csv",
        default="data/client.csv",
        help="Path to client.csv (default: data/client.csv)",
    )
    parser.add_argument(
        "--client-id",
        default=None,
        help="Optional exact customer_id filter (example: C100377)",
    )
    parser.add_argument(
        "--client-name",
        default=None,
        help="Optional case-insensitive partial customer_name filter",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Top N rows for distribution outputs (default: 10)",
    )

    args = parser.parse_args()

    client_csv_path = Path(args.client_csv)
    if not client_csv_path.exists():
        raise FileNotFoundError(f"Client CSV not found: {client_csv_path}")

    all_clients = load_clients(client_csv_path)
    scoped_clients = filter_clients(all_clients, args.client_id, args.client_name)

    if not scoped_clients:
        print("No clients match the provided filters.")
        return

    if len(scoped_clients) == 1:
        print_client_profile(scoped_clients[0])
    elif args.client_id or args.client_name:
        print(f"Matched {len(scoped_clients)} clients using provided filters.")

    run_entity_view(all_clients, scoped_clients, top_n=args.top_n)


if __name__ == "__main__":
    main()
