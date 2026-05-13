"""
Opportunities Module — CLA Brand
==================================
Two types of opportunities:
1. Unserved entities in the ontology (scarlett nodes)
2. Served entities missing service lines (seamless growth)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from utils.sample_data import (
    get_all_entities, get_all_relationships, get_opportunities,
    get_billing_history, SERVICE_LINES, ENTITY_CLUSTERS,
)

# CLA Brand Palette
CLA_NAVY = "#2E334E"
CLA_RIPTIDE = "#7DD2D3"
CLA_RIPTIDE_SHADE = "#39A5A7"
CLA_SAFFRON = "#FBC55A"
CLA_SCARLETT = "#EE5340"
CLA_CHARCOAL = "#25282A"
CLA_SMOKE = "#ABAEAB"
CLA_CLOUD = "#F7F7F6"

st.set_page_config(page_title="Opportunities", page_icon="C", layout="wide")

st.title("Opportunities")
st.caption("Find unserved entities to engage and service gaps to fill. Drive seamless growth.")

entities_df = get_all_entities()
relationships_df = get_all_relationships()
opportunities_df = get_opportunities()
billing_df = get_billing_history()

# =============================================================================
# OPPORTUNITY SUMMARY
# =============================================================================
st.subheader("Opportunity Pipeline Summary")

red_nodes = opportunities_df[opportunities_df["opportunity_type"] == "New Engagement (Red Node)"]
service_gaps = opportunities_df[opportunities_df["opportunity_type"] == "Service Gap (Seamless Growth)"]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Unserved Entities", len(red_nodes), help="Unserved entities within existing client clusters")
with col2:
    st.metric("Service Gap Opportunities", len(service_gaps), help="Served entities missing service lines")
with col3:
    st.metric("Unserved Revenue Pool", f"${red_nodes['revenue_mm'].sum():.1f}MM")
with col4:
    st.metric("Gap Revenue at Stake", f"${service_gaps['revenue_mm'].sum():.1f}MM")

st.divider()

# =============================================================================
# TABS
# =============================================================================
tab_red, tab_gaps, tab_drilldown = st.tabs([
    "New Engagements (Unserved)", "Service Gaps (Seamless)", "Entity Drill-Down"
])

# =============================================================================
# TAB 1: UNSERVED ENTITIES
# =============================================================================
with tab_red:
    st.subheader("Unserved Entities — New Engagement Opportunities")
    st.markdown("""
    These are entities **within our existing client clusters** that we do NOT currently serve.
    They already have relationships with entities we serve — the introduction pathway exists.
    
    **Why these are high-value:** The CRL already has a relationship with the cluster. These 
    entities are connected through partnership, ownership, or dependency. Converting an unserved 
    node means:
    - New revenue from an entity with an existing warm path
    - Denser ontology = better modeling
    - More touchpoints in the cluster = harder for the whole cluster to leave
    """)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        target_service = st.selectbox(
            "Target Service Line", ["All Services"] + SERVICE_LINES,
            help="Which service would you pursue for these entities?",
        )
    with col_f2:
        cluster_filter = st.selectbox(
            "Client Cluster", ["All Clusters"] + red_nodes["cluster_name"].unique().tolist(),
        )

    display_red = red_nodes.copy()
    if cluster_filter != "All Clusters":
        display_red = display_red[display_red["cluster_name"] == cluster_filter]

    st.dataframe(
        display_red[["entity_name", "entity_type", "cluster_name", "industry", "geography", "revenue_mm", "priority_score"]],
        use_container_width=True, hide_index=True,
        column_config={
            "entity_name": "Entity (Unserved)", "entity_type": "Entity Type",
            "cluster_name": "Client Cluster", "industry": "Industry", "geography": "Geography",
            "revenue_mm": st.column_config.NumberColumn("Revenue ($MM)", format="$%.1f"),
            "priority_score": st.column_config.NumberColumn("Priority Score", format="%.1f"),
        },
    )

    st.markdown("---")
    st.markdown("**Relationship Context — How are these connected to entities we serve?**")

    for _, red_entity in display_red.head(5).iterrows():
        eid = red_entity["entity_id"]
        connected = relationships_df[
            (relationships_df["source_id"] == eid) | (relationships_df["target_id"] == eid)
        ]
        if not connected.empty:
            with st.expander(f"{red_entity['entity_name']} ({red_entity['entity_type']}) — ${red_entity['revenue_mm']:.1f}MM"):
                for _, rel in connected.iterrows():
                    other_name = rel["target_name"] if rel["source_id"] == eid else rel["source_name"]
                    other_served = rel["target_served"] if rel["source_id"] == eid else rel["source_served"]
                    status = "Served" if other_served else "Not Served"
                    ownership_str = f" ({rel['ownership_pct']}%)" if pd.notna(rel["ownership_pct"]) else ""
                    st.markdown(f"- **{rel['relationship_type'].replace('_', ' ')}** → {other_name}{ownership_str} [{status}]")

# =============================================================================
# TAB 2: SERVICE GAPS
# =============================================================================
with tab_gaps:
    st.subheader("Service Gaps — Seamless Growth Opportunities")
    st.markdown("""
    These entities are **already served** but are missing service lines. Pursuing these 
    means moving toward **seamless** — bundled services that:
    - Increase revenue per entity
    - Create barriers to exit (harder to switch firms when we do assurance + tax + digital)
    - Generate better data for modeling (more touchpoints = richer profiles)
    """)

    target_gap_service = st.selectbox(
        "Show entities missing this service:", ["All Gaps"] + SERVICE_LINES, key="gap_service",
    )

    display_gaps = service_gaps.copy()
    if target_gap_service != "All Gaps":
        display_gaps = display_gaps[display_gaps["available_services"].apply(lambda x: target_gap_service in x)]

    st.dataframe(
        display_gaps[["entity_name", "entity_type", "cluster_name", "revenue_mm", "available_services", "num_available_services", "priority_score"]],
        use_container_width=True, hide_index=True,
        column_config={
            "entity_name": "Entity", "entity_type": "Type", "cluster_name": "Cluster",
            "revenue_mm": st.column_config.NumberColumn("Revenue ($MM)", format="$%.1f"),
            "available_services": "Services NOT Engaged (Opportunity)",
            "num_available_services": "Gaps",
            "priority_score": st.column_config.NumberColumn("Priority", format="%.1f"),
        },
    )

    st.markdown("---")
    st.markdown("**Seamless Progress by Service Line:**")
    st.caption("How many served entities have each service line?")

    served = entities_df[entities_df["is_served"]]
    total_served = len(served)
    svc_coverage = {}
    for svc in SERVICE_LINES:
        has_svc = served["services_engaged"].apply(lambda x: svc in x).sum()
        svc_coverage[svc] = has_svc

    svc_df = pd.DataFrame({
        "Service Line": SERVICE_LINES,
        "Entities Served": [svc_coverage[s] for s in SERVICE_LINES],
        "Coverage %": [svc_coverage[s] / total_served * 100 for s in SERVICE_LINES],
    })

    fig_coverage = px.bar(
        svc_df, x="Service Line", y="Coverage %", color="Coverage %",
        color_continuous_scale=[CLA_SCARLETT, CLA_SAFFRON, CLA_RIPTIDE],
        text="Entities Served", title="Service Line Coverage Among Served Entities",
    )
    fig_coverage.add_hline(y=100, line_dash="dash", line_color=CLA_RIPTIDE, annotation_text="Full Seamless")
    fig_coverage.update_layout(height=350, font=dict(family="Calibri, Arial, sans-serif"), plot_bgcolor="white")
    st.plotly_chart(fig_coverage, use_container_width=True)

# =============================================================================
# TAB 3: ENTITY DRILL-DOWN
# =============================================================================
with tab_drilldown:
    st.subheader("Entity Drill-Down")
    st.caption("Select an entity to see its billing health, service coverage, and position in the ontology graph")

    all_entity_names = entities_df[entities_df["annual_revenue_mm"] > 0]["entity_name"].sort_values().tolist()
    selected_entity = st.selectbox("Select Entity", all_entity_names)

    if selected_entity:
        entity_row = entities_df[entities_df["entity_name"] == selected_entity].iloc[0]
        cluster_name = entity_row["cluster_name"]

        col_d1, col_d2 = st.columns([2, 1])

        with col_d2:
            st.markdown("#### Entity Profile")
            st.markdown(f"""
            - **Name:** {entity_row['entity_name']}
            - **Type:** {entity_row['entity_type']}
            - **Cluster:** {entity_row['cluster_name']}
            - **Industry:** {entity_row['industry']}
            - **Geography:** {entity_row['geography']}
            - **Revenue:** ${entity_row['annual_revenue_mm']:.1f}MM
            - **Served:** {'Yes' if entity_row['is_served'] else 'No (Opportunity)'}
            """)

            if entity_row["is_served"]:
                st.markdown(f"""
                - **Health:** {entity_row['health_status']}
                - **Days Since Activity:** {entity_row['days_since_activity']}
                - **Services:** {', '.join(entity_row['services_engaged'])}
                - **Seamless Score:** {entity_row['seamless_score']}/4
                - **CRL Steward:** {entity_row['crl_owner']}
                """)

                st.markdown("**Service Coverage:**")
                for svc in SERVICE_LINES:
                    if svc in entity_row["services_engaged"]:
                        st.markdown(f"- {svc} — engaged")
                    else:
                        st.markdown(f"- {svc} — *opportunity*")
            else:
                st.markdown("---")
                st.markdown("**This is an unserved entity.**")
                st.markdown("All service lines are available:")
                for svc in SERVICE_LINES:
                    st.markdown(f"- {svc}")

        with col_d1:
            if entity_row["is_served"]:
                st.markdown("#### Billing Health")
                entity_billing = billing_df[billing_df["entity_name"] == selected_entity]

                if not entity_billing.empty:
                    fig_bill = px.bar(
                        entity_billing, x="period", y="billed_amount", color="service_line",
                        title=f"Billing History — {selected_entity}", barmode="stack",
                        labels={"billed_amount": "Amount ($)", "period": "Quarter"},
                        color_discrete_sequence=[CLA_NAVY, CLA_RIPTIDE, CLA_SAFFRON, CLA_SCARLETT],
                    )
                    fig_bill.update_layout(height=300, font=dict(family="Calibri, Arial, sans-serif"), plot_bgcolor="white")
                    st.plotly_chart(fig_bill, use_container_width=True)

                    recent = entity_billing[entity_billing["period"] == entity_billing["period"].max()]
                    outstanding = recent["outstanding_amount"].sum()
                    total_billed = entity_billing["billed_amount"].sum()

                    col_b1, col_b2, col_b3 = st.columns(3)
                    with col_b1:
                        st.metric("Total Billed (All Time)", f"${total_billed:,.0f}")
                    with col_b2:
                        st.metric("Current Outstanding", f"${outstanding:,.0f}")
                    with col_b3:
                        max_days = recent["days_outstanding"].max()
                        health_label = "Healthy" if max_days < 30 else ("Strained" if max_days < 60 else "Poor")
                        st.metric("AR Status", health_label)
                else:
                    st.info("No billing history available.")
            else:
                st.markdown("#### Conversion Opportunity")
                st.markdown(f"This entity is not currently served but exists within the **{cluster_name}** cluster.")
                st.markdown("**Warm path to engagement:**")
                eid = entity_row["entity_id"]
                connections = relationships_df[
                    (relationships_df["source_id"] == eid) | (relationships_df["target_id"] == eid)
                ]
                for _, conn in connections.iterrows():
                    other_name = conn["target_name"] if conn["source_id"] == eid else conn["source_name"]
                    other_served = conn["target_served"] if conn["source_id"] == eid else conn["source_served"]
                    if other_served:
                        st.markdown(f"- Connected to **{other_name}** (served) via _{conn['relationship_type'].replace('_', ' ')}_")

        # Graph position
        st.markdown("---")
        st.markdown("#### Position in Cluster Ontology")
        st.caption(f"Showing {selected_entity} (highlighted) in the {cluster_name} network")

        cluster_data = next(c for c in ENTITY_CLUSTERS if c["cluster_name"] == cluster_name)
        G = nx.DiGraph()
        for e in cluster_data["entities"]:
            G.add_node(e["id"], name=e["name"], served=e["id"] in cluster_data["engagements"])
        for rel in cluster_data["relationships"]:
            G.add_edge(rel["source"], rel["target"], relationship=rel["type"])

        pos = nx.spring_layout(G, seed=42, k=1.8)
        fig_graph = go.Figure()

        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            fig_graph.add_trace(go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                line=dict(width=1.5, color=CLA_SMOKE), hoverinfo="none", mode="lines", showlegend=False,
            ))

        selected_eid = entity_row["entity_id"]
        for node_id in G.nodes():
            x, y = pos[node_id]
            data = G.nodes[node_id]
            is_selected = node_id == selected_eid
            is_served = data["served"]

            if is_selected:
                color = CLA_NAVY
                size = 25
            elif is_served:
                color = CLA_RIPTIDE
                size = 14
            else:
                color = CLA_SCARLETT
                size = 12

            fig_graph.add_trace(go.Scatter(
                x=[x], y=[y], mode="markers+text",
                marker=dict(size=size, color=color, line=dict(width=2 if is_selected else 1, color="white")),
                text=[data["name"][:18]], textposition="top center",
                textfont=dict(size=8, color=CLA_CHARCOAL if is_selected else CLA_SMOKE),
                hovertext=f"{data['name']}<br>{'Served' if is_served else 'Not Served'}",
                hoverinfo="text", showlegend=False,
            ))

        fig_graph.update_layout(
            height=400, title=f"{selected_entity} in {cluster_name}",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=10, r=10, t=40, b=10),
            font=dict(family="Calibri, Arial, sans-serif"), plot_bgcolor="white",
        )
        st.plotly_chart(fig_graph, use_container_width=True)
