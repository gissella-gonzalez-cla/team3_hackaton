"""Page layout functions for the CLA app."""

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



def my_customers_page():
    spotlight_entities = ENTITIES[:3]
    spotlight_cards = []

    for entity in spotlight_entities:
        spotlight_cards.append(
            dbc.Col(
                html.Div(
                    [
                        html.P(
                            "Conversation Ready",
                            style={
                                "color": "#9db5c8",
                                "fontSize": "0.72rem",
                                "letterSpacing": "1px",
                                "textTransform": "uppercase",
                                "marginBottom": "0.25rem",
                            },
                        ),
                        html.H4(entity["name"], style={"color": "#fff", "marginBottom": "0.3rem"}),
                        html.P(
                            f"{entity['coverage_team']} | Lead: {entity['relationship_lead']}",
                            style={"color": "#a8bac8", "marginBottom": "0.75rem", "fontSize": "0.85rem"},
                        ),
                        html.P(
                            get_entity_opportunities(entity["id"])[0]["description"]
                            if get_entity_opportunities(entity["id"])
                            else "Prepare for a portfolio review and capture emerging needs.",
                            style={"color": "#dbe7f0", "fontSize": "0.9rem", "marginBottom": "1rem"},
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-box-arrow-up-right me-2"), "Go To Client"],
                            id={"type": "spotlight-client", "entity": entity["id"]},
                            color="light",
                            outline=True,
                            className="w-100",
                        ),
                    ],
                    style={
                        **CARD_STYLE,
                        "height": "100%",
                        "background": "linear-gradient(135deg, #274760 0%, #152637 100%)",
                    },
                ),
                xs=12,
                lg=4,
            )
        )

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P(
                                        "MY CUSTOMERS",
                                        style={"color": "#7fa8c6", "letterSpacing": "2px", "fontSize": "0.75rem", "marginBottom": "0.5rem"},
                                    ),
                                    html.H1("Client relationship workspace", style={"color": "#fff", "marginBottom": "0.5rem", "fontSize": "2.5rem"}),
                                    html.P(
                                        "Start from a customer-first layout, open a full client workspace, and move directly into a guided conversation plan with meeting and capture actions.",
                                        style={"color": "#b2c7d6", "fontSize": "1rem", "maxWidth": "760px", "marginBottom": "0"},
                                    ),
                                ],
                                style={"flex": "1"},
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        [html.I(className="bi bi-diagram-3 me-2"), "Entity Map"],
                                        id={"type": "nav-btn", "page": "entity"},
                                        color="info",
                                        className="w-100 mb-2",
                                        style={"borderRadius": "10px", "fontWeight": "bold"},
                                    ),
                                    html.Div([html.P("Next Action", style={"color": "#9db5c8", "fontSize": "0.75rem", "marginBottom": "0.15rem"}), html.H4("Open a client", style={"color": "#fff", "marginBottom": "0"})]),
                                ],
                                style={"minWidth": "220px", "padding": "1rem 1.25rem", "borderRadius": "14px", "backgroundColor": "#162433", "border": "1px solid #30506b"},
                            ),
                        ],
                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "gap": "1rem", "flexWrap": "wrap"},
                    )
                ],
                style={
                    "padding": "1.5rem",
                    "borderRadius": "18px",
                    "marginBottom": "1.5rem",
                    "background": "linear-gradient(135deg, #243d56 0%, #11202f 100%)",
                    "border": "1px solid #2f526d",
                },
            ),
            build_customer_summary_cards(),
            dbc.Row(spotlight_cards, className="g-3 mb-4"),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H4("Prepared conversation tracks", style={"color": "#fff", "marginBottom": "0.75rem"}),
                                html.P(
                                    "Each client workspace includes a scripted talk track, meeting setup link, and mobile-friendly note capture panel.",
                                    style={"color": "#b2c7d6", "marginBottom": "0.75rem"},
                                ),
                                html.Ul([html.Li(step, style={"color": "#dbe7f0", "marginBottom": "0.35rem"}) for step in MEETING_AUTOMATION_STEPS]),
                            ],
                            style=CARD_STYLE,
                        ),
                        xs=12,
                        lg=4,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H4("Customer Portfolio", style={"color": "#fff", "marginBottom": "0.75rem"}),
                                html.P(
                                    "Open any customer to see full-screen entity details, key contacts, active work, and a structured conversation flow.",
                                    style={"color": "#b2c7d6", "marginBottom": "0"},
                                ),
                            ],
                            style=CARD_STYLE,
                        ),
                        xs=12,
                        lg=8,
                    ),
                ],
                className="g-3 mb-3",
            ),
            build_customer_cards(),
        ]
    )


def _render_roadmap_timeline(entity_id, roadmap_entries):
    entries = [e for e in (roadmap_entries or []) if e.get("entity") == entity_id]
    entries = sorted(entries, key=lambda x: x.get("timestamp", ""), reverse=True)

    if not entries:
        return html.Div(
            "No roadmap entries yet. Add one after your next client conversation.",
            style={"color": "#b2c7d6"},
        )

    timeline_cards = []
    for e in entries[:25]:
        stage = e.get("stage", "")
        title = e.get("title", "")
        notes = e.get("notes", "")
        next_steps = e.get("next_steps", "")
        ts = e.get("timestamp", "")
        source = e.get("source", "Manual")

        timeline_cards.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(stage, className="badge", style={"backgroundColor": "#2a4a6b", "marginRight": "0.5rem"}),
                            html.Span(source, className="badge", style={"backgroundColor": "#122131", "color": "#9db5c8"}),
                            html.Span(ts, style={"color": "#6d8597", "fontSize": "0.75rem", "marginLeft": "auto"}),
                        ],
                        style={"display": "flex", "alignItems": "center", "gap": "0.5rem", "marginBottom": "0.5rem"},
                    ),
                    html.H6(title or "Client conversation note", style={"color": "#fff", "marginBottom": "0.4rem"}),
                    html.P(notes, style={"color": "#b2c7d6", "marginBottom": "0.4rem", "whiteSpace": "pre-wrap"}),
                    html.P(
                        next_steps,
                        style={"color": "#f39c12", "marginBottom": "0", "whiteSpace": "pre-wrap"} if next_steps else {"display": "none"},
                    ),
                ],
                style={"backgroundColor": "#122131", "border": "1px solid #2a3f55", "borderRadius": "12px", "padding": "1rem", "marginBottom": "0.75rem"},
            )
        )

    return html.Div(timeline_cards)


def client_detail_page(entity_id):
    entity = get_entity(entity_id) or ENTITIES[0]
    contacts = get_entity_contacts(entity["id"])
    projects = get_entity_projects(entity["id"])
    contracts = get_entity_contracts(entity["id"])
    opportunities = get_entity_opportunities(entity["id"])
    related_entities = get_related_entities(entity["id"])

    contact_rows = []
    for contact in contacts:
        contact_rows.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(contact["name"], style={"color": "#fff", "marginBottom": "0.1rem"}),
                            html.P(contact["title"], style={"color": "#9db5c8", "marginBottom": "0"}),
                        ]
                    ),
                    html.Div(
                        [
                            html.Span(contact["strength"], className="badge", style={"backgroundColor": TAG_COLORS.get(contact["strength"], "#95a5a6")}),
                            html.P(contact["email"], style={"color": "#b2c7d6", "fontSize": "0.8rem", "margin": "0.35rem 0 0 0"}),
                        ],
                        style={"textAlign": "right"},
                    ),
                ],
                style={"display": "flex", "justifyContent": "space-between", "gap": "1rem", "padding": "0.85rem 0", "borderBottom": "1px solid #2a3f55", "flexWrap": "wrap"},
            )
        )

    project_rows = []
    for project in projects:
        project_rows.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(project["name"], style={"color": "#fff", "marginBottom": "0.15rem"}),
                            html.P(f"{project['service']} | {project['phase']} | {project['type']}", style={"color": "#9db5c8", "marginBottom": "0"}),
                        ]
                    ),
                    html.Div(
                        [
                            html.Span(project["status"], className="badge", style={"backgroundColor": "#2a4a6b", "marginRight": "0.5rem"}),
                            html.Span(project["value"], style={"color": "#4fc3f7", "fontWeight": "bold"}),
                        ]
                    ),
                ],
                style={"display": "flex", "justifyContent": "space-between", "gap": "1rem", "padding": "0.85rem 0", "borderBottom": "1px solid #2a3f55", "flexWrap": "wrap"},
            )
        )

    contract_rows = []
    for contract in contracts:
        contract_rows.append(
            html.Div(
                [
                    html.H6(contract["type"], style={"color": "#fff", "marginBottom": "0.15rem"}),
                    html.P(f"{contract['start']} to {contract['end']} | {contract['status']} | {contract['value']}", style={"color": "#9db5c8", "marginBottom": "0"}),
                ],
                style={"padding": "0.85rem 0", "borderBottom": "1px solid #2a3f55"},
            )
        )

    playbook_items = []
    for section in DISCOVERY_PLAYBOOK:
        playbook_items.append(
            dbc.AccordionItem(
                [
                    html.P(section["prompt"], style={"color": "#dbe7f0"}),
                    html.Ul([html.Li(point, style={"color": "#b2c7d6", "marginBottom": "0.35rem"}) for point in section["talk_track"]]),
                ],
                title=section["title"],
            )
        )

    opportunity_rows = []
    for opportunity in opportunities or [
        {
            "title": "Relationship review",
            "description": "No immediate growth gap is logged. Use this conversation to confirm current priorities and uncover the next advisory need.",
            "priority": "Warm",
        }
    ]:
        opportunity_rows.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                opportunity["priority"].upper(),
                                className="badge",
                                style={"backgroundColor": TAG_COLORS.get(opportunity["priority"], "#95a5a6"), "marginRight": "0.5rem"},
                            ),
                            html.Span(opportunity.get("gap_type", "Client agenda"), style={"color": "#9db5c8", "fontSize": "0.8rem"}),
                        ],
                        style={"marginBottom": "0.5rem"},
                    ),
                    html.H6(opportunity["title"], style={"color": "#fff", "marginBottom": "0.3rem"}),
                    html.P(opportunity["description"], style={"color": "#b2c7d6", "marginBottom": "0"}),
                ],
                style={"padding": "1rem", "backgroundColor": "#122131", "borderRadius": "12px", "marginBottom": "0.75rem"},
            )
        )

    related_items = [
        html.Li(f"{relative['name']} | {relative['type']} | {relative['industry']}", style={"color": "#dbe7f0", "marginBottom": "0.35rem"})
        for relative in related_entities
    ] or [html.Li("No adjacent entities are linked in the current dataset.", style={"color": "#dbe7f0"})]

    return html.Div(
        [
            html.Div(
                [
                    dbc.Button(
                        [html.I(className="bi bi-arrow-left me-2"), "Back to My Customers"],
                        id={"type": "nav-btn", "page": "my-customers"},
                        color="secondary",
                        outline=True,
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P("CLIENT WORKSPACE", style={"color": "#7fa8c6", "letterSpacing": "2px", "fontSize": "0.75rem", "marginBottom": "0.35rem"}),
                                    html.H1(entity["name"], style={"color": "#fff", "marginBottom": "0.35rem", "fontSize": "2.4rem"}),
                                    html.P(
                                        f"{entity['type']} | {entity['industry']} | Revenue {entity['revenue']} | Lead {entity['relationship_lead']}",
                                        style={"color": "#b2c7d6", "marginBottom": "0"},
                                    ),
                                ],
                                style={"flex": "1"},
                            ),
                            html.Div(
                                [
                                    html.A(
                                        dbc.Button([html.I(className="bi bi-camera-video me-2"), "Create Teams Meeting"], color="info", className="w-100 mb-2"),
                                        href=build_teams_meeting_link(entity),
                                        target="_blank",
                                    ),
                                    html.A(
                                        dbc.Button([html.I(className="bi bi-envelope me-2"), "Email Client Prep Note"], color="light", outline=True, className="w-100"),
                                        href=build_mailto_link(entity),
                                    ),
                                ],
                                style={"width": "280px", "maxWidth": "100%"},
                            ),
                        ],
                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "gap": "1rem", "flexWrap": "wrap"},
                    ),
                ],
                style={
                    "padding": "1.5rem",
                    "marginBottom": "1.5rem",
                    "borderRadius": "18px",
                    "background": "linear-gradient(135deg, #274760 0%, #132434 100%)",
                    "border": "1px solid #30506b",
                },
            ),

            # Roadmap + capture (the "headless CRL" memory system)
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H4("Client Roadmap (Capture What You Know)", style={"color": "#fff", "marginBottom": "0.5rem"}),
                                html.P(
                                    "Log conversation outcomes so the relationship context is reusable across the firm — not trapped in one person's head.",
                                    style={"color": "#b2c7d6", "marginBottom": "1rem"},
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.P("Stage", style={"color": "#9db5c8", "fontSize": "0.8rem", "marginBottom": "0.35rem"}),
                                                dcc.Dropdown(
                                                    id="roadmap-stage",
                                                    options=[{"label": s, "value": s} for s in ROADMAP_STAGES],
                                                    value="Discovery",
                                                    clearable=False,
                                                    style={"color": "#0f1724"},
                                                ),
                                            ],
                                            md=4,
                                        ),
                                        dbc.Col(
                                            [
                                                html.P("Title", style={"color": "#9db5c8", "fontSize": "0.8rem", "marginBottom": "0.35rem"}),
                                                dbc.Input(id="roadmap-title", placeholder="e.g., QBR recap, ownership change, acquisition plan"),
                                            ],
                                            md=8,
                                        ),
                                    ],
                                    className="g-2",
                                ),
                                html.Div(style={"height": "0.75rem"}),
                                html.P("Key notes / client language", style={"color": "#9db5c8", "fontSize": "0.8rem", "marginBottom": "0.35rem"}),
                                dbc.Textarea(
                                    id="roadmap-notes",
                                    placeholder="Capture the key facts, what changed, risks, what they care about, and what they said verbatim if useful.",
                                    style={"minHeight": "120px"},
                                ),
                                html.Div(style={"height": "0.75rem"}),
                                html.P("Next steps (owners + dates)", style={"color": "#9db5c8", "fontSize": "0.8rem", "marginBottom": "0.35rem"}),
                                dbc.Textarea(
                                    id="roadmap-next-steps",
                                    placeholder="- Owner:\n- Deliverable:\n- Due date:",
                                    style={"minHeight": "90px"},
                                ),
                                html.Div(style={"height": "0.75rem"}),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                [html.I(className="bi bi-plus-circle me-2"), "Add Roadmap Entry"],
                                                id="roadmap-add",
                                                color="info",
                                                className="w-100",
                                                style={"borderRadius": "10px", "fontWeight": "bold"},
                                            ),
                                            md=6,
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                [html.I(className="bi bi-mic-fill me-2"), "Save Manual Transcript To Roadmap"],
                                                id="roadmap-save-from-transcript",
                                                color="secondary",
                                                outline=True,
                                                className="w-100",
                                                style={"borderRadius": "10px", "fontWeight": "bold"},
                                            ),
                                            md=6,
                                        ),
                                    ],
                                    className="g-2",
                                ),
                                html.Div(id="roadmap-save-status", style={"color": "#b2c7d6", "marginTop": "0.75rem"}),
                            ],
                            style=CARD_STYLE,
                        ),
                        xs=12,
                        lg=6,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H4("Roadmap Timeline", style={"color": "#fff", "marginBottom": "0.75rem"}),
                                html.Div(id="roadmap-timeline"),
                            ],
                            style=CARD_STYLE,
                        ),
                        xs=12,
                        lg=6,
                    ),
                ],
                className="g-3 mb-3",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H4("Client Summary", style={"color": "#fff", "marginBottom": "0.75rem"}),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P("Coverage Team", style={"color": "#6d8597", "fontSize": "0.72rem", "marginBottom": "0.1rem"}),
                                                html.H5(entity["coverage_team"], style={"color": "#fff", "marginBottom": "0"}),
                                            ],
                                            style={"flex": "1"},
                                        ),
                                        html.Div(
                                            [
                                                html.P("Open Opportunities", style={"color": "#6d8597", "fontSize": "0.72rem", "marginBottom": "0.1rem"}),
                                                html.H5(str(len(opportunities)), style={"color": "#fff", "marginBottom": "0"}),
                                            ],
                                            style={"flex": "1"},
                                        ),
                                        html.Div(
                                            [
                                                html.P("Client Scorecard", style={"color": "#6d8597", "fontSize": "0.72rem", "marginBottom": "0.1rem"}),
                                                html.H5(str(entity.get("scorecard", "—")), style={"color": "#fff", "marginBottom": "0"}),
                                            ],
                                            style={"flex": "1"},
                                        ),
                                    ],
                                    style={"display": "flex", "gap": "0.75rem", "flexWrap": "wrap"},
                                ),
                                html.Hr(style={"borderColor": "#2a3f55"}),
                                html.P("Related entities", style={"color": "#9db5c8", "fontWeight": "bold", "marginBottom": "0.5rem"}),
                                html.Ul(related_items, style={"paddingLeft": "1.1rem", "marginBottom": "0"}),
                            ],
                            style=CARD_STYLE,
                        ),
                        xs=12,
                        lg=4,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H4("Suggested Conversation Agenda", style={"color": "#fff", "marginBottom": "0.75rem"}),
                                dbc.Accordion(playbook_items, start_collapsed=True, always_open=True, flush=True),
                            ],
                            style=CARD_STYLE,
                        ),
                        xs=12,
                        lg=8,
                    ),
                ],
                className="g-3 mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([html.H4("Active Work", style={"color": "#fff", "marginBottom": "0.75rem"}), project_rows or [html.P("No active projects found.", style={"color": "#b2c7d6"})]], style=CARD_STYLE), xs=12, xl=6),
                    dbc.Col(html.Div([html.H4("Key Contacts", style={"color": "#fff", "marginBottom": "0.75rem"}), contact_rows or [html.P("No contacts found.", style={"color": "#b2c7d6"})]], style=CARD_STYLE), xs=12, xl=6),
                ],
                className="g-3 mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([html.H4("Growth Conversation Prompts", style={"color": "#fff", "marginBottom": "0.75rem"}), opportunity_rows], style=CARD_STYLE), xs=12, xl=6),
                    dbc.Col(html.Div([html.H4("Contracts And Commitments", style={"color": "#fff", "marginBottom": "0.75rem"}), contract_rows or [html.P("No contracts found.", style={"color": "#b2c7d6"})]], style=CARD_STYLE), xs=12, xl=6),
                ],
                className="g-3 mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H4("Meeting Automation", style={"color": "#fff", "marginBottom": "0.75rem"}),
                                html.Ul([html.Li(step, style={"color": "#dbe7f0", "marginBottom": "0.35rem"}) for step in MEETING_AUTOMATION_STEPS], style={"paddingLeft": "1.1rem", "marginBottom": "1rem"}),
                                html.A(dbc.Button([html.I(className="bi bi-calendar-event me-2"), "Schedule In Teams"], color="info", className="w-100"), href=build_teams_meeting_link(entity), target="_blank"),
                            ],
                            style=CARD_STYLE,
                        ),
                        xs=12,
                        lg=4,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H4("Mobile Capture And Manual Transcript", style={"color": "#fff", "marginBottom": "0.75rem"}),
                                html.P(
                                    "Use this lightweight panel during an in-person or mobile conversation when recording or live transcription needs a manual fallback.",
                                    style={"color": "#b2c7d6", "marginBottom": "1rem"},
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Button([html.I(className="bi bi-record-circle me-2"), "Start / Stop Capture"], id="toggle-recording", color="danger", className="w-100 mb-2"), xs=12, md=4),
                                        dbc.Col(dbc.Button([html.I(className="bi bi-clock-history me-2"), "Add Timestamp"], id="add-timestamp", color="secondary", className="w-100 mb-2"), xs=12, md=4),
                                        dbc.Col(dbc.Button([html.I(className="bi bi-journal-text me-2"), "Insert Follow-Up Template"], id="insert-follow-up", color="info", className="w-100 mb-2"), xs=12, md=4),
                                    ],
                                    className="g-2",
                                ),
                                html.Div(id="manual-recording-status", children="Recorder idle. Ready for manual capture.", style={"color": "#b2c7d6", "margin": "0.75rem 0"}),
                                dcc.Textarea(
                                    id="manual-transcript",
                                    value="",
                                    placeholder="Capture transcript snippets, action items, and verbatim client language here.",
                                    style={
                                        "width": "100%",
                                        "minHeight": "220px",
                                        "backgroundColor": "#0f1724",
                                        "color": "#fff",
                                        "border": "1px solid #2a3f55",
                                        "borderRadius": "12px",
                                        "padding": "0.9rem",
                                    },
                                ),
                                html.Ul([html.Li(tip, style={"color": "#9db5c8", "marginTop": "0.45rem"}) for tip in MOBILE_CAPTURE_TIPS], style={"paddingLeft": "1.1rem", "marginTop": "1rem", "marginBottom": "0"}),
                            ],
                            style=CARD_STYLE,
                        ),
                        xs=12,
                        lg=8,
                    ),
                ],
                className="g-3",
            ),
        ]
    )





def build_cytoscape_elements(lens="all"):
    elements = []

    # Entity nodes
    for e in ENTITIES:
        classes = f"{e['type'].lower()}"
        if lens == "service":
            classes += f" {e.get('coverage_team', '').split()[0].lower()}"

        elements.append(
            {
                "data": {
                    "id": e["id"],
                    "label": e["name"],
                    "type": e["type"],
                    "industry": e["industry"],
                    "revenue": e["revenue"],
                    "lead": e["relationship_lead"],
                    "score": e.get("scorecard"),
                },
                "classes": classes,
            }
        )

    # Parent-child edges
    for e in ENTITIES:
        if "parent" in e:
            elements.append({"data": {"source": e["parent"], "target": e["id"], "label": "subsidiary"}})

    # Service lens
    if lens == "service":
        for p in PROJECTS:
            elements.append(
                {
                    "data": {"source": p["entity"], "target": f"svc_{p['service']}", "label": p["service"]},
                    "classes": "service-edge",
                }
            )
        for svc in sorted(set(p["service"] for p in PROJECTS)):
            elements.append({"data": {"id": f"svc_{svc}", "label": svc, "type": "Service"}, "classes": "service-node"})

    # Contracts lens
    if lens == "contracts":
        for ct in CONTRACTS:
            elements.append(
                {
                    "data": {"source": ct["entity"], "target": f"ct_{ct['id']}", "label": ct["type"][:15]},
                    "classes": "contract-edge",
                }
            )
            status_class = "active" if ct["status"] == "Active" else "renewal"
            elements.append(
                {
                    "data": {"id": f"ct_{ct['id']}", "label": f"{ct['type'][:20]}\n{ct['value']}", "type": "Contract", "status": ct["status"]},
                    "classes": f"contract-node {status_class}",
                }
            )

    # Contacts lens
    if lens == "contacts":
        for c in CONTACTS:
            strength_class = c["strength"].lower()
            elements.append(
                {
                    "data": {"id": c["id"], "label": f"{c['name']}\n{c['title']}", "type": "Contact", "strength": c["strength"]},
                    "classes": f"contact-node {strength_class}",
                }
            )
            elements.append(
                {
                    "data": {"source": c["entity"], "target": c["id"], "label": c["strength"]},
                    "classes": f"contact-edge {strength_class}",
                }
            )

    # Health lens (projects + overdue)
    if lens == "health":
        for p in PROJECTS:
            due = p.get("due_date")
            overdue = False
            if due:
                try:
                    overdue = datetime.strptime(due, "%Y-%m-%d").date() < datetime.now().date()
                except Exception:
                    overdue = False

            status_class = "overdue" if overdue else "ontrack"
            elements.append(
                {
                    "data": {
                        "id": f"prj_{p['id']}",
                        "label": f"{p['name']}\n{p['status']}",
                        "type": "Project",
                        "service": p["service"],
                        "status": p["status"],
                        "due_date": p.get("due_date", ""),
                    },
                    "classes": f"project-node {status_class}",
                }
            )
            elements.append(
                {
                    "data": {"source": p["entity"], "target": f"prj_{p['id']}", "label": p["service"]},
                    "classes": f"project-edge {status_class}",
                }
            )

    # Gaps lens (opportunities)
    if lens == "gaps":
        for o in OPPORTUNITIES:
            priority_class = o["priority"].lower()
            elements.append(
                {
                    "data": {
                        "id": f"opp_{o['id']}",
                        "label": f"{o['title']}\n{o['potential_revenue']}",
                        "type": "Opportunity",
                        "priority": o["priority"],
                        "gap_type": o.get("gap_type", ""),
                        "confidence": o.get("confidence", ""),
                    },
                    "classes": f"opportunity-node {priority_class}",
                }
            )
            elements.append(
                {
                    "data": {"source": o["entity"], "target": f"opp_{o['id']}", "label": o["gap_type"]},
                    "classes": f"opportunity-edge {priority_class}",
                }
            )

    # Scorecard lens
    if lens == "scorecard":
        for e in ENTITIES:
            score = e.get("scorecard")
            if score is None:
                continue
            band = "good" if score >= 80 else "watch" if score >= 60 else "risk"
            elements.append(
                {
                    "data": {"id": f"sc_{e['id']}", "label": f"Score\n{score}", "type": "Scorecard", "score": score},
                    "classes": f"scorecard-node {band}",
                }
            )
            elements.append(
                {"data": {"source": e["id"], "target": f"sc_{e['id']}", "label": "health"}, "classes": f"scorecard-edge {band}"}
            )

    return elements


CYTO_STYLESHEET = [
    {
        "selector": "node",
        "style": {
            "label": "data(label)",
            "text-wrap": "wrap",
            "text-max-width": "120px",
            "font-size": "10px",
            "color": "#fff",
            "text-valign": "center",
            "background-color": "#2a4a6b",
            "border-color": "#4fc3f7",
            "border-width": 2,
            "width": 60,
            "height": 60,
            "padding": "10px",
        },
    },
    {"selector": ".parent", "style": {"background-color": "#1a5276", "border-color": "#4fc3f7", "border-width": 3, "width": 80, "height": 80, "font-size": "11px", "font-weight": "bold"}},
    {"selector": ".subsidiary", "style": {"background-color": "#1e3a5f", "border-color": "#5dade2", "border-width": 2, "width": 60, "height": 60}},

    {"selector": ".service-node", "style": {"background-color": "#0e6655", "border-color": "#27ae60", "border-width": 2, "shape": "diamond", "width": 50, "height": 50}},
    {"selector": ".service-edge", "style": {"line-color": "#27ae60", "target-arrow-color": "#27ae60", "line-style": "dashed"}},

    {"selector": ".contract-node", "style": {"background-color": "#6c3483", "border-color": "#af7ac5", "border-width": 2, "shape": "round-rectangle", "width": 70, "height": 40}},
    {"selector": ".renewal", "style": {"background-color": "#7d3c1e", "border-color": "#f39c12", "border-width": 3}},
    {"selector": ".contract-edge", "style": {"line-color": "#af7ac5", "target-arrow-color": "#af7ac5"}},

    {"selector": ".contact-node", "style": {"background-color": "#1a5276", "border-color": "#85c1e9", "border-width": 2, "shape": "ellipse", "width": 55, "height": 55}},
    {"selector": ".contact-node.strong", "style": {"border-color": "#27ae60"}},
    {"selector": ".contact-node.moderate", "style": {"border-color": "#f39c12"}},
    {"selector": ".contact-node.weak", "style": {"border-color": "#e74c3c"}},
    {"selector": ".contact-node.cold", "style": {"border-color": "#95a5a6", "border-style": "dashed"}},
    {"selector": ".contact-edge.strong", "style": {"line-color": "#27ae60", "width": 3}},
    {"selector": ".contact-edge.weak", "style": {"line-color": "#e74c3c", "line-style": "dashed", "width": 1}},
    {"selector": ".contact-edge.cold", "style": {"line-color": "#95a5a6", "line-style": "dotted", "width": 1}},

    # Projects / health
    {"selector": ".project-node", "style": {"shape": "round-rectangle", "width": 90, "height": 45, "background-color": "#1f2937", "border-width": 2, "font-size": "9px"}},
    {"selector": ".project-node.ontrack", "style": {"border-color": "#27ae60"}},
    {"selector": ".project-node.overdue", "style": {"border-color": "#e74c3c"}},
    {"selector": ".project-edge.ontrack", "style": {"line-color": "#27ae60", "target-arrow-color": "#27ae60"}},
    {"selector": ".project-edge.overdue", "style": {"line-color": "#e74c3c", "target-arrow-color": "#e74c3c", "line-style": "dashed"}},

    # Opportunities / gaps
    {"selector": ".opportunity-node", "style": {"shape": "hexagon", "width": 85, "height": 55, "background-color": "#3b1d2a", "border-width": 2, "font-size": "9px"}},
    {"selector": ".opportunity-node.hot", "style": {"border-color": "#e74c3c"}},
    {"selector": ".opportunity-node.warm", "style": {"border-color": "#f39c12"}},
    {"selector": ".opportunity-node.watch", "style": {"border-color": "#3498db"}},
    {"selector": ".opportunity-edge.hot", "style": {"line-color": "#e74c3c", "target-arrow-color": "#e74c3c"}},
    {"selector": ".opportunity-edge.warm", "style": {"line-color": "#f39c12", "target-arrow-color": "#f39c12"}},
    {"selector": ".opportunity-edge.watch", "style": {"line-color": "#3498db", "target-arrow-color": "#3498db"}},

    # Scorecard
    {"selector": ".scorecard-node", "style": {"shape": "diamond", "width": 55, "height": 55, "background-color": "#0b2a3f", "border-width": 3, "font-weight": "bold"}},
    {"selector": ".scorecard-node.good", "style": {"border-color": "#27ae60"}},
    {"selector": ".scorecard-node.watch", "style": {"border-color": "#f39c12"}},
    {"selector": ".scorecard-node.risk", "style": {"border-color": "#e74c3c"}},
    {"selector": ".scorecard-edge.good", "style": {"line-color": "#27ae60", "target-arrow-color": "#27ae60"}},
    {"selector": ".scorecard-edge.watch", "style": {"line-color": "#f39c12", "target-arrow-color": "#f39c12"}},
    {"selector": ".scorecard-edge.risk", "style": {"line-color": "#e74c3c", "target-arrow-color": "#e74c3c"}},

    {
        "selector": "edge",
        "style": {
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            "target-arrow-color": "#4a6a8a",
            "line-color": "#4a6a8a",
            "width": 2,
            "label": "data(label)",
            "font-size": "8px",
            "color": "#8899aa",
            "text-rotation": "autorotate",
        },
    },
]


def entity_view_page():
    return html.Div(
        [
            html.Div(
                [
                    html.H3("Entity Relationship Map", style={"color": "#fff", "marginBottom": "0.5rem"}),
                    html.P("Explore client entity structures, service relationships, and growth opportunities", style={"color": "#8899aa", "marginBottom": "1.5rem"}),
                ]
            ),
            dbc.Tabs(
                [
                    dbc.Tab(label="Structure Overview", tab_id="all", label_style={"color": "#8899aa"}, active_label_style={"color": "#4fc3f7"}),
                    dbc.Tab(label="Service Lens", tab_id="service", label_style={"color": "#8899aa"}, active_label_style={"color": "#27ae60"}),
                    dbc.Tab(label="Key Contacts", tab_id="contacts", label_style={"color": "#8899aa"}, active_label_style={"color": "#85c1e9"}),
                    dbc.Tab(label="Contracts", tab_id="contracts", label_style={"color": "#8899aa"}, active_label_style={"color": "#af7ac5"}),
                    dbc.Tab(label="Projects + Health", tab_id="health", label_style={"color": "#8899aa"}, active_label_style={"color": "#f39c12"}),
                    dbc.Tab(label="Coverage Gaps", tab_id="gaps", label_style={"color": "#8899aa"}, active_label_style={"color": "#e74c3c"}),
                    dbc.Tab(label="Scorecard", tab_id="scorecard", label_style={"color": "#8899aa"}, active_label_style={"color": "#4fc3f7"}),
                ],
                id="entity-lens-tabs",
                active_tab="all",
                style={"marginBottom": "1rem"},
            ),
            html.Div(
                [
                    cyto.Cytoscape(
                        id="entity-graph",
                        elements=build_cytoscape_elements("all"),
                        layout={"name": "cose", "animate": True, "nodeRepulsion": 8000, "idealEdgeLength": 120, "gravity": 0.3},
                        stylesheet=CYTO_STYLESHEET,
                        style={"width": "100%", "height": "520px", "backgroundColor": "#0f1724", "borderRadius": "12px", "border": "1px solid #2a3f55"},
                    ),
                ]
            ),
            html.Div(id="entity-detail-panel", style={"marginTop": "1.5rem"}),
            html.H5("All Entities", style={"color": "#fff", "marginTop": "2rem", "marginBottom": "1rem"}),
            html.Div(id="entity-cards-grid", children=build_entity_cards()),
        ]
    )


def build_entity_cards():
    cards = []
    for e in ENTITIES:
        entity_projects = [p for p in PROJECTS if p["entity"] == e["id"]]
        entity_contacts = [c for c in CONTACTS if c["entity"] == e["id"]]
        entity_contracts = [ct for ct in CONTRACTS if ct["entity"] == e["id"]]

        type_color = "#4fc3f7" if e["type"] == "Parent" else "#5dade2"
        cards.append(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span(e["type"].upper(), className="badge", style={"backgroundColor": type_color, "fontSize": "0.65rem", "marginRight": "0.5rem"}),
                                html.Span(e["industry"], style={"color": "#8899aa", "fontSize": "0.75rem"}),
                            ],
                            style={"marginBottom": "0.5rem"},
                        ),
                        html.H6(e["name"], style={"color": "#fff", "marginBottom": "0.3rem"}),
                        html.P(f"Lead: {e['relationship_lead']} | {e['coverage_team']}", style={"color": "#8899aa", "fontSize": "0.75rem", "marginBottom": "0.5rem"}),
                        html.Div(
                            [
                                html.Span(f"{len(entity_projects)} projects", className="badge bg-info me-2", style={"fontSize": "0.65rem"}),
                                html.Span(f"{len(entity_contacts)} contacts", className="badge bg-success me-2", style={"fontSize": "0.65rem"}),
                                html.Span(f"{len(entity_contracts)} contracts", className="badge bg-warning", style={"fontSize": "0.65rem"}),
                            ]
                        ),
                        html.Div([html.Span(f"Revenue: {e['revenue']}", style={"color": "#4fc3f7", "fontSize": "0.8rem", "fontWeight": "bold"})], style={"marginTop": "0.5rem"}),
                    ],
                    style=CARD_STYLE,
                ),
                width=4,
                className="mb-3",
            )
        )

    return dbc.Row(cards)





def opportunities_page():
    def parse_k(v):
        try:
            return int(v.replace("$", "").replace("K", ""))
        except Exception:
            return 0

    total_pipeline = sum(parse_k(o["potential_revenue"]) for o in OPPORTUNITIES)

    return html.Div(
        [
            html.Div(
                [
                    html.H3("Growth Opportunities", style={"color": "#fff", "marginBottom": "0.5rem"}),
                    html.P("AI-identified gaps in entity relationships and service coverage for CRL review", style={"color": "#8899aa", "marginBottom": "1.5rem"}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([html.H2(f"${total_pipeline}K", style={"color": "#27ae60", "marginBottom": "0"}), html.P("Total Pipeline Potential", style={"color": "#8899aa", "fontSize": "0.8rem"})], style=CARD_STYLE), width=3),
                    dbc.Col(html.Div([html.H2(str(len([o for o in OPPORTUNITIES if o["priority"] == "Hot"])), style={"color": "#e74c3c", "marginBottom": "0"}), html.P("Hot Opportunities", style={"color": "#8899aa", "fontSize": "0.8rem"})], style=CARD_STYLE), width=3),
                    dbc.Col(html.Div([html.H2(str(len([o for o in OPPORTUNITIES if o.get("gap_type") == "Entity Gap"])), style={"color": "#f39c12", "marginBottom": "0"}), html.P("Entity Gaps", style={"color": "#8899aa", "fontSize": "0.8rem"})], style=CARD_STYLE), width=3),
                    dbc.Col(html.Div([html.H2(str(len([o for o in OPPORTUNITIES if o.get("gap_type") == "Relationship Gap"])), style={"color": "#9b59b6", "marginBottom": "0"}), html.P("Relationship Gaps", style={"color": "#8899aa", "fontSize": "0.8rem"})], style=CARD_STYLE), width=3),
                ],
                className="mb-4",
            ),
            html.Div(
                [
                    dbc.ButtonGroup(
                        [
                            dbc.Button("All", id="opp-filter-all", color="light", size="sm", outline=True, className="me-1"),
                            dbc.Button("Hot", id="opp-filter-hot", size="sm", style={"backgroundColor": "#e74c3c", "border": "none"}, className="me-1"),
                            dbc.Button("Warm", id="opp-filter-warm", size="sm", style={"backgroundColor": "#f39c12", "border": "none"}, className="me-1"),
                            dbc.Button("Watch", id="opp-filter-watch", size="sm", style={"backgroundColor": "#3498db", "border": "none"}),
                        ]
                    )
                ],
                style={"marginBottom": "1.5rem"},
            ),
            html.Div(id="opportunity-cards", children=build_opportunity_cards()),
        ]
    )


def build_opportunity_cards(priority_filter=None):
    filtered = OPPORTUNITIES if not priority_filter else [o for o in OPPORTUNITIES if o["priority"] == priority_filter]
    cards = []

    for opp in filtered:
        entity = next((e for e in ENTITIES if e["id"] == opp["entity"]), {})
        priority_color = TAG_COLORS.get(opp["priority"], "#95a5a6")

        cards.append(
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.Span(opp["priority"].upper(), className="badge me-2", style={"backgroundColor": priority_color, "fontSize": "0.7rem"}),
                                            html.Span(opp["gap_type"], className="badge", style={"backgroundColor": "#2a3f55", "color": "#8899aa", "fontSize": "0.7rem"}),
                                        ],
                                        style={"marginBottom": "0.5rem"},
                                    ),
                                    html.H5(opp["title"], style={"color": "#fff", "marginBottom": "0.3rem"}),
                                    html.P(f"{entity.get('name', '')} | Lead: {entity.get('relationship_lead', '')}", style={"color": "#4fc3f7", "fontSize": "0.8rem", "marginBottom": "0.5rem"}),
                                    html.P(opp["description"], style={"color": "#8899aa", "fontSize": "0.85rem", "marginBottom": "0.75rem"}),
                                    html.Div([html.I(className="bi bi-exclamation-triangle me-1", style={"color": "#f39c12"}), html.Span(f"Contact Gap: {opp['contact_gap']}", style={"color": "#f39c12", "fontSize": "0.8rem"})]),
                                ],
                                width=8,
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.H4(opp["potential_revenue"], style={"color": "#27ae60", "marginBottom": "0.2rem"}),
                                            html.P("Potential Revenue", style={"color": "#8899aa", "fontSize": "0.7rem", "marginBottom": "1rem"}),
                                            html.Div(
                                                [
                                                    html.P("Confidence", style={"color": "#8899aa", "fontSize": "0.7rem", "marginBottom": "0.2rem"}),
                                                    html.Span(
                                                        opp["confidence"],
                                                        className="badge",
                                                        style={
                                                            "backgroundColor": "#27ae60" if opp["confidence"] == "High" else "#f39c12" if opp["confidence"] == "Medium" else "#95a5a6"
                                                        },
                                                    ),
                                                ]
                                            ),
                                            dbc.Button("Review & Assign", size="sm", color="info", className="mt-3 w-100", style={"borderRadius": "6px"}),
                                        ],
                                        style={"textAlign": "center", "padding": "1rem", "backgroundColor": "#0f1724", "borderRadius": "8px"},
                                    )
                                ],
                                width=4,
                            ),
                        ]
                    )
                ],
                style=CARD_STYLE,
            )
        )

    return cards


def contacts_page():
    rows = []
    for c in CONTACTS:
        entity = next((e for e in ENTITIES if e["id"] == c["entity"]), {})
        strength_color = TAG_COLORS.get(c["strength"], "#95a5a6")

        rows.append(
            html.Tr(
                [
                    html.Td(c["name"], style={"color": "#fff"}),
                    html.Td(c["title"], style={"color": "#8899aa"}),
                    html.Td(entity.get("name", ""), style={"color": "#4fc3f7"}),
                    html.Td(html.Span(c["strength"], className="badge", style={"backgroundColor": strength_color, "fontSize": "0.7rem"})),
                    html.Td(c["last_contact"], style={"color": "#8899aa"}),
                    html.Td(c["email"], style={"color": "#8899aa", "fontSize": "0.8rem"}),
                ]
            )
        )

    return html.Div(
        [
            html.H3("Client Contacts", style={"color": "#fff", "marginBottom": "0.5rem"}),
            html.P("Manage and track relationships with key client contacts", style={"color": "#8899aa", "marginBottom": "1.5rem"}),
            html.Div(
                [
                    dbc.Table(
                        [
                            html.Thead(html.Tr([html.Th("Name"), html.Th("Title"), html.Th("Entity"), html.Th("Strength"), html.Th("Last Contact"), html.Th("Email")] ), style={"color": "#8899aa"}),
                            html.Tbody(rows),
                        ],
                        bordered=False,
                        hover=True,
                        responsive=True,
                        className="table-dark",
                        style={"backgroundColor": "#1e2d3d", "borderRadius": "12px"},
                    )
                ],
                style=CARD_STYLE,
            ),
        ]
    )


def projects_page():
    phase_order = ["Planning", "Interim", "Fieldwork", "Reporting", "Conclusion"]
    cards = []

    for p in PROJECTS:
        entity = next((e for e in ENTITIES if e["id"] == p["entity"]), {})
        status_colors = {"On Track": "#27ae60", "Needs Review": "#f39c12", "Hot": "#e74c3c", "Waiting on Client": "#3498db", "AR Hold": "#e74c3c"}
        status_color = status_colors.get(p["status"], "#95a5a6")

        phase_idx = phase_order.index(p["phase"]) if p["phase"] in phase_order else 0
        progress_pct = ((phase_idx + 1) / len(phase_order)) * 100

        cards.append(
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div([
                                        html.Span(p["service"], className="badge me-2", style={"backgroundColor": "#2a4a6b", "fontSize": "0.7rem"}),
                                        html.Span(p["status"], className="badge", style={"backgroundColor": status_color, "fontSize": "0.7rem"}),
                                    ]),
                                    html.H6(p["name"], style={"color": "#fff", "marginTop": "0.5rem"}),
                                    html.P(f"{entity.get('name','')} | {p['type']}", style={"color": "#8899aa", "fontSize": "0.8rem"}),
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    html.P(f"Current Phase: {p['phase']}", style={"color": "#8899aa", "fontSize": "0.75rem", "marginBottom": "0.3rem"}),
                                    dbc.Progress(value=progress_pct, color="info", style={"height": "8px", "backgroundColor": "#0f1724"}),
                                    html.P(f"Due: {p.get('due_date','')}", style={"color": "#6d8597", "fontSize": "0.75rem", "marginTop": "0.35rem"}),
                                ],
                                width=5,
                            ),
                            dbc.Col([html.H5(p["value"], style={"color": "#4fc3f7", "textAlign": "right"})], width=3),
                        ],
                        align="center",
                    )
                ],
                style=CARD_STYLE,
            )
        )

    return html.Div(
        [
            html.H3("Active Projects", style={"color": "#fff", "marginBottom": "0.5rem"}),
            html.P("Track project phases and engagement status across the portfolio", style={"color": "#8899aa", "marginBottom": "1.5rem"}),
            html.Div(cards),
        ]
    )


def contracts_page():
    cards = []

    for ct in CONTRACTS:
        entity = next((e for e in ENTITIES if e["id"] == ct["entity"]), {})
        status_color = "#27ae60" if ct["status"] == "Active" else "#f39c12"

        cards.append(
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Span(ct["status"], className="badge", style={"backgroundColor": status_color, "fontSize": "0.7rem"}),
                                    html.H6(ct["type"], style={"color": "#fff", "marginTop": "0.5rem"}),
                                    html.P(entity.get("name", ""), style={"color": "#4fc3f7", "fontSize": "0.85rem"}),
                                ],
                                width=4,
                            ),
                            dbc.Col([html.P(f"{ct['start']} → {ct['end']}", style={"color": "#8899aa", "fontSize": "0.8rem"})], width=4),
                            dbc.Col([html.H5(ct["value"], style={"color": "#27ae60", "textAlign": "right"})], width=4),
                        ],
                        align="center",
                    )
                ],
                style=CARD_STYLE,
            )
        )

    return html.Div(
        [
            html.H3("Contracts & Agreements", style={"color": "#fff", "marginBottom": "0.5rem"}),
            html.P("Monitor active contracts, renewals, and engagement terms", style={"color": "#8899aa", "marginBottom": "1.5rem"}),
            html.Div(cards),
        ]
    )


