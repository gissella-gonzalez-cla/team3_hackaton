#!/usr/bin/env python3
"""Relationship View analysis for hackathon client data.

Focus areas:
1) Parent / child
2) Shared ownership
3) Connections between clients
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Set, Tuple


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


def to_client_lookup(clients: Iterable[Dict[str, Optional[str]]]) -> Dict[str, Dict[str, Optional[str]]]:
    lookup: Dict[str, Dict[str, Optional[str]]] = {}
    for c in clients:
        cid = c.get("customer_id")
        if cid:
            lookup[cid] = c
    return lookup


def get_client_label(client_lookup: Dict[str, Dict[str, Optional[str]]], client_id: str) -> str:
    client = client_lookup.get(client_id)
    if not client:
        return f"{client_id} (Unknown Client)"
    return f"{client_id} ({client.get('customer_name') or 'Unknown Name'})"


def filter_relationships(
    relationships: Iterable[Dict[str, Optional[str]]],
    client_id: Optional[str],
    relationship_type: Optional[str],
) -> List[Dict[str, Optional[str]]]:
    scoped = list(relationships)

    if relationship_type:
        wanted = relationship_type.strip().upper()
        scoped = [r for r in scoped if (r.get("relationship_type") or "").upper() == wanted]

    if client_id:
        cid = client_id.strip().upper()
        scoped = [
            r
            for r in scoped
            if (r.get("client_1_id") or "").upper() == cid or (r.get("client_2_id") or "").upper() == cid
        ]

    return scoped


def build_undirected_graph(
    relationships: Iterable[Dict[str, Optional[str]]],
) -> DefaultDict[str, Set[str]]:
    graph: DefaultDict[str, Set[str]] = defaultdict(set)
    for rel in relationships:
        c1 = rel.get("client_1_id")
        c2 = rel.get("client_2_id")
        if not c1 or not c2:
            continue
        graph[c1].add(c2)
        graph[c2].add(c1)
    return graph


def connected_components(graph: Dict[str, Set[str]]) -> List[Set[str]]:
    components: List[Set[str]] = []
    seen: Set[str] = set()

    for node in graph:
        if node in seen:
            continue
        comp: Set[str] = set()
        queue: deque[str] = deque([node])
        seen.add(node)
        while queue:
            current = queue.popleft()
            comp.add(current)
            for nbr in graph[current]:
                if nbr not in seen:
                    seen.add(nbr)
                    queue.append(nbr)
        components.append(comp)

    return components


def print_counter(counter: Counter, title: str, top_n: int) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    for label, count in counter.most_common(top_n):
        print(f"{label:<35} {count:>6}")


def summarize_parent_child(
    relationships: Iterable[Dict[str, Optional[str]]],
) -> Tuple[Counter, Counter]:
    parent_count: Counter = Counter()
    child_count: Counter = Counter()

    for rel in relationships:
        if (rel.get("relationship_type") or "").upper() != "PARENT_CHILD":
            continue
        parent = rel.get("client_1_id")
        child = rel.get("client_2_id")
        if parent:
            parent_count[parent] += 1
        if child:
            child_count[child] += 1

    return parent_count, child_count


def summarize_ownership(
    relationships: Iterable[Dict[str, Optional[str]]],
) -> Counter:
    owner_count: Counter = Counter()
    for rel in relationships:
        if (rel.get("relationship_type") or "").upper() != "OWNERSHIP":
            continue
        owner = rel.get("client_1_id")
        if owner:
            owner_count[owner] += 1
    return owner_count


def print_client_edges(
    scoped_relationships: Iterable[Dict[str, Optional[str]]],
    client_lookup: Dict[str, Dict[str, Optional[str]]],
    top_n: int,
) -> None:
    rows = list(scoped_relationships)
    if not rows:
        return

    print("\nRelationships In Scope")
    print("----------------------")
    print(f"Showing up to {top_n} rows")

    for rel in rows[:top_n]:
        c1 = rel.get("client_1_id") or "Unknown"
        c2 = rel.get("client_2_id") or "Unknown"
        rtype = rel.get("relationship_type") or "Unknown"
        left = get_client_label(client_lookup, c1) if c1 != "Unknown" else "Unknown"
        right = get_client_label(client_lookup, c2) if c2 != "Unknown" else "Unknown"
        print(f"{left} --[{rtype}]--> {right}")


def run_relationship_view(
    clients: List[Dict[str, Optional[str]]],
    relationships: List[Dict[str, Optional[str]]],
    scoped_relationships: List[Dict[str, Optional[str]]],
    top_n: int,
) -> None:
    client_lookup = to_client_lookup(clients)
    scoped_client_ids: Set[str] = set()
    for rel in scoped_relationships:
        c1 = rel.get("client_1_id")
        c2 = rel.get("client_2_id")
        if c1:
            scoped_client_ids.add(c1)
        if c2:
            scoped_client_ids.add(c2)

    relationship_type_counts = Counter((r.get("relationship_type") or "Unknown") for r in scoped_relationships)
    print("Relationship View Analysis")
    print("==========================")
    print(f"Total clients: {len(clients)}")
    print(f"Total relationships (all): {len(relationships)}")
    print(f"Relationships in current scope: {len(scoped_relationships)}")
    print(f"Unique clients in current scope: {len(scoped_client_ids)}")

    print_counter(relationship_type_counts, "Relationship Type Distribution", top_n=top_n)

    parent_count, child_count = summarize_parent_child(scoped_relationships)
    if parent_count:
        relabeled_parents = Counter({get_client_label(client_lookup, cid): cnt for cid, cnt in parent_count.items()})
        print_counter(relabeled_parents, "Parent Entities By Number Of Children", top_n=top_n)

    if child_count:
        relabeled_children = Counter({get_client_label(client_lookup, cid): cnt for cid, cnt in child_count.items()})
        print_counter(relabeled_children, "Child Entities In Parent-Child Links", top_n=top_n)

    owner_count = summarize_ownership(scoped_relationships)
    if owner_count:
        relabeled_owners = Counter({get_client_label(client_lookup, cid): cnt for cid, cnt in owner_count.items()})
        print_counter(relabeled_owners, "Owners By Number Of Ownership Links", top_n=top_n)

    graph = build_undirected_graph(scoped_relationships)
    components = connected_components(graph)
    component_sizes = Counter({f"Component size {len(comp)}": 1 for comp in components})
    if component_sizes:
        print_counter(component_sizes, "Connection Component Sizes", top_n=top_n)

    degree_counter = Counter({cid: len(neighbors) for cid, neighbors in graph.items()})
    if degree_counter:
        relabeled_degree = Counter({get_client_label(client_lookup, cid): cnt for cid, cnt in degree_counter.items()})
        print_counter(relabeled_degree, "Most Connected Clients (Degree)", top_n=top_n)

    print_client_edges(scoped_relationships, client_lookup, top_n=top_n)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze relationship view: parent/child, ownership, and connections"
    )
    parser.add_argument(
        "--client-csv",
        default="data/client.csv",
        help="Path to client.csv (default: data/client.csv)",
    )
    parser.add_argument(
        "--relationship-csv",
        default="data/relationship.csv",
        help="Path to relationship.csv (default: data/relationship.csv)",
    )
    parser.add_argument(
        "--client-id",
        default=None,
        help="Optional client filter (example: C100377)",
    )
    parser.add_argument(
        "--relationship-type",
        default=None,
        help="Optional type filter (example: PARENT_CHILD, OWNERSHIP, AFFILIATE)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Top N rows for distribution outputs and edge list (default: 10)",
    )

    args = parser.parse_args()

    client_path = Path(args.client_csv)
    relationship_path = Path(args.relationship_csv)

    if not client_path.exists():
        raise FileNotFoundError(f"Client CSV not found: {client_path}")
    if not relationship_path.exists():
        raise FileNotFoundError(f"Relationship CSV not found: {relationship_path}")

    clients = load_csv(client_path)
    relationships = load_csv(relationship_path)
    scoped_relationships = filter_relationships(
        relationships,
        client_id=args.client_id,
        relationship_type=args.relationship_type,
    )

    if not scoped_relationships:
        print("No relationships match the provided filters.")
        return

    run_relationship_view(clients, relationships, scoped_relationships, top_n=args.top_n)


if __name__ == "__main__":
    main()
