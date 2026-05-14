"""CLA Customer Relationship Hub - Thin entrypoint."""

import os
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from data import ENTITIES
from styles import CONTENT_STYLE
from components import sidebar

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    title="CLA | Customer Relationship Hub",
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="current-page", data="my-customers"),
        dcc.Store(id="selected-entity", data=ENTITIES[0]["id"]),
        dcc.Store(id="roadmap-store", data=[], storage_type="local"),
        html.Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"),
        sidebar,
        html.Div(id="page-content", style=CONTENT_STYLE),
    ]
)

# Import callbacks AFTER app and layout are created so @callback decorators register
import callbacks  # noqa: E402, F401

if __name__ == "__main__":
    port = int(os.environ.get("DATABRICKS_APP_PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
