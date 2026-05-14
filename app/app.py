"""
CLA One Firm View
==================
A Databricks App (Streamlit) providing firmwide client relationship
intelligence. CRLs use the sidebar to manage their profile, and the
main pages to explore client families and manage opportunities.
"""

import streamlit as st
from utils.sample_data import (
    get_all_entities, get_crl_actions, CRL_NAMES,
)

st.set_page_config(
    page_title="CLA | One Firm View",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CLA Brand CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --cla-navy: #2E334E;
        --cla-riptide: #7DD2D3;
        --cla-celadon: #E2E868;
        --cla-saffron: #FBC55A;
        --cla-scarlett: #EE5340;
        --cla-charcoal: #25282A;
        --cla-smoke: #ABAEAB;
        --cla-cloud: #F7F7F6;
        --cla-riptide-shade: #39A5A7;
        --cla-navy-light: #262A40;
    }

    .stApp {
        font-family: 'Inter', Calibri, Arial, sans-serif;
    }

    @media (max-width: 768px) {
        .block-container { padding: 1rem 0.5rem; }
    }

    .hero-card {
        background: linear-gradient(135deg, var(--cla-navy) 0%, var(--cla-navy-light) 100%);
        border-radius: 12px;
        padding: 2.5rem;
        color: white;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero-card::before {
        content: '';
        position: absolute;
        top: -30px;
        right: -30px;
        width: 200px;
        height: 200px;
        background: var(--cla-riptide);
        opacity: 0.15;
        border-radius: 50%;
    }
    .hero-card h2 { margin: 0 0 0.75rem 0; font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }
    .hero-card p { margin: 0; opacity: 0.9; font-size: 0.95rem; line-height: 1.6; }

    .module-card {
        border-radius: 8px;
        padding: 1.5rem;
        color: white;
        margin-bottom: 1rem;
        min-height: 150px;
        border: none;
    }
    .module-card h3 { margin: 0 0 0.5rem 0; font-size: 1.1rem; font-weight: 600; }
    .module-card p { margin: 0; opacity: 0.9; font-size: 0.88rem; line-height: 1.5; }

    .def-header {
        font-weight: 600;
        color: var(--cla-navy);
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }

    a { color: var(--cla-riptide-shade); }

    [data-testid="stSidebar"] {
        background-color: var(--cla-cloud);
    }
</style>
""", unsafe_allow_html=True)


def _build_sidebar():
    """Build the CRL profile sidebar with Quick Pulse metrics."""
    st.sidebar.title("CRL Profile")

    if "crl_name" not in st.session_state:
        st.session_state.crl_name = ""

    crl_name = st.sidebar.selectbox(
        "Select Your Name",
        options=[""] + CRL_NAMES,
        index=0,
        format_func=lambda x: "Choose a CRL..." if x == "" else x,
    )
    st.session_state.crl_name = crl_name

    entities_df = get_all_entities()
    total_firm_clients = len(entities_df[entities_df["is_served"]])

    if crl_name:
        # CRL-specific metrics
        crl_clients = entities_df[
            (entities_df["crl_owner"] == crl_name) & (entities_df["is_served"])
        ]
        crl_client_count = len(crl_clients)
        pct_of_firm = round(crl_client_count / total_firm_clients * 100, 1) if total_firm_clients > 0 else 0
        healthy_count = len(crl_clients[crl_clients["health_status"] == "Healthy"])

        st.sidebar.divider()
        st.sidebar.markdown("**Quick Pulse**")
        st.sidebar.metric("% of Firm Clients", f"{pct_of_firm}%")
        st.sidebar.metric("My Clients", crl_client_count)
        st.sidebar.metric("Healthy Clients", healthy_count)

        # Action counts
        actions_df = get_crl_actions(crl_name)
        if not actions_df.empty:
            immediate = len(actions_df[actions_df["urgency"] == "Immediate"])
            this_week = len(actions_df[actions_df["urgency"] == "This Week"])
            upcoming = len(actions_df[actions_df["urgency"] == "Upcoming"])
        else:
            immediate = this_week = upcoming = 0

        st.sidebar.divider()
        st.sidebar.markdown("**Actions**")
        st.sidebar.metric("Immediate", immediate, help="Check-ins/meetings due today or tomorrow")
        st.sidebar.metric("This Week", this_week, help="Actions due within the next 7 days")
        st.sidebar.metric("Upcoming (30 days)", upcoming, help="Actions due within the next month")
    else:
        st.sidebar.divider()
        st.sidebar.info("Select your name to see your Quick Pulse.")


def main():
    _build_sidebar()

    # --- Hero Section ---
    st.markdown("""
    <div class="hero-card">
        <h2>One Firm View</h2>
        <p>
            A unified, trusted view of client relationships across the firm — enabling smarter growth,
            proactive risk awareness, and coordinated decision-making. Built on the <strong>One-Firm</strong>
            principle: every client is a firm client, and every CRL is a steward of the relationship.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Module Cards ---
    st.markdown("### Navigate")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="module-card" style="background: #2E334E;">
            <h3>Client Family Explorer</h3>
            <p>Firmwide client family view — node graph showing served vs. unserved entities,
            family health, and seamless analysis. Select a client family to explore its entity web,
            then drill into individual nodes for details.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="module-card" style="background: #39A5A7;">
            <h3>Opportunity Manager</h3>
            <p>Manage your leads and opportunities from a dashboard summary view.
            Drill into unserved entities and service gaps. Track client events and check-ins
            to strengthen relationships and drive seamless growth.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- Key Definitions ---
    st.markdown("### Key Definitions")
    col_def1, col_def2 = st.columns(2)
    with col_def1:
        st.markdown('<p class="def-header">Client Family</p>', unsafe_allow_html=True)
        st.markdown("""
        The web of complex relationships between client entities. A 1065 partnership
        with 5 partners, a working partnership with another 1065 — the client family maps
        these connections as nodes and edges. **Riptide nodes** = entities we serve.
        **Scarlett nodes** = entities we don't (opportunities).
        """)
        st.markdown("---")
        st.markdown('<p class="def-header">Opportunities</p>', unsafe_allow_html=True)
        st.markdown("""
        Two types: (1) **Unserved entities** — nodes in the family we haven't engaged yet,
        and (2) **Service gaps** — clients we serve but with missing service lines.
        """)

    with col_def2:
        st.markdown('<p class="def-header">Health</p>', unsafe_allow_html=True)
        st.markdown("""
        Based on **AR recency + client tenure**:
        - **Healthy** — Recent activity; long-term clients earn grace for loyalty
        - **Strained** — Activity gap growing; needs attention
        - **Poor** — Significant gap. Relationship at risk.

        Clients with multi-year tenure and recurring contracts maintain stability.
        """)
        st.markdown("---")
        st.markdown('<p class="def-header">Seamless</p>', unsafe_allow_html=True)
        st.markdown("""
        Bundled services (e.g., Assurance + Tax) to the same client. Increases
        revenue extraction and retention through higher barriers to exit.
        """)


if __name__ == "__main__":
    main()
