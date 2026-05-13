"""
One-Firm View — Client Ontology & Firmwide Health
===================================================
CLA Brand Colors:
- Riptide #7DD2D3 = Served / Healthy
- Saffron #FBC55A = Strained
- Scarlett #EE5340 = Poor / Unserved (opportunity)
- Navy #2E334E = Primary / Anchoring
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from utils.sample_data import (
    get_all_entities, get_all_relationships, get_cluster_summary,
    get_seamless_analysis, get_billing_history, SERVICE_LINES,
    ENTITY_CLUSTERS,
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

st.set_page_config(page_title="One-Firm View", page_icon="C", layout="wide")

st.title("One-Firm View")
st.caption("Every client is a firm client. CRLs are stewards. Riptide = served. Scarlett = opportunity.")

entities_df = get_all_entities()
relationships_df = get_all_relationships()
cluster_summary = get_cluster_summary()
served_df = entities_df[entities_df["is_served"]]

# =============================================================================
# FIRMWIDE EXECUTIVE PULSE
# =============================================================================
st.subheader("Firmwide Portfolio Health")

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Total Entities", len(entities_df))
with col2:
    st.metric("Served", len(served_df))
with col3:
    unserved = entities_df[(~entities_df["is_served"]) & (entities_df["annual_revenue_mm"] > 0)]
    st.metric("Unserved", len(unserved))
with col4:
    healthy = served_df[served_df["health_status"] == "Healthy"].shape[0]
    st.metric("Healthy (<30d)", healthy)
with col5:
    strained = served_df[served_df["health_status"] == "Strained"].shape[0]
    st.metric("Strained (30-60d)", strained)
with col6:
    poor = served_df[served_df["health_status"] == "Poor"].shape[0]
    st.metric("Poor (60+d)", poor)

# Health bar
total_served = len(served_df)
if total_served > 0:
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        st.progress(healthy / total_served, text=f"Healthy: {healthy}/{total_served}")
    with col_h2:
        st.progress(strained / total_served, text=f"Strained: {strained}/{total_served}")
    with col_h3:
        st.progress(poor / total_served, text=f"Poor: {poor}/{total_served}")

st.divider()

# =============================================================================
# TABS
# =============================================================================
tab_ontology, tab_clusters, tab_health, tab_seamless = st.tabs([
    "Client Ontology Graph", "Cluster Overview", "Health Monitor", "Seamless Analysis"
])

# =============================================================================
# TAB 1: ONTOLOGY GRAPH
# =============================================================================
with tab_ontology:
    st.subheader("Client Entity Ontology")
    st.markdown("""
    **How to read this graph:**
    - **Riptide nodes** = Entities we currently serve (engaged)
    - **Scarlett nodes** = Entities we do NOT serve (opportunities)
    - **Lines** = Relationships (partner, owner, dependent, working partnership)
    - **Node size** = Revenue scale
    
    Select a client cluster to explore its entity web:
    """)

    cluster_names = [c["cluster_name"] for c in ENTITY_CLUSTERS]
    selected_cluster = st.selectbox("Select Client Cluster", cluster_names)

    cluster_data = next(c for c in ENTITY_CLUSTERS if c["cluster_name"] == selected_cluster)
    cluster_entities = entities_df[entities_df["cluster_name"] == selected_cluster]
    cluster_rels = relationships_df[relationships_df["cluster_name"] == selected_cluster]

    # Build graph
    G = nx.DiGraph()
    engagements = cluster_data["engagements"]

    for entity in cluster_data["entities"]:
        G.add_node(
            entity["id"],
            name=entity["name"],
            entity_type=entity["type"],
            revenue=entity["revenue_mm"],
            served=entity["id"] in engagements,
            services=engagements.get(entity["id"], []),
        )

    for rel in cluster_data["relationships"]:
        G.add_edge(rel["source"], rel["target"], relationship=rel["type"], ownership_pct=rel.get("ownership_pct"))

    pos = nx.spring_layout(G, seed=42, k=1.8, iterations=50)

    # Edges
    edge_traces = []
    annotations = []
    edge_color_map = {
        "partner_of": CLA_SMOKE,
        "owner_of": CLA_NAVY,
        "dependent_of": CLA_RIPTIDE_SHADE,
        "working_partnership": CLA_SAFFRON,
        "beneficiary_of": CLA_RIPTIDE,
    }

    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        rel_type = edge[2]["relationship"]
        color = edge_color_map.get(rel_type, CLA_SMOKE)

        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=2, color=color),
            hoverinfo="none", mode="lines", showlegend=False,
        ))

        mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
        label = rel_type.replace("_", " ")
        ownership = edge[2].get("ownership_pct")
        if ownership:
            label += f" ({ownership}%)"
        annotations.append(dict(x=mid_x, y=mid_y, text=label, showarrow=False, font=dict(size=8, color=color), opacity=0.8))

    # Nodes
    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    node_colors, node_sizes, node_texts, hover_texts = [], [], [], []

    for node_id in G.nodes():
        data = G.nodes[node_id]
        is_served = data["served"]

        if is_served:
            health = cluster_entities[cluster_entities["entity_id"] == node_id]["health_status"].iloc[0] if node_id in cluster_entities["entity_id"].values else "Healthy"
            if health == "Healthy":
                node_colors.append(CLA_RIPTIDE)
            elif health == "Strained":
                node_colors.append(CLA_SAFFRON)
            else:
                node_colors.append(CLA_SCARLETT)
        else:
            node_colors.append(CLA_SCARLETT)

        size = max(15, min(50, 15 + data["revenue"] * 0.5))
        node_sizes.append(size)

        name = data["name"]
        node_texts.append(name[:20] + "..." if len(name) > 20 else name)

        services_str = ", ".join(data["services"]) if data["services"] else "None"
        hover_texts.append(
            f"<b>{name}</b><br>Type: {data['entity_type']}<br>Revenue: ${data['revenue']:.1f}MM<br>"
            f"Status: {'Served' if is_served else 'Not Served'}<br>Services: {services_str}"
        )

    fig = go.Figure()
    for trace in edge_traces:
        fig.add_trace(trace)

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        marker=dict(size=node_sizes, color=node_colors, line=dict(width=2, color="white"), opacity=0.9),
        text=node_texts, textposition="top center", textfont=dict(size=9, color=CLA_CHARCOAL),
        hovertext=hover_texts, hoverinfo="text", showlegend=False,
    ))

    # Legend
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", marker=dict(size=12, color=CLA_RIPTIDE), name="Served (Healthy)"))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", marker=dict(size=12, color=CLA_SAFFRON), name="Served (Strained)"))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", marker=dict(size=12, color=CLA_SCARLETT), name="Not Served / Poor"))

    fig.update_layout(
        title=f"Entity Ontology — {selected_cluster}",
        height=600,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        annotations=annotations,
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Calibri, Arial, sans-serif"),
        plot_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Entity table
    st.markdown("---")
    st.markdown(f"**Entities in {selected_cluster}:**")
    display_cols = ["entity_name", "entity_type", "is_served", "services_engaged", "health_status", "annual_revenue_mm", "geography"]
    st.dataframe(
        cluster_entities[display_cols].sort_values("annual_revenue_mm", ascending=False),
        use_container_width=True, hide_index=True,
        column_config={
            "entity_name": "Entity", "entity_type": "Type", "is_served": "Served?",
            "services_engaged": "Services", "health_status": "Health",
            "annual_revenue_mm": st.column_config.NumberColumn("Revenue ($MM)", format="$%.1f"),
            "geography": "Geography",
        },
    )

# =============================================================================
# TAB 2: CLUSTER OVERVIEW
# =============================================================================
with tab_clusters:
    st.subheader("Client Cluster Portfolio")
    st.caption("Each cluster is a web of related entities (partnerships, individuals, trusts, corps)")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        geo_filter = st.multiselect("Filter by Geography", entities_df["geography"].unique().tolist())
    with col_f2:
        ind_filter = st.multiselect("Filter by Industry", entities_df["industry"].unique().tolist())

    st.dataframe(
        cluster_summary.sort_values("total_revenue_mm", ascending=False),
        use_container_width=True, hide_index=True,
        column_config={
            "cluster_name": "Client Cluster", "total_entities": "Total Entities",
            "served_entities": "Served", "unserved_entities": "Unserved",
            "total_revenue_mm": st.column_config.NumberColumn("Total Revenue ($MM)", format="$%.1f"),
            "served_revenue_mm": st.column_config.NumberColumn("Served Revenue ($MM)", format="$%.1f"),
            "penetration_pct": st.column_config.NumberColumn("Penetration %", format="%.1f%%"),
            "avg_seamless": st.column_config.NumberColumn("Avg Seamless Score", format="%.1f"),
            "healthy_count": "Healthy", "strained_count": "Strained", "poor_count": "Poor",
        },
    )

    fig_pen = px.bar(
        cluster_summary.sort_values("penetration_pct"),
        x="penetration_pct", y="cluster_name", orientation="h",
        color="penetration_pct",
        color_continuous_scale=[CLA_SCARLETT, CLA_SAFFRON, CLA_RIPTIDE],
        title="Cluster Penetration Rate (% of entities served)",
        labels={"penetration_pct": "Penetration %", "cluster_name": ""},
    )
    fig_pen.update_layout(height=350, font=dict(family="Calibri, Arial, sans-serif"), plot_bgcolor="white")
    st.plotly_chart(fig_pen, use_container_width=True)

# =============================================================================
# TAB 3: HEALTH MONITOR
# =============================================================================
with tab_health:
    st.subheader("Relationship Health Monitor")
    st.markdown("""
    Health is based on our **90-day AR policy**:
    - **Healthy** — Payment received or check-in within 30 days
    - **Strained** — 30-59 days since last payment or meaningful check-in
    - **Poor** — 60+ days overdue. Relationship at risk of deterioration.
    """)

    health_pivot = served_df.groupby(["cluster_name", "health_status"]).size().unstack(fill_value=0).reset_index()
    for col in ["Healthy", "Strained", "Poor"]:
        if col not in health_pivot.columns:
            health_pivot[col] = 0

    fig_health = px.bar(
        health_pivot, x="cluster_name", y=["Healthy", "Strained", "Poor"], barmode="stack",
        color_discrete_map={"Healthy": CLA_RIPTIDE, "Strained": CLA_SAFFRON, "Poor": CLA_SCARLETT},
        title="Health Status by Client Cluster",
        labels={"value": "Entity Count", "cluster_name": ""},
    )
    fig_health.update_layout(height=400, font=dict(family="Calibri, Arial, sans-serif"), plot_bgcolor="white")
    st.plotly_chart(fig_health, use_container_width=True)

    st.markdown("**Entities Needing Attention (Strained or Poor):**")
    at_risk = served_df[served_df["health_status"].isin(["Strained", "Poor"])].sort_values("days_since_activity", ascending=False)

    if not at_risk.empty:
        st.dataframe(
            at_risk[["entity_name", "cluster_name", "health_status", "days_since_activity", "services_engaged", "annual_revenue_mm", "crl_owner"]],
            use_container_width=True, hide_index=True,
            column_config={
                "entity_name": "Entity", "cluster_name": "Cluster", "health_status": "Status",
                "days_since_activity": "Days Since Activity", "services_engaged": "Services",
                "annual_revenue_mm": st.column_config.NumberColumn("Revenue ($MM)", format="$%.1f"),
                "crl_owner": "CRL Steward",
            },
        )
    else:
        st.success("All served entities are healthy.")

# =============================================================================
# TAB 4: SEAMLESS ANALYSIS
# =============================================================================
with tab_seamless:
    st.subheader("Seamless Analysis")
    st.markdown("""
    **Seamless** = Bundled services to the same client. Benefits:
    - Higher revenue extraction per client
    - Stronger retention (higher barriers to exit)
    - Deeper relationship = better data = better modeling
    
    | Score | Status | Retention Risk |
    |-------|--------|----------------|
    | 1 service | Single Service | HIGH — easy to leave |
    | 2 services | Partially Seamless | Moderate |
    | 3+ services | Fully Seamless | LOW — deeply embedded |
    """)

    seamless_df = get_seamless_analysis()
    seamless_counts = seamless_df["seamless_status"].value_counts().reset_index()
    seamless_counts.columns = ["Status", "Count"]

    fig_seamless = px.pie(
        seamless_counts, names="Status", values="Count", color="Status",
        color_discrete_map={
            "Fully Seamless (3+)": CLA_RIPTIDE,
            "Partially Seamless (2)": CLA_SAFFRON,
            "Single Service (At Risk)": CLA_SCARLETT,
        },
        title="Served Entities by Seamless Status", hole=0.4,
    )
    fig_seamless.update_layout(font=dict(family="Calibri, Arial, sans-serif"))
    st.plotly_chart(fig_seamless, use_container_width=True)

    st.markdown("**Single-Service Entities (High Exit Risk):**")
    single_svc = seamless_df[seamless_df["seamless_status"] == "Single Service (At Risk)"].sort_values("annual_revenue_mm", ascending=False)

    if not single_svc.empty:
        st.dataframe(
            single_svc[["entity_name", "cluster_name", "services_engaged", "services_not_engaged", "annual_revenue_mm", "health_status"]],
            use_container_width=True, hide_index=True,
            column_config={
                "entity_name": "Entity", "cluster_name": "Cluster",
                "services_engaged": "Current Service", "services_not_engaged": "Available for Seamless",
                "annual_revenue_mm": st.column_config.NumberColumn("Revenue ($MM)", format="$%.1f"),
                "health_status": "Health",
            },
        )

    st.markdown("---")
    st.markdown("**Service Line Opportunity (available for seamless bundling):**")

    service_opp = {"Service Line": [], "Entities Not Receiving": [], "Revenue at Stake ($MM)": []}
    for svc in SERVICE_LINES:
        not_receiving = seamless_df[seamless_df["services_not_engaged"].apply(lambda x: svc in x)]
        service_opp["Service Line"].append(svc)
        service_opp["Entities Not Receiving"].append(len(not_receiving))
        service_opp["Revenue at Stake ($MM)"].append(round(not_receiving["annual_revenue_mm"].sum(), 1))

    svc_opp_df = pd.DataFrame(service_opp)
    fig_svc = px.bar(
        svc_opp_df, x="Service Line", y="Entities Not Receiving",
        color="Revenue at Stake ($MM)", color_continuous_scale=[CLA_SAFFRON, CLA_SCARLETT],
        title="Seamless Expansion Opportunity by Service Line", text="Entities Not Receiving",
    )
    fig_svc.update_layout(height=350, font=dict(family="Calibri, Arial, sans-serif"), plot_bgcolor="white")
    st.plotly_chart(fig_svc, use_container_width=True)
