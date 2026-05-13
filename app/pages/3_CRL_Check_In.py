"""
Client Relationship Check-In — Structured Data Collection
=========================================================
Designed to collect structured data from client interactions to
generate stronger ontologies and better firmwide intelligence.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from utils.sample_data import (
    get_all_entities, get_interaction_history, SERVICE_LINES, ENTITY_CLUSTERS,
)

st.set_page_config(page_title="Client Relationship Check-In", page_icon="C", layout="wide")

st.title("Client Relationship Check-In")
st.caption("Structured intake form — collect better data, build stronger ontologies.")

entities_df = get_all_entities()
interactions_df = get_interaction_history()

# =============================================================================
# TABS
# =============================================================================
tab_checkin, tab_history = st.tabs(["New Check-In", "Check-In History"])

# =============================================================================
# TAB 1: NEW CHECK-IN FORM
# =============================================================================
with tab_checkin:
    st.subheader("New Client Check-In")
    st.markdown("""
    Complete this form after each client interaction. This data strengthens our 
    entity ontologies, improves health tracking, and surfaces new opportunities.
    
    > *Think of this like a medical chart — structured, consistent, building over time.*
    """)

    with st.form("crl_checkin_form", clear_on_submit=False):
        # SECTION 1
        st.markdown("### 1. Interaction Context")
        st.caption("Who did you engage with and why?")

        col_s1a, col_s1b = st.columns(2)
        with col_s1a:
            cluster_names = [c["cluster_name"] for c in ENTITY_CLUSTERS]
            selected_cluster = st.selectbox(
                "Client Cluster*", cluster_names,
                help="Which client cluster does this interaction relate to?",
            )
            cluster_entities = entities_df[entities_df["cluster_name"] == selected_cluster]
            entity_options = cluster_entities["entity_name"].tolist()
            primary_entity = st.selectbox(
                "Primary Entity*", entity_options,
                help="Which entity was the primary focus of this interaction?",
            )

        with col_s1b:
            interaction_type = st.selectbox(
                "Interaction Type*",
                ["In-Person Meeting", "Phone Call", "Video Call", "Email Exchange", "Client Event", "Conference/Seminar", "Informal (Lunch/Coffee)", "Other"],
            )
            interaction_date = st.date_input("Interaction Date*", value=date.today(), max_value=date.today())
            crl_name = st.text_input("CRL Name*", placeholder="e.g., Rypina, Katarzyna")

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            duration_min = st.number_input("Duration (minutes)", min_value=5, max_value=480, value=30, step=5)
        with col_d2:
            contacts_met = st.text_input("Client Contact(s) Met", placeholder="e.g., John Smith (CFO), Jane Doe (Partner)")

        st.divider()

        # SECTION 2
        st.markdown("### 2. Relationship Discoveries")
        st.caption("Did you learn about NEW entities, partners, or ownership structures?")
        st.markdown("""
        > *This is how we grow the ontology. Every new entity or relationship you discover 
        > helps us see the full picture and find new opportunities.*
        """)

        new_entities_discovered = st.text_area(
            "New Entities Mentioned",
            placeholder="e.g., 'Client mentioned a new LLC they formed for their rental properties — Greenfield Properties LLC'\n'Partner mentioned her husband also runs a consulting firm — Apex Advisory Group'",
            height=100,
            help="Any new businesses, partnerships, trusts, or individuals you learned about",
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
            placeholder="e.g., 'The 1065 has 5 partners: 3 we don't serve yet. John holds 40%, Mary holds 30%, remaining three hold 10% each.'",
            height=80,
        )

        st.divider()

        # SECTION 3
        st.markdown("### 3. Service Line Discussion")
        st.caption("What services were discussed? Where are expansion opportunities?")

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
            placeholder="e.g., 'Client expressed frustration with current tax advisor for their partnership. May be open to switching.'",
            height=80,
        )

        st.divider()

        # SECTION 4
        st.markdown("### 4. Health & Satisfaction Signals")
        st.caption("How is the relationship? Any concerns?")

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
            placeholder="e.g., 'Send proposal for tax services by Friday. Schedule intro meeting with partner Mary.'",
            height=80,
        )

        st.divider()

        # SECTION 5
        st.markdown("### 5. Data Consent & Authorization")
        st.caption("Stronger profiles require consent. Did the client authorize expanded data collection?")

        consent_checkbox = st.checkbox(
            "Client consents to expanded profile building",
            help="Check if the client verbally or in writing authorized us to build a stronger profile including entity relationships, ownership structures, and affiliated entities.",
        )

        consent_details = st.radio(
            "Consent Scope",
            ["No consent discussion", "Verbal consent only", "Written consent provided", "Client declined expanded profile"],
            horizontal=True,
        )

        if consent_checkbox:
            st.success("Consent recorded. This interaction data will be used to enrich the client ontology.")
        else:
            st.info("Building stronger client profiles helps us serve them better and find related opportunities.")

        st.divider()

        # SECTION 6
        st.markdown("### 6. Additional Notes")

        general_notes = st.text_area(
            "General Notes / Free Text",
            placeholder="Anything else noteworthy from this interaction...",
            height=100,
        )

        st.markdown("#### Voice Recording (Coming Soon)")
        st.info("Future feature: Record a voice memo that will be transcribed and parsed into structured ontology data using AI.")
        voice_file = st.file_uploader("Upload Voice Memo (optional)", type=["mp3", "wav", "m4a"])

        st.divider()

        # SUBMIT
        submitted = st.form_submit_button("Submit Check-In", type="primary", use_container_width=True)

        if submitted:
            if not crl_name:
                st.error("Please enter your name.")
            elif not primary_entity:
                st.error("Please select the primary entity.")
            else:
                st.success(f"""
                **Check-in submitted successfully.**
                
                - **CRL:** {crl_name}
                - **Entity:** {primary_entity} ({selected_cluster})
                - **Date:** {interaction_date}
                - **Type:** {interaction_type}
                - **Duration:** {duration_min} min
                - **New Entities Discovered:** {'Yes' if new_entities_discovered else 'None'}
                - **Consent:** {'Granted' if consent_checkbox else 'Not yet'}
                - **Follow-up Required:** {'Yes' if follow_up_needed else 'None'}
                
                *This data is strengthening the {selected_cluster} ontology and improving firmwide intelligence.*
                """)
                st.balloons()


# =============================================================================
# TAB 2: CHECK-IN HISTORY
# =============================================================================
with tab_history:
    st.subheader("Recent Check-In History")
    st.caption("View past interactions across the firm")

    col_hf1, col_hf2, col_hf3 = st.columns(3)
    with col_hf1:
        hist_cluster = st.selectbox(
            "Filter by Cluster", ["All Clusters"] + [c["cluster_name"] for c in ENTITY_CLUSTERS], key="hist_cluster",
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

    if hist_cluster != "All Clusters":
        display_interactions = display_interactions[display_interactions["cluster_name"] == hist_cluster]
    if hist_crl != "All CRLs":
        display_interactions = display_interactions[display_interactions["crl_name"] == hist_crl]

    st.dataframe(
        display_interactions.sort_values("interaction_date", ascending=False),
        use_container_width=True, hide_index=True,
        column_config={
            "interaction_date": "Date", "entity_name": "Entity", "cluster_name": "Cluster",
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
                "entity_name": "Entity", "cluster_name": "Cluster",
                "days_since_activity": "Days Since Last Activity",
                "health_status": "Health Status", "crl_owner": "CRL Steward",
                "services_engaged": "Services",
            },
        )
    else:
        st.success("All served entities have been contacted within 45 days.")
