"""
Databricks Connector
=====================
Utility for connecting to Databricks Unity Catalog and executing queries.
In production, this replaces the sample_data module with live queries.

Usage:
    from utils.db_connector import DatabricksConnector
    db = DatabricksConnector()
    df = db.query("SELECT * FROM catalog.schema.client_ontology")
"""

import os
from functools import lru_cache


class DatabricksConnector:
    """
    Databricks SQL connector for the CLA Shared Client Relationship View.

    In Databricks Apps, authentication is handled automatically via the
    app's service principal. Environment variables are injected by the runtime.
    """

    def __init__(self):
        self.host = os.getenv("DATABRICKS_HOST", "")
        self.warehouse_id = os.getenv("DATABRICKS_WAREHOUSE_ID", "")
        self.catalog = os.getenv("DATABRICKS_CATALOG", "crl_intelligence")
        self.schema = os.getenv("DATABRICKS_SCHEMA", "prod")

    def get_connection(self):
        """Get a Databricks SQL connection."""
        try:
            from databricks import sql

            return sql.connect(
                server_hostname=self.host,
                http_path=f"/sql/1.0/warehouses/{self.warehouse_id}",
                access_token=os.getenv("DATABRICKS_TOKEN", ""),
            )
        except ImportError:
            raise ImportError(
                "databricks-sql-connector not installed. "
                "Run: pip install databricks-sql-connector"
            )

    def query(self, sql_query: str, params=None):
        """Execute a SQL query and return results as a pandas DataFrame."""
        import pandas as pd

        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql_query, params)
            else:
                cursor.execute(sql_query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return pd.DataFrame(rows, columns=columns)
        finally:
            cursor.close()
            conn.close()

    def get_clients(self):
        """Fetch One-Firm client ontology."""
        return self.query(f"""
            SELECT * FROM {self.catalog}.{self.schema}.client_ontology
            WHERE is_active = TRUE
            ORDER BY annual_revenue_mm DESC
        """)

    def get_relationship_edges(self):
        """Fetch relationship edges for network graph."""
        return self.query(f"""
            SELECT * FROM {self.catalog}.{self.schema}.entity_relationships
        """)

    def get_billing_history(self, client_name=None):
        """Fetch billing history for health trending."""
        query = f"SELECT * FROM {self.catalog}.{self.schema}.billing_history"
        if client_name:
            query += f" WHERE client_name = '{client_name}'"
        query += " ORDER BY period DESC"
        return self.query(query)

    def get_opportunities(self):
        """Fetch opportunity pipeline view."""
        return self.query(f"""
            SELECT * FROM {self.catalog}.{self.schema}.v_opportunity_pipeline
        """)

    def save_checkin(self, entry: dict):
        """Save a CRL check-in entry."""
        self.query(f"""
            INSERT INTO {self.catalog}.{self.schema}.crl_checkins
            VALUES (
                uuid(), current_timestamp(),
                :crl_name, :client_name, :meeting_date, :meeting_type,
                :client_contacts, :seniority_levels,
                :satisfaction_score, :engagement_quality,
                :responsiveness_score, :trust_level, :overall_sentiment,
                :services_discussed, :expansion_services,
                :expansion_likelihood, :revenue_potential, :opportunity_timeline,
                :retention_risk, :competitor_activity, :compliance_flags, :risk_notes,
                :key_takeaways, :action_items, :competitive_intel, :industry_signals,
                :consent_granted, :consent_sources, :consent_years,
                :consent_method, :consent_contact,
                :flag_opportunity, :flag_risk, :flag_escalation, :flag_followup,
                :followup_date, :crl_attestation
            )
        """, entry)

    def save_consent_record(self, record: dict):
        """Save a consent record to the audit trail."""
        self.query(f"""
            INSERT INTO {self.catalog}.{self.schema}.consent_records
            VALUES (
                uuid(), current_timestamp(),
                :client_name, :consent_granted, :consent_date,
                :data_sources, :years_authorized, :consent_method,
                :client_contact, :prior_firm_involved, :prior_firm_name,
                :restrictions, :expiry_date, :crl_name, :crl_attestation
            )
        """, record)
