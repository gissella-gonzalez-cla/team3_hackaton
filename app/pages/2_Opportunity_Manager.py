"""
Opportunity Manager — Leads, Service Gaps & Client Check-Ins
=============================================================
Consolidated view for CRLs to manage opportunities and client interactions.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from utils.sample_data import (
    get_all_entities, get_all_relationships, get_opportunities,
    get_billing_history, get_interaction_history, get_crl_actions,
    SERVICE_LINES, ENTITY_CLUSTERS, CRL_NAMES,
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

st.set_page_config(page_title="Opportunity Manager", page_icon="C", layout="wide")

st.title("Opportunity Manager")
st.caption("Manage leads, service gaps, and client interactions in one place.")

entities_df = get_all_entities()
relationships_df = get_all_relationships()
opportunities_df = get_opportunities()
billing_df = get_billing_history()
interactions_df = get_interaction_history()

crl_name = st.session_state.get("crl_name", "")

# =============================================================================
# DASHBOARD SUMMARY
# =============================================================================
st.subheader("Pipeline Summary")

red_nodes = opportunities_df[opportunities_df["opportunity_type"] == "New Engagement (Red Node)"]
service_gaps = opportunities_df[opportunities_df["opportunity_type"] == "Service Gap (Seamless Growth)"]

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Unserved Entities", len(red_nodes))
with col2:
    st.metric("Service Gap Opportunities", len(service_gaps))
with col3:
    st.metric("Unserved Revenue Pool", f"${red_nodes['revenue_k'].sum():.1f}K")
with col4:
    st.metric("Gap Revenue at Stake", f"${service_gaps['revenue_k'].sum():.1f}K")
with col5:
    actions_df = get_crl_actions(crl_name if crl_name else None)
    immediate_actions = len(actions_df[actions_df["urgency"] == "Immediate"]) if not actions_df.empty else 0
    st.metric("Immediate Actions", immediate_actions)

st.divider()

# =============================================================================
# TABS
# =============================================================================
tab_leads, tab_gaps, tab_drilldown, tab_checkin, tab_history = st.tabs([
    "New Leads (Unserved)", "Service Gaps", "Entity Drill-Down", "New Check-In", "Check-In History"
])

# =============================================================================
# TAB 1: UNSERVED ENTITIES (LEADS)
# =============================================================================
with tab_leads:
    st.subheader("Unserved Entities — New Engagement Leads")
    st.markdown("""
    Entities **within existing client families** that we do NOT currently serve.
    The CRL already has a relationship with the family — these are warm-path leads.
    """)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        target_service = st.selectbox(
            "Target Service Line", ["All Services"] + SERVICE_LINES,
        )
    with col_f2:
        cluster_filter = st.selectbox(
            "Client Family", ["All Families"] + red_nodes["cluster_name"].unique().tolist(),
        )

    display_red = red_nodes.copy()
    if cluster_filter != "All Families":
        display_red = display_red[display_red["cluster_name"] == cluster_filter]

    st.dataframe(
        display_red[["entity_name", "entity_type", "cluster_name", "industry", "geography", "revenue_k", "priority_score"]],
        use_container_width=True, hide_index=True,
        column_config={
            "entity_name": "Entity (Unserved)", "entity_type": "Entity Type",
            "cluster_name": "Client Family", "industry": "Industry", "geography": "Geography",
            "revenue_k": st.column_config.NumberColumn("Revenue ($K)", format="$%.1f"),
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
            with st.expander(f"{red_entity['entity_name']} ({red_entity['entity_type']}) — ${red_entity['revenue_k']:.1f}K"):
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
    Served entities missing service lines. Pursuing these creates barriers to exit
    and generates better data for modeling.
    """)

    target_gap_service = st.selectbox(
        "Show entities missing this service:", ["All Gaps"] + SERVICE_LINES, key="gap_service",
    )

    display_gaps = service_gaps.copy()
    if target_gap_service != "All Gaps":
        display_gaps = display_gaps[display_gaps["available_services"].apply(lambda x: target_gap_service in x)]

    st.dataframe(
        display_gaps[["entity_name", "entity_type", "cluster_name", "revenue_k", "available_services", "num_available_services", "priority_score"]],
        use_container_width=True, hide_index=True,
        column_config={
            "entity_name": "Entity", "entity_type": "Type", "cluster_name": "Client Family",
            "revenue_k": st.column_config.NumberColumn("Revenue ($K)", format="$%.1f"),
            "available_services": "Services NOT Engaged (Opportunity)",
            "num_available_services": "Gaps",
            "priority_score": st.column_config.NumberColumn("Priority", format="%.1f"),
        },
    )

    st.markdown("---")
    st.markdown("**Seamless Progress by Service Line:**")

    served = entities_df[entities_df["is_served"]]
    total_served = len(served)
    svc_coverage = {}
    for svc in SERVICE_LINES:
        has_svc = served["services_engaged"].apply(lambda x: svc in x).sum()
        svc_coverage[svc] = has_svc

    svc_df = pd.DataFrame({
        "Service Line": SERVICE_LINES,
        "Entities Served": [svc_coverage[s] for s in SERVICE_LINES],
        "Coverage %": [round(svc_coverage[s] / total_served * 100, 1) if total_served > 0 else 0 for s in SERVICE_LINES],
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
    st.caption("Select an entity to see billing health, service coverage, and position in the client family")

    all_entity_names = entities_df[entities_df["annual_revenue_k"] > 0]["entity_name"].sort_values().tolist()
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
            - **Client Family:** {entity_row['cluster_name']}
            - **Industry:** {entity_row['industry']}
            - **Geography:** {entity_row['geography']}
            - **Revenue:** ${entity_row['annual_revenue_k']:.1f}K
            - **Served:** {'Yes' if entity_row['is_served'] else 'No (Opportunity)'}
            """)

            if entity_row["is_served"]:
                st.markdown(f"""
                - **Health:** {entity_row['health_status']}
                - **Years with CLA:** {entity_row['years_with_cla']}
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
                st.markdown(f"This entity is not currently served but exists within the **{cluster_name}** client family.")
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

# =============================================================================
# TAB 4: NEW CHECK-IN
# =============================================================================
with tab_checkin:
    st.subheader("New Client Check-In")
    st.markdown("""
    Complete this form after each client interaction. This data strengthens client
    family intelligence, improves health tracking, and surfaces new opportunities.
    """)

    with st.form("crl_checkin_form", clear_on_submit=False):
        # SECTION 1
        st.markdown("### 1. Interaction Context")

        col_s1a, col_s1b = st.columns(2)
        with col_s1a:
            cluster_names = [c["cluster_name"] for c in ENTITY_CLUSTERS]
            selected_cluster = st.selectbox(
                "Client Family*", cluster_names,
                help="Which client family does this interaction relate to?",
            )
            cluster_entities = entities_df[entities_df["cluster_name"] == selected_cluster]
            entity_options = cluster_entities["entity_name"].tolist()
            primary_entity = st.selectbox("Primary Entity*", entity_options)

        with col_s1b:
            interaction_type = st.selectbox(
                "Interaction Type*",
                ["In-Person Meeting", "Phone Call", "Video Call", "Email Exchange", "Client Event", "Conference/Seminar", "Informal (Lunch/Coffee)", "Other"],
            )
            interaction_date = st.date_input("Interaction Date*", value=date.today(), max_value=date.today())
            form_crl_name = st.selectbox(
                "CRL Name*",
                options=[""] + CRL_NAMES,
                index=([0] + CRL_NAMES).index(crl_name) if crl_name in CRL_NAMES else 0,
            )

        col_d1a, col_d1b = st.columns(2)
        with col_d1a:
            duration_min = st.number_input("Duration (minutes)", min_value=5, max_value=480, value=30, step=5)
        with col_d1b:
            contacts_met = st.text_input("Client Contact(s) Met", placeholder="e.g., John Smith (CFO), Jane Doe (Partner)")

        st.divider()

        # SECTION 2
        st.markdown("### 2. Relationship Discoveries")
        st.caption("Did you learn about NEW entities, partners, or ownership structures?")

        new_entities_discovered = st.text_area(
            "New Entities Mentioned",
            placeholder="e.g., 'Client mentioned a new LLC they formed — Greenfield Properties LLC'",
            height=80,
        )

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            new_entity_types = st.multiselect(
                "Types of New Entities Discovered",
                ["Partnership (1065)", "S-Corp (1120S)", "C-Corp (1120)", "Trust (1041)", "Individual (1040)", "LLC", "Foundation/Non-Profit", "Other"],
            )
        with col_r2:
            new_relationships = st.multiselect(
                "Relationship Types Identified",
                ["Partner of existing entity", "Owner/Shareholder", "Dependent/Beneficiary", "Working Partnership", "Family Connection", "Board/Advisory Role", "Vendor/Client Relationship"],
            )

        ownership_notes = st.text_area(
            "Ownership/Structure Notes",
            placeholder="e.g., 'The 1065 has 5 partners: 3 we don't serve yet.'",
            height=60,
        )

        st.divider()

        # SECTION 3
        st.markdown("### 3. Service Line Discussion")

        col_svc1, col_svc2 = st.columns(2)
        with col_svc1:
            services_discussed = st.multiselect("Service Lines Discussed", SERVICE_LINES)
        with col_svc2:
            services_interest = st.multiselect("Client Expressed Interest In", SERVICE_LINES)

        seamless_opportunity = st.radio(
            "Seamless Opportunity Detected?",
            ["No new opportunity", "Client open to additional services", "Active cross-sell discussion", "Proposal requested"],
            horizontal=True,
        )

        services_notes = st.text_area(
            "Service Discussion Notes",
            placeholder="e.g., 'Client expressed frustration with current tax advisor for their partnership.'",
            height=60,
        )

        st.divider()

        # SECTION 4
        st.markdown("### 4. Health & Satisfaction Signals")

        col_h1, col_h2, col_h3 = st.columns(3)
        with col_h1:
            satisfaction = st.select_slider(
                "Client Satisfaction",
                options=["Very Dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"],
                value="Satisfied",
            )
        with col_h2:
            engagement_temp = st.select_slider(
                "Engagement Temperature",
                options=["Cold", "Cool", "Warm", "Hot"], value="Warm",
            )
        with col_h3:
            payment_status = st.selectbox(
                "Payment Status (if discussed)",
                ["Not Discussed", "Current/No Issues", "Mentioned Delay", "Dispute/Concern", "Payment Received Today"],
            )

        risk_signals = st.multiselect(
            "Risk Signals Detected",
            ["None — relationship healthy", "Client mentioned competing firms",
             "Expressed dissatisfaction with fees", "Delayed response patterns",
             "Key contact leaving the entity", "Business underperforming",
             "Organizational restructuring", "Succession/Transition discussion"],
        )

        follow_up_needed = st.text_area(
            "Follow-Up Actions Required",
            placeholder="e.g., 'Send proposal for tax services by Friday.'",
            height=60,
        )

        st.divider()

        # SECTION 5
        st.markdown("### 5. Data Consent & Authorization")

        consent_checkbox = st.checkbox(
            "Client consents to expanded profile building",
            help="Check if the client authorized us to build a stronger profile.",
        )

        consent_details = st.radio(
            "Consent Scope",
            ["No consent discussion", "Verbal consent only", "Written consent provided", "Client declined expanded profile"],
            horizontal=True,
        )

        if consent_checkbox:
            st.success("Consent recorded. This interaction data will enrich the client family intelligence.")
        else:
            st.info("Building stronger client profiles helps us serve them better.")

        st.divider()

        # SECTION 6
        st.markdown("### 6. Additional Notes")
        general_notes = st.text_area("General Notes / Free Text", height=80)

        submitted = st.form_submit_button("Submit Check-In", type="primary", use_container_width=True)

        if submitted:
            if not form_crl_name:
                st.error("Please select your name.")
            elif not primary_entity:
                st.error("Please select the primary entity.")
            else:
                st.success(f"""
                **Check-in submitted successfully.**

                - **CRL:** {form_crl_name}
                - **Entity:** {primary_entity} ({selected_cluster})
                - **Date:** {interaction_date}
                - **Type:** {interaction_type}
                - **Duration:** {duration_min} min
                - **New Entities Discovered:** {'Yes' if new_entities_discovered else 'None'}
                - **Consent:** {'Granted' if consent_checkbox else 'Not yet'}
                - **Follow-up Required:** {'Yes' if follow_up_needed else 'None'}

                *This data is strengthening the {selected_cluster} client family intelligence.*
                """)
                st.balloons()

# =============================================================================
# TAB 5: CHECK-IN HISTORY
# =============================================================================
with tab_history:
    st.subheader("Recent Check-In History")
    st.caption("View past interactions across the firm")

    col_hf1, col_hf2, col_hf3 = st.columns(3)
    with col_hf1:
        hist_cluster = st.selectbox(
            "Filter by Client Family", ["All Families"] + [c["cluster_name"] for c in ENTITY_CLUSTERS], key="hist_cluster",
        )
    with col_hf2:
        hist_crl = st.selectbox(
            "Filter by CRL", ["All CRLs"] + interactions_df["crl_name"].unique().tolist(), key="hist_crl",
        )
    with col_hf3:
        hist_days = st.slider("Last N days", 7, 180, 90, key="hist_days")

    display_interactions = interactions_df.copy()
    cutoff_date = (datetime.now() - timedelta(days=hist_days)).strftime("%Y-%m-%d")
    display_interactions = display_interactions[display_interactions["interaction_date"] >= cutoff_date]

    if hist_cluster != "All Families":
        display_interactions = display_interactions[display_interactions["cluster_name"] == hist_cluster]
    if hist_crl != "All CRLs":
        display_interactions = display_interactions[display_interactions["crl_name"] == hist_crl]

    st.dataframe(
        display_interactions.sort_values("interaction_date", ascending=False),
        use_container_width=True, hide_index=True,
        column_config={
            "interaction_date": "Date", "entity_name": "Entity", "cluster_name": "Client Family",
            "crl_name": "CRL", "interaction_type": "Type",
            "services_discussed": "Services Discussed", "new_entities_found": "New Entities?",
            "health_signal": "Health Signal", "consent_status": "Consent",
        },
    )

    st.markdown("---")
    st.markdown("**Check-In Frequency Analysis:**")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        total_interactions = len(display_interactions)
        st.metric("Total Check-Ins", total_interactions)
    with col_m2:
        unique_entities = display_interactions["entity_name"].nunique()
        st.metric("Unique Entities Engaged", unique_entities)
    with col_m3:
        if total_interactions > 0 and hist_days > 0:
            freq = total_interactions / (hist_days / 7)
            st.metric("Avg Check-Ins / Week", f"{freq:.1f}")

    st.markdown("**Entities Overdue for Check-In (>45 days):**")
    served_entities = entities_df[entities_df["is_served"]]
    overdue = served_entities[served_entities["days_since_activity"] > 45].sort_values("days_since_activity", ascending=False)

    if not overdue.empty:
        st.dataframe(
            overdue[["entity_name", "cluster_name", "days_since_activity", "health_status", "crl_owner", "services_engaged"]],
            use_container_width=True, hide_index=True,
            column_config={
                "entity_name": "Entity", "cluster_name": "Client Family",
                "days_since_activity": "Days Since Last Activity",
                "health_status": "Health Status", "crl_owner": "CRL Steward",
                "services_engaged": "Services",
            },
        )
    else:
        st.success("All served entities have been contacted within 45 days.")
