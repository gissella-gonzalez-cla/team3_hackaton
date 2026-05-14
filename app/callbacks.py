"""Callback definitions for the CLA app - FIXED routing architecture."""

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

@callback(Output("entity-graph", "elements"), Input("entity-lens-tabs", "active_tab"))
def update_graph_lens(active_tab):
    return build_cytoscape_elements(active_tab)


@callback(Output("entity-detail-panel", "children"), Input("entity-graph", "tapNodeData"))
def show_entity_detail(node_data):
    if not node_data:
        return html.Div()

    if node_data.get("type") in ["Service", "Contract", "Contact", "Project", "Opportunity", "Scorecard"]:
        details = []
        for k in ["type", "service", "status", "due_date", "priority", "gap_type", "confidence", "score", "strength"]:
            if k in node_data and node_data.get(k) not in (None, ""):
                details.append(html.P(f"{k.replace('_',' ').title()}: {node_data[k]}", style={"color": "#8899aa", "marginBottom": "0.25rem"}))

        return html.Div(
            [
                html.Div(
                    [
                        html.H6(node_data.get("label", ""), style={"color": "#fff"}),
                        *details,
                    ],
                    style=CARD_STYLE,
                )
            ]
        )

    entity = next((e for e in ENTITIES if e["id"] == node_data.get("id")), None)
    if not entity:
        return html.Div()

    entity_projects = [p for p in PROJECTS if p["entity"] == entity["id"]]
    entity_contacts = [c for c in CONTACTS if c["entity"] == entity["id"]]
    entity_contracts = [ct for ct in CONTRACTS if ct["entity"] == entity["id"]]

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5(entity["name"], style={"color": "#fff"}),
                            html.P(f"{entity['type']} | {entity['industry']} | Revenue: {entity['revenue']}", style={"color": "#4fc3f7", "fontSize": "0.85rem"}),
                            html.P(f"Relationship Lead: {entity['relationship_lead']} | Team: {entity['coverage_team']}", style={"color": "#8899aa", "fontSize": "0.8rem"}),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.Span(f"{len(entity_projects)} Projects", className="badge bg-info me-2"),
                                    html.Span(f"{len(entity_contacts)} Contacts", className="badge bg-success me-2"),
                                    html.Span(f"{len(entity_contracts)} Contracts", className="badge bg-warning"),
                                ],
                                style={"textAlign": "right"},
                            )
                        ],
                        width=6,
                    ),
                ]
            ),
            html.Hr(style={"borderColor": "#2a3f55"}),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P("Projects", style={"color": "#8899aa", "fontWeight": "bold", "fontSize": "0.8rem"}),
                            *[
                                html.Div(
                                    [
                                        html.Span(f"{p['name']} ({p['service']})", style={"color": "#fff", "fontSize": "0.8rem"}),
                                        html.Span(f" - {p['phase']}", style={"color": "#8899aa", "fontSize": "0.75rem"}),
                                    ]
                                )
                                for p in entity_projects
                            ],
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.P("Contacts", style={"color": "#8899aa", "fontWeight": "bold", "fontSize": "0.8rem"}),
                            *[
                                html.Div(
                                    [
                                        html.Span(f"{c['name']} ({c['title']})", style={"color": "#fff", "fontSize": "0.8rem"}),
                                        html.Span(f" - {c['strength']}", style={"color": TAG_COLORS.get(c["strength"], "#fff"), "fontSize": "0.75rem"}),
                                    ]
                                )
                                for c in entity_contacts
                            ],
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.P("Contracts", style={"color": "#8899aa", "fontWeight": "bold", "fontSize": "0.8rem"}),
                            *[
                                html.Div(
                                    [
                                        html.Span(f"{ct['type'][:25]}", style={"color": "#fff", "fontSize": "0.8rem"}),
                                        html.Span(f" - {ct['value']}", style={"color": "#27ae60", "fontSize": "0.75rem"}),
                                    ]
                                )
                                for ct in entity_contracts
                            ],
                        ],
                        width=4,
                    ),
                ]
            ),
        ],
        style=CARD_STYLE,
    )


@callback(
    Output("manual-recording-status", "children"),
    Output("manual-recording-status", "style"),
    Output("manual-transcript", "value"),
    Input("toggle-recording", "n_clicks"),
    Input("add-timestamp", "n_clicks"),
    Input("insert-follow-up", "n_clicks"),
    State("manual-transcript", "value"),
    State("selected-entity", "data"),
    prevent_initial_call=True,
)
def update_manual_transcript(toggle_recording, add_timestamp, insert_follow_up, transcript, selected_entity):
    transcript_value = transcript or ""
    entity = get_entity(selected_entity) or ENTITIES[0]
    trigger = ctx.triggered_id
    is_recording = ((toggle_recording or 0) % 2) == 1

    if trigger == "add-timestamp":
        timestamp = datetime.now().strftime("%H:%M")
        transcript_value = f"{transcript_value}\n[{timestamp}] Topic shift / key quote:".strip()
    elif trigger == "insert-follow-up":
        template = (
            f"\nAction items for {entity['name']}:\n"
            "- Decision owner:\n"
            "- Follow-up deliverable:\n"
            "- Next meeting date:\n"
        )
        transcript_value = f"{transcript_value}{template}".strip()

    status_text = "Manual capture is live. Keep notes brief and use timestamps." if is_recording else "Recorder idle. Ready for manual capture."
    status_style = {"color": "#ffb3b3" if is_recording else "#b2c7d6", "margin": "0.75rem 0", "fontWeight": "bold" if is_recording else "normal"}

    return status_text, status_style, transcript_value


@callback(
    Output("roadmap-store", "data"),
    Output("roadmap-timeline", "children"),
    Output("roadmap-save-status", "children"),
    Output("roadmap-title", "value"),
    Output("roadmap-notes", "value"),
    Output("roadmap-next-steps", "value"),
    Input("roadmap-add", "n_clicks"),
    Input("roadmap-save-from-transcript", "n_clicks"),
    State("selected-entity", "data"),
    State("roadmap-store", "data"),
    State("roadmap-stage", "value"),
    State("roadmap-title", "value"),
    State("roadmap-notes", "value"),
    State("roadmap-next-steps", "value"),
    State("manual-transcript", "value"),
    prevent_initial_call=True,
)
def add_roadmap_entry(add_clicks, save_from_transcript_clicks, selected_entity, roadmap_data, stage, title, notes, next_steps, transcript):
    if not ctx.triggered_id:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    entity = selected_entity or ENTITIES[0]["id"]
    roadmap_data = list(roadmap_data or [])

    trig = ctx.triggered_id
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    if trig == "roadmap-save-from-transcript":
        transcript_value = (transcript or "").strip()
        if not transcript_value:
            timeline = _render_roadmap_timeline(entity, roadmap_data)
            return roadmap_data, timeline, "Nothing to save — manual transcript is empty.", title, notes, next_steps

        entry = {
            "id": f"rm_{int(datetime.now().timestamp()*1000)}_{random.randint(100,999)}",
            "entity": entity,
            "timestamp": ts,
            "stage": stage or "Discovery",
            "title": title or "In-person conversation (manual capture)",
            "notes": notes or "",
            "next_steps": next_steps or "",
            "transcript_excerpt": transcript_value[:2000],
            "source": "Manual transcript",
        }
        roadmap_data.append(entry)
        status = "Saved manual transcript into the client roadmap timeline."

    else:
        if not (title or notes or next_steps):
            timeline = _render_roadmap_timeline(entity, roadmap_data)
            return roadmap_data, timeline, "Add at least a title, notes, or next steps.", title, notes, next_steps

        entry = {
            "id": f"rm_{int(datetime.now().timestamp()*1000)}_{random.randint(100,999)}",
            "entity": entity,
            "timestamp": ts,
            "stage": stage or "Discovery",
            "title": (title or "Client roadmap note").strip(),
            "notes": (notes or "").strip(),
            "next_steps": (next_steps or "").strip(),
            "source": "Manual",
        }
        roadmap_data.append(entry)
        status = "Roadmap entry added."

    timeline = _render_roadmap_timeline(entity, roadmap_data)

    # Clear fields after save
    return roadmap_data, timeline, status, "", "", ""


@callback(
    Output("roadmap-timeline", "children", allow_duplicate=True),
    Input("roadmap-store", "data"),
    State("selected-entity", "data"),
    prevent_initial_call=True,
)
def refresh_roadmap_timeline(roadmap_data, selected_entity):
    entity = selected_entity or ENTITIES[0]["id"]
    return _render_roadmap_timeline(entity, roadmap_data)


@callback(Output("opportunity-cards", "children"), Input("opp-filter-all", "n_clicks"), Input("opp-filter-hot", "n_clicks"), Input("opp-filter-warm", "n_clicks"), Input("opp-filter-watch", "n_clicks"))
def filter_opportunities(all_clicks, hot_clicks, warm_clicks, watch_clicks):
    trig = ctx.triggered_id
    if trig == "opp-filter-hot":
        return build_opportunity_cards("Hot")
    if trig == "opp-filter-warm":
        return build_opportunity_cards("Warm")
    if trig == "opp-filter-watch":
        return build_opportunity_cards("Watch")
    return build_opportunity_cards()

