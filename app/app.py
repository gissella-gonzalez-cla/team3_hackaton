"""
CLA Shared Client Relationship View
======================================
A Databricks App (Streamlit) serving two core functions:
    1. Stronger upfront data collection from CRL client interactions
    2. Better centralized reporting on client ontologies, health, and opportunity

Built with the "One-Firm" mindset: clients belong to the firm, CRLs are relationship
leads. This enables firmwide visibility into growth, risk, and coordination.
"""

import streamlit as st

st.set_page_config(
    page_title="CLA | Shared Client Relationship View",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="collapsed",
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

    .purpose-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    .badge-collection { background: #C2EAEA; color: #24787A; }
    .badge-reporting { background: #262A40; color: #7DD2D3; }

    .def-header {
        font-weight: 600;
        color: var(--cla-navy);
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }

    /* Override Streamlit's default link color */
    a { color: var(--cla-riptide-shade); }

    /* Sidebar branding */
    [data-testid="stSidebar"] {
        background-color: var(--cla-cloud);
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Sidebar
    st.sidebar.title("CLA Client View")
    st.sidebar.caption("One Firm. Shared Relationships. Better Decisions.")

    if "crl_name" not in st.session_state:
        st.session_state.crl_name = ""

    crl_name = st.sidebar.text_input(
        "CRL (Relationship Lead)",
        value=st.session_state.crl_name,
        placeholder="e.g., Rypina, Katarzyna",
    )
    st.session_state.crl_name = crl_name

    st.sidebar.divider()
    st.sidebar.markdown("**Platform Purpose**")
    st.sidebar.markdown("""
    - **Reporting** — Firmwide client ontology, health, risk
    - **Collection** — Structured meeting data from CRL interactions
    """)
    st.sidebar.divider()
    st.sidebar.markdown("**Quick Pulse**")
    st.sidebar.metric("Firm Clients (Active)", "312")
    st.sidebar.metric("Open Opportunities", "47")
    st.sidebar.metric("Meetings This Week", "23")

    # --- Hero Section ---
    st.markdown("""
    <div class="hero-card">
        <h2>CLA Shared Client Relationship View</h2>
        <p>
            A unified, trusted view of client relationships across the firm — enabling smarter growth, 
            proactive risk awareness, and coordinated decision-making. Built on the <strong>One-Firm</strong> 
            principle: every client is a firm client, and every CRL is a steward of the relationship.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Dual Purpose Banner ---
    st.markdown("### This platform serves two core functions:")
    col_purpose1, col_purpose2 = st.columns(2)
    with col_purpose1:
        st.markdown("""
        <span class="purpose-badge badge-reporting">CENTRALIZED REPORTING</span>
        
        **Firmwide client ontology visualization** — aggregated views of health, risk, 
        and opportunity stratified by geography, service line, and industry. Leaders 
        see the full relationship network, not just their slice.
        """, unsafe_allow_html=True)
    with col_purpose2:
        st.markdown("""
        <span class="purpose-badge badge-collection">DATA COLLECTION</span>
        
        **Structured CRL check-in workflow** — front-end guardrails that ensure 
        consistent, high-quality data capture during every client interaction. 
        Like a doctor's intake form — the right fields, every time.
        """, unsafe_allow_html=True)

    st.divider()

    # --- Module Cards ---
    st.markdown("### Modules")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="module-card" style="background: #2E334E;">
            <h3>One-Firm View</h3>
            <p>Firmwide entity ontology — node graph showing served vs. unserved entities, 
            cluster health, and seamless analysis. See all entities as firm assets.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="module-card" style="background: #39A5A7;">
            <h3>Opportunities</h3>
            <p>Unserved entities and service gaps. Drill into specific entities, 
            see their position in the ontology, and track billing health for seamless growth.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="module-card" style="background: #24787A;">
            <h3>CRL Check-In</h3>
            <p>Structured intake form — collect entity relationships, ownership structures, 
            service discussions, health signals, and consent. Better data = stronger ontologies.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- Key Definitions ---
    st.markdown("### Key Definitions")
    st.markdown("These four concepts drive everything in this platform:")

    col_def1, col_def2 = st.columns(2)
    with col_def1:
        st.markdown("""
        <p class="def-header">Ontology</p>
        """, unsafe_allow_html=True)
        st.markdown("""
        The web of complex relationships between client entities. A 1065 partnership 
        with 5 partners, a working partnership with another 1065 — the ontology maps 
        these connections as nodes and edges. **Riptide nodes** = entities we serve. 
        **Scarlett nodes** = entities we don't (opportunities). Partners, trusts, corps, 
        and individuals all interconnect.
        """)
        st.markdown("---")
        st.markdown("""
        <p class="def-header">Opportunities</p>
        """, unsafe_allow_html=True)
        st.markdown("""
        Two types: (1) **Unserved entities** — nodes in the ontology we haven't engaged yet, 
        and (2) **Service gaps** — clients we serve but with missing service lines 
        (Assurance, Tax, BizOps, Digital). Both represent revenue we should pursue.
        """)

    with col_def2:
        st.markdown("""
        <p class="def-header">Health</p>
        """, unsafe_allow_html=True)
        st.markdown("""
        Based on our **90-day AR policy**:
        - **Healthy** — Payment or check-in within 30 days
        - **Strained** — 30-59 days of no check-ins or payments
        - **Poor** — 60+ days overdue. Relationship deteriorating.
        """)
        st.markdown("---")
        st.markdown("""
        <p class="def-header">Seamless</p>
        """, unsafe_allow_html=True)
        st.markdown("""
        When we provide bundled services (e.g., Assurance + Tax) to the same client. 
        We pursue seamless growth because it: (1) increases revenue extraction, and 
        (2) increases client retention through higher barriers to exit. A client with 
        3+ service lines is deeply embedded and unlikely to leave.
        """)

    st.divider()

    # --- The "Why" ---
    st.markdown("### Why This Matters")
    st.markdown("""
    > *"What do we know about this client relationship network, and what should we do next?"*
    
    Today, relationship context is **fragmented** across CRM, engagement, financial, and operational 
    systems. Entity relationships aren't consistently mapped. Unserved nodes are invisible. Seamless 
    growth stalls because no one sees the full picture.
    
    This platform brings entity ontologies, health signals, and opportunity data into **one shared view** — 
    so leaders can shift from reactive updates to **proactive, coordinated growth**.
    """)

    col_w1, col_w2, col_w3 = st.columns(3)
    with col_w1:
        st.markdown("**Entity Ontology**")
        st.markdown("Node mapping, partnership structures, ownership webs, connected entities across clusters")
    with col_w2:
        st.markdown("**Health & AR Signals**")
        st.markdown("90-day AR policy compliance, check-in recency, billing trends, risk escalation")
    with col_w3:
        st.markdown("**Seamless Growth**")
        st.markdown("Service bundling progress, cross-sell gaps, retention barriers, revenue extraction per entity")


if __name__ == "__main__":
    main()
