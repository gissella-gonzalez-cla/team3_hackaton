# Databricks notebook source
# DBTITLE 1,Read existing app.py and extract sections
# Read the existing monolithic app.py
import os

BASE_DIR = "/Workspace/Users/cody.kreiner@claconnect.com/hackathon-team-3"

with open(os.path.join(BASE_DIR, "app.py"), "r") as f:
    original_source = f.read()

lines = original_source.split("\n")
print(f"Total lines in app.py: {len(lines)}")
print(f"Total size: {len(original_source)} bytes")

# Find section markers
markers = {}
for i, line in enumerate(lines):
    if line.startswith("# ─── ") or line.startswith("# ───"):
        markers[i] = line.strip()

print("\nSection markers found:")
for line_num, marker in sorted(markers.items()):
    print(f"  Line {line_num + 1}: {marker}")

# COMMAND ----------

# DBTITLE 1,Write data.py - all mock data constants
# Extract mock data section (lines 10-118, 0-indexed: 9-117)
# Also need DISCOVERY_PLAYBOOK, MEETING_AUTOMATION_STEPS, etc. which are in the HELPERS section

# Find where DISCOVERY_PLAYBOOK starts and ends
disc_start = None
disc_end = None
for i, line in enumerate(lines):
    if line.startswith("DISCOVERY_PLAYBOOK"):
        disc_start = i
    elif line.startswith("MEETING_AUTOMATION_STEPS"):
        if disc_start and not disc_end:
            pass  # part of same section
    elif line.startswith("MOBILE_CAPTURE_TIPS"):
        pass
    elif line.startswith("ROADMAP_STAGES"):
        pass

# Find the end of ROADMAP_STAGES
for i, line in enumerate(lines):
    if line.startswith("ROADMAP_STAGES"):
        # Find closing bracket
        for j in range(i, len(lines)):
            if lines[j].strip() == "]":
                disc_end = j
                break
        break

print(f"DISCOVERY_PLAYBOOK etc start at line {disc_start + 1}")
print(f"ROADMAP_STAGES ends at line {disc_end + 1}")

# Build data.py
data_py = '''"""Mock data constants for the CLA Customer Relationship Hub."""

'''

# Add the ENTITIES through OPPORTUNITIES (lines 11-117)
data_section = "\n".join(lines[11:118])  # After the MOCK DATA marker
data_py += data_section + "\n\n"

# Add DISCOVERY_PLAYBOOK through ROADMAP_STAGES
playbook_section = "\n".join(lines[disc_start:disc_end + 1])
data_py += playbook_section + "\n"

with open(os.path.join(BASE_DIR, "data.py"), "w") as f:
    f.write(data_py)

print(f"Written data.py: {len(data_py)} bytes")
print(f"First 200 chars: {data_py[:200]}")
print(f"Last 200 chars: {data_py[-200:]}")


# COMMAND ----------

# DBTITLE 1,Write styles.py - style constants and routing maps
# Styles section: lines 142-180 (0-indexed: 141-179)
# Routing map: lines 128-141 (0-indexed: 127-140)

styles_py = '''"""Style constants and routing maps for the CLA app."""

'''

# Add routing maps (lines 130-140)
routing_section = "\n".join(lines[129:141])
styles_py += routing_section + "\n\n"

# Add styles (lines 143-180)
styles_section = "\n".join(lines[142:180])
styles_py += styles_section + "\n"

with open(os.path.join(BASE_DIR, "styles.py"), "w") as f:
    f.write(styles_py)

print(f"Written styles.py: {len(styles_py)} bytes")
print(styles_py[:500])


# COMMAND ----------

# DBTITLE 1,Write components.py - navigation, helpers, sidebar
# Navigation section: lines 181-259 (0-indexed: 180-258)
# Helpers section: lines 260-487 (0-indexed: 259-486)

components_py = '''"""Navigation, sidebar, and helper components for the CLA app."""

from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from urllib.parse import quote
from data import ENTITIES, CONTACTS, PROJECTS, CONTRACTS, OPPORTUNITIES
from styles import SIDEBAR_STYLE, CARD_STYLE, TAG_COLORS

'''

# Add navigation functions (lines 182-259)
nav_section = "\n".join(lines[181:259])
components_py += nav_section + "\n\n"

# Add helper functions (lines 261-487)
helpers_section = "\n".join(lines[260:487])
components_py += helpers_section + "\n"

with open(os.path.join(BASE_DIR, "components.py"), "w") as f:
    f.write(components_py)

print(f"Written components.py: {len(components_py)} bytes")
print(f"First 400 chars:\n{components_py[:400]}")


# COMMAND ----------

# DBTITLE 1,Write pages.py - all page layout functions
# Pages section: lines 488-1058 (0-indexed: 487-1057)
# Entity map (cytoscape): lines 1059-1372 (0-indexed: 1058-1371) 
# Other pages: lines 1373-1619 (0-indexed: 1372-1618)

pages_py = '''"""Page layout functions for the CLA app."""

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from datetime import datetime
from data import (ENTITIES, CONTACTS, PROJECTS, CONTRACTS, OPPORTUNITIES,
                  DISCOVERY_PLAYBOOK, MEETING_AUTOMATION_STEPS, MOBILE_CAPTURE_TIPS, ROADMAP_STAGES)
from styles import CARD_STYLE, TAG_COLORS
from components import (get_entity, get_entity_contacts, get_entity_projects, get_entity_contracts,
                        get_entity_opportunities, get_related_entities, build_teams_meeting_link,
                        build_mailto_link, build_customer_summary_cards, build_customer_cards, build_nav_items)

'''

# Add pages section (lines 489-1058)
pages_section = "\n".join(lines[488:1058])
pages_py += pages_section + "\n\n"

# Add entity map section (lines 1060-1372)
entity_map_section = "\n".join(lines[1059:1372])
pages_py += entity_map_section + "\n\n"

# Add other pages section (lines 1374-1619)
other_pages_section = "\n".join(lines[1373:1619])
pages_py += other_pages_section + "\n"

with open(os.path.join(BASE_DIR, "pages.py"), "w") as f:
    f.write(pages_py)

print(f"Written pages.py: {len(pages_py)} bytes")
print(f"First 500 chars:\n{pages_py[:500]}")


# COMMAND ----------

# DBTITLE 1,Write callbacks.py - FIXED routing architecture
# Callbacks section: lines 1635-1969 (0-indexed: 1634-1968)
# We need to rewrite the navigate + route_from_url callbacks to fix the circular dependency

# First, let's see what the existing callbacks look like
print("Existing callback section first 20 lines:")
for i in range(1635, 1655):
    print(f"  {i+1}: {lines[i]}")

# Find line numbers of each callback function
callback_starts = []
for i in range(1634, 1969):
    if lines[i].strip().startswith("@callback"):
        callback_starts.append(i)
    elif lines[i].strip().startswith("def ") and i > 0 and any(lines[j].strip().startswith("@callback") for j in range(max(i-15, 1634), i)):
        print(f"  Callback function at line {i+1}: {lines[i].strip()[:60]}")

print(f"\nCallback decorators at lines: {[s+1 for s in callback_starts]}")


# COMMAND ----------

# DBTITLE 1,Write callbacks.py with fixed routing
# Extract remaining callbacks (non-routing ones) from lines after route_from_url
# route_from_url ends around line 1719 (before update_graph_lens at 1722)
# So remaining callbacks: lines 1722-1968

remaining_callbacks = "\n".join(lines[1721:1968])

# Also need the add_roadmap_entry callback - let's check what's between line 1875 and 1947
print("Line 1875-1880:")
for i in range(1874, 1880):
    print(f"  {i+1}: {lines[i]}")

callbacks_py = '''"""Callback definitions for the CLA app - FIXED routing architecture."""

import dash
from dash import callback, Input, Output, State, ALL, ctx, html
import dash_bootstrap_components as dbc
from datetime import datetime
import random
from data import ENTITIES, OPPORTUNITIES, ROADMAP_STAGES
from styles import PAGE_TO_PATH, PATH_TO_PAGE, CARD_STYLE, TAG_COLORS
from components import build_nav_items, get_entity, get_entity_contacts, get_entity_projects, get_entity_contracts
from pages import (my_customers_page, client_detail_page, entity_view_page,
                   opportunities_page, contacts_page, projects_page, contracts_page,
                   build_cytoscape_elements, build_opportunity_cards, _render_roadmap_timeline)


# ─── ROUTING (FIXED - no circular dependency) ────────────────────────────────

@callback(
    Output("url", "pathname"),
    Output("url", "search"),
    Input({"type": "nav-btn", "page": ALL}, "n_clicks"),
    Input({"type": "open-client", "entity": ALL}, "n_clicks"),
    Input({"type": "spotlight-client", "entity": ALL}, "n_clicks"),
    State("current-page", "data"),
    State("selected-entity", "data"),
    prevent_initial_call=True,
)
def navigate(n_clicks, open_client_clicks, spotlight_clicks, current_page, selected_entity):
    """Only updates the URL - does NOT render pages directly."""
    if not ctx.triggered_id:
        return dash.no_update, dash.no_update
    trigger = ctx.triggered_id
    page = current_page
    entity_id = selected_entity
    if isinstance(trigger, dict) and trigger.get("type") == "nav-btn":
        page = trigger["page"]
    elif isinstance(trigger, dict) and trigger.get("type") in ("open-client", "spotlight-client"):
        entity_id = trigger["entity"]
        page = "client-detail"
    path = PAGE_TO_PATH.get(page, "/")
    search = ""
    if page == "client-detail":
        path = "/client"
        search = f"?entity={entity_id}"
    return path, search


@callback(
    Output("page-content", "children"),
    Output("current-page", "data"),
    Output("nav-items", "children"),
    Output("selected-entity", "data"),
    Input("url", "pathname"),
    Input("url", "search"),
    State("selected-entity", "data"),
    prevent_initial_call=False,
)
def render_page(pathname, search, selected_entity):
    """Single source of truth for page rendering based on URL."""
    page = PATH_TO_PAGE.get(pathname or "/", "my-customers")
    entity_id = selected_entity or ENTITIES[0]["id"]
    if page == "client-detail" and search:
        try:
            parts = [p for p in search.lstrip("?").split("&") if "=" in p]
            qs = {k: v for k, v in (x.split("=", 1) for x in parts)}
            entity_id = qs.get("entity", entity_id)
        except Exception:
            pass
    pages = {
        "my-customers": my_customers_page,
        "client-detail": lambda: client_detail_page(entity_id),
        "entity": entity_view_page,
        "opportunities": opportunities_page,
        "contacts": contacts_page,
        "projects": projects_page,
        "contracts": contracts_page,
    }
    nav_items = build_nav_items(page)
    return pages.get(page, my_customers_page)(), page, nav_items, entity_id


# ─── REMAINING CALLBACKS ─────────────────────────────────────────────────────

'''

# Add remaining callbacks (update_graph_lens through filter_opportunities)
# These are lines 1722-1968 (the non-routing callbacks)
callbacks_py += remaining_callbacks + "\n"

# Fix: refresh_roadmap_timeline uses allow_duplicate but needs prevent_initial_call=True
callbacks_py = callbacks_py.replace(
    '''Output("roadmap-timeline", "children", allow_duplicate=True),
    Input("roadmap-store", "data"),
    State("selected-entity", "data"),
    prevent_initial_call=False,''',
    '''Output("roadmap-timeline", "children", allow_duplicate=True),
    Input("roadmap-store", "data"),
    State("selected-entity", "data"),
    prevent_initial_call=True,'''
)

with open(os.path.join(BASE_DIR, "callbacks.py"), "w") as f:
    f.write(callbacks_py)

print(f"Written callbacks.py: {len(callbacks_py)} bytes")
print(f"First 300 chars:\n{callbacks_py[:300]}")
print(f"\n... contains 'render_page': {'render_page' in callbacks_py}")
print(f"... contains 'navigate': {'def navigate' in callbacks_py}")
print(f"... contains 'update_graph_lens': {'update_graph_lens' in callbacks_py}")
print(f"... contains 'filter_opportunities': {'filter_opportunities' in callbacks_py}")


# COMMAND ----------

# DBTITLE 1,Overwrite app.py with thin entrypoint
app_py = '''"""CLA Customer Relationship Hub - Thin entrypoint."""

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
'''

with open(os.path.join(BASE_DIR, "app.py"), "w") as f:
    f.write(app_py)

print(f"Written app.py: {len(app_py)} bytes")
print(app_py)


# COMMAND ----------

# DBTITLE 1,Verify all modules - syntax check
# MAGIC %pip install --quiet databricks-sdk --upgrade

# COMMAND ----------

# DBTITLE 1,Deploy the refactored app
import requests
import time

# Get workspace host and token
ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
host = ctx.apiUrl().get()
token = ctx.apiToken().get()

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Deploy the app
print("Deploying hackathon-team-3...")
resp = requests.post(
    f"{host}/api/2.0/apps/hackathon-team-3/deployments",
    headers=headers,
    json={
        "source_code_path": "/Workspace/Users/cody.kreiner@claconnect.com/hackathon-team-3",
        "mode": "SNAPSHOT"
    }
)
print(f"Deploy response: {resp.status_code}")
deploy_data = resp.json()
print(f"Deployment ID: {deploy_data.get('deployment_id', 'N/A')}")

# Poll for completion
deployment_id = deploy_data.get("deployment_id")
if deployment_id:
    for i in range(30):
        time.sleep(5)
        status_resp = requests.get(
            f"{host}/api/2.0/apps/hackathon-team-3/deployments/{deployment_id}",
            headers=headers
        )
        status_data = status_resp.json()
        state = status_data.get("status", {}).get("state", "UNKNOWN")
        msg = status_data.get("status", {}).get("message", "")
        print(f"  [{i*5}s] State: {state} - {msg}")
        if state in ("SUCCEEDED", "FAILED"):
            break
    print(f"\nFinal status: {state}")
    if state == "SUCCEEDED":
        print("App deployed successfully!")
    else:
        print(f"DEPLOYMENT FAILED: {msg}")
