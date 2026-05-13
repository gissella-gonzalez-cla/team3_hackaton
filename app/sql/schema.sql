-- =============================================================================
-- CLA Shared Client Relationship View — Unity Catalog Schema
-- =============================================================================
-- Deploy in Databricks Unity Catalog to support the application.
-- Catalog: crl_intelligence | Schema: prod
-- Aligned to DORGCON Hackathon requirements: shared view, relationship signals,
-- health/risk/opportunity indicators, and CRL data collection.
-- =============================================================================

-- Client Ontology Master Table (The "One-Firm" View)
CREATE TABLE IF NOT EXISTS crl_intelligence.prod.client_ontology (
    client_id STRING NOT NULL,
    client_name STRING NOT NULL,
    parent_entity_id STRING,
    parent_entity_name STRING,
    industry STRING,
    sub_industry STRING,
    geography STRING,
    has_multi_geo_presence BOOLEAN DEFAULT FALSE,
    primary_service STRING,
    services_engaged ARRAY<STRING>,
    services_not_engaged ARRAY<STRING>,
    annual_revenue_mm DECIMAL(10, 2),
    revenue_tier STRING,
    relationship_health_score DECIMAL(3, 1),
    num_services_engaged INT,
    total_service_lines INT DEFAULT 9,
    years_as_client INT,
    crl_owner STRING,
    last_interaction_date DATE,
    consent_status STRING DEFAULT 'Not Requested',
    risk_flag BOOLEAN DEFAULT FALSE,
    employee_count INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT current_timestamp(),
    updated_at TIMESTAMP DEFAULT current_timestamp()
)
USING DELTA
COMMENT 'One-Firm client ontology: every client is a firm asset with relationship signals and service coverage';

-- Parent-Child Entity Relationships
CREATE TABLE IF NOT EXISTS crl_intelligence.prod.entity_relationships (
    relationship_id STRING DEFAULT uuid(),
    source_client_id STRING NOT NULL,
    source_client_name STRING NOT NULL,
    target_client_id STRING NOT NULL,
    target_client_name STRING NOT NULL,
    relationship_type STRING NOT NULL COMMENT 'parent_child, sibling, shared_geography, shared_industry, shared_crl, ownership',
    relationship_weight INT DEFAULT 1,
    validated BOOLEAN DEFAULT FALSE,
    validated_by STRING,
    validated_date DATE,
    created_at TIMESTAMP DEFAULT current_timestamp()
)
USING DELTA
COMMENT 'Relationship edges between client entities: parent/child, ownership, shared leadership, geographic overlap, industry alignment';

-- CRL Check-In Entries (Structured Data Collection)
CREATE TABLE IF NOT EXISTS crl_intelligence.prod.crl_checkins (
    entry_id STRING DEFAULT uuid(),
    recorded_at TIMESTAMP DEFAULT current_timestamp(),
    crl_name STRING NOT NULL,
    client_name STRING NOT NULL,
    meeting_date DATE NOT NULL,
    meeting_type STRING,
    client_contacts STRING,
    seniority_levels ARRAY<STRING>,
    -- Relationship Vitals
    satisfaction_score INT,
    engagement_quality INT,
    responsiveness_score INT,
    trust_level INT,
    overall_sentiment STRING,
    -- Service & Opportunity
    services_discussed ARRAY<STRING>,
    expansion_services ARRAY<STRING>,
    expansion_likelihood INT,
    revenue_potential STRING,
    opportunity_timeline STRING,
    -- Risk & Retention
    retention_risk STRING,
    competitor_activity STRING,
    compliance_flags STRING,
    risk_notes STRING,
    -- Notes & Intelligence
    key_takeaways STRING,
    action_items STRING,
    competitive_intel STRING,
    industry_signals STRING,
    -- Consent
    consent_granted BOOLEAN DEFAULT FALSE,
    consent_sources ARRAY<STRING>,
    consent_years ARRAY<STRING>,
    consent_method STRING,
    consent_contact STRING,
    -- Flags
    flag_opportunity BOOLEAN DEFAULT FALSE,
    flag_risk BOOLEAN DEFAULT FALSE,
    flag_escalation BOOLEAN DEFAULT FALSE,
    flag_followup BOOLEAN DEFAULT FALSE,
    followup_date DATE,
    -- Attestation
    crl_attestation BOOLEAN NOT NULL
)
USING DELTA
COMMENT 'Structured CRL check-in data captured during client interactions with front-end guardrails';

-- Billing History (Client Health Trending)
CREATE TABLE IF NOT EXISTS crl_intelligence.prod.billing_history (
    billing_id STRING DEFAULT uuid(),
    client_name STRING NOT NULL,
    period STRING NOT NULL COMMENT 'Format: YYYY-QN (e.g., 2025-Q3)',
    service_line STRING NOT NULL,
    billed_amount DECIMAL(12, 2),
    collected_amount DECIMAL(12, 2),
    outstanding_amount DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT current_timestamp()
)
USING DELTA
COMMENT 'Quarterly billing history by client and service line for health trending';

-- Consent Records (Audit Trail)
CREATE TABLE IF NOT EXISTS crl_intelligence.prod.consent_records (
    consent_id STRING DEFAULT uuid(),
    recorded_at TIMESTAMP DEFAULT current_timestamp(),
    client_name STRING NOT NULL,
    consent_granted BOOLEAN NOT NULL,
    consent_date DATE NOT NULL,
    data_sources ARRAY<STRING>,
    years_authorized ARRAY<STRING>,
    consent_method STRING,
    client_contact STRING,
    prior_firm_involved BOOLEAN DEFAULT FALSE,
    prior_firm_name STRING,
    restrictions STRING,
    expiry_date DATE,
    crl_name STRING,
    crl_attestation BOOLEAN NOT NULL
)
USING DELTA
COMMENT 'Consent audit trail for prior financial reporting data ingestion authorization';

-- Interaction History (Aggregated)
CREATE TABLE IF NOT EXISTS crl_intelligence.prod.interaction_history (
    interaction_id STRING DEFAULT uuid(),
    client_name STRING NOT NULL,
    interaction_date TIMESTAMP NOT NULL,
    interaction_type STRING,
    crl_name STRING,
    satisfaction_score INT,
    duration_minutes INT
)
USING DELTA
COMMENT 'Aggregated interaction history for trend analysis and CRL activity tracking';

-- =============================================================================
-- Views for the Shared Client Relationship View
-- =============================================================================

-- One-Firm Portfolio Summary
CREATE OR REPLACE VIEW crl_intelligence.prod.v_one_firm_summary AS
SELECT
    geography,
    industry,
    primary_service,
    COUNT(*) as client_count,
    SUM(annual_revenue_mm) as total_revenue_mm,
    AVG(relationship_health_score) as avg_health,
    SUM(CASE WHEN relationship_health_score < 5 THEN 1 ELSE 0 END) as at_risk_count,
    AVG(num_services_engaged) as avg_services,
    SUM(CASE WHEN consent_status = 'Granted' THEN 1 ELSE 0 END) as consented_count
FROM crl_intelligence.prod.client_ontology
WHERE is_active = TRUE
GROUP BY geography, industry, primary_service;

-- Opportunity Pipeline
CREATE OR REPLACE VIEW crl_intelligence.prod.v_opportunity_pipeline AS
SELECT
    co.client_name,
    co.industry,
    co.geography,
    co.annual_revenue_mm,
    co.num_services_engaged,
    co.total_service_lines - co.num_services_engaged as service_gap,
    co.relationship_health_score,
    co.services_not_engaged,
    co.crl_owner,
    -- Opportunity score
    (co.relationship_health_score * 0.3 
     + (co.total_service_lines - co.num_services_engaged) * 2.0
     + (co.annual_revenue_mm / 2000) * 3
     + co.years_as_client * 0.1) as opportunity_score
FROM crl_intelligence.prod.client_ontology co
WHERE co.is_active = TRUE
    AND co.num_services_engaged < co.total_service_lines
    AND co.relationship_health_score >= 5
ORDER BY opportunity_score DESC;

-- CRL Stewardship Performance
CREATE OR REPLACE VIEW crl_intelligence.prod.v_crl_stewardship AS
SELECT
    crl_owner,
    COUNT(*) as portfolio_size,
    SUM(annual_revenue_mm) as total_revenue_mm,
    AVG(relationship_health_score) as avg_health_score,
    SUM(CASE WHEN relationship_health_score < 5 THEN 1 ELSE 0 END) as at_risk_count,
    AVG(num_services_engaged) as avg_services,
    COUNT(DISTINCT industry) as industry_spread,
    COUNT(DISTINCT geography) as geo_spread
FROM crl_intelligence.prod.client_ontology
WHERE is_active = TRUE
GROUP BY crl_owner;

-- Parent Entity Aggregation
CREATE OR REPLACE VIEW crl_intelligence.prod.v_parent_entities AS
SELECT
    parent_entity_name,
    COUNT(*) as child_entities,
    SUM(annual_revenue_mm) as combined_revenue_mm,
    AVG(relationship_health_score) as avg_health,
    SUM(num_services_engaged) as total_engagements,
    COLLECT_SET(geography) as geographies,
    COLLECT_SET(industry) as industries
FROM crl_intelligence.prod.client_ontology
WHERE parent_entity_name IS NOT NULL AND is_active = TRUE
GROUP BY parent_entity_name;

-- Client Health Trends (from billing)
CREATE OR REPLACE VIEW crl_intelligence.prod.v_client_billing_health AS
SELECT
    b.client_name,
    b.period,
    SUM(b.billed_amount) as total_billed,
    COUNT(DISTINCT b.service_line) as active_service_lines,
    co.relationship_health_score,
    co.crl_owner
FROM crl_intelligence.prod.billing_history b
JOIN crl_intelligence.prod.client_ontology co ON b.client_name = co.client_name
GROUP BY b.client_name, b.period, co.relationship_health_score, co.crl_owner;
