"""Navigation, sidebar, and helper components for the CLA app."""

from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from urllib.parse import quote
from data import ENTITIES, CONTACTS, PROJECTS, CONTRACTS, OPPORTUNITIES
from styles import SIDEBAR_STYLE, CARD_STYLE, TAG_COLORS


def make_nav_item(icon, label, page_id, active=False):
    return dbc.Button(
        [html.I(className=f"bi bi-{icon} me-2"), label],
        id={"type": "nav-btn", "page": page_id},
        className="w-100 text-start mb-1",
        color="primary" if active else "link",
        style={
            "color": "#fff" if active else "#8899aa",
            "borderRadius": "8px",
            "padding": "0.7rem 1rem",
            "fontSize": "0.9rem",
            "backgroundColor": "#2a4a6b" if active else "transparent",
            "border": "none",
        },
    )


def build_nav_items(active_page):
    return [
        make_nav_item("people-fill", "My Customers", "my-customers", active=(active_page == "my-customers")),
        make_nav_item("diagram-3", "Entity Map", "entity", active=(active_page == "entity")),
        make_nav_item("lightbulb", "Opportunities", "opportunities", active=(active_page == "opportunities")),
        make_nav_item("people", "Contacts", "contacts", active=(active_page == "contacts")),
        make_nav_item("folder2", "Projects", "projects", active=(active_page == "projects")),
        make_nav_item("file-earmark-text", "Contracts", "contracts", active=(active_page == "contracts")),
    ]


sidebar = html.Div(
    [
        html.Div(
            [
                html.H4("CLA", style={"color": "#4fc3f7", "fontWeight": "bold", "marginBottom": "0"}),
                html.P("Relationship Hub", style={"color": "#8899aa", "fontSize": "0.8rem", "marginTop": "0"}),
            ],
            style={"marginBottom": "2rem", "paddingLeft": "0.5rem"},
        ),
        html.P(
            "NAVIGATE",
            style={"color": "#556677", "fontSize": "0.7rem", "letterSpacing": "1px", "paddingLeft": "0.5rem"},
        ),
        html.Div(id="nav-items", children=build_nav_items("my-customers")),
        html.Hr(style={"borderColor": "#2a3f55", "margin": "1.5rem 0"}),
        html.P(
            "KEY METRICS",
            style={"color": "#556677", "fontSize": "0.7rem", "letterSpacing": "1px", "paddingLeft": "0.5rem"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Span("10", style={"fontSize": "1.5rem", "fontWeight": "bold", "color": "#4fc3f7"}),
                        html.P("Entities", style={"color": "#8899aa", "fontSize": "0.75rem", "margin": "0"}),
                    ],
                    style={"textAlign": "center", "flex": "1"},
                ),
                html.Div(
                    [
                        html.Span("8", style={"fontSize": "1.5rem", "fontWeight": "bold", "color": "#27ae60"}),
                        html.P("Projects", style={"color": "#8899aa", "fontSize": "0.75rem", "margin": "0"}),
                    ],
                    style={"textAlign": "center", "flex": "1"},
                ),
                html.Div(
                    [
                        html.Span("6", style={"fontSize": "1.5rem", "fontWeight": "bold", "color": "#f39c12"}),
                        html.P("Opportunities", style={"color": "#8899aa", "fontSize": "0.75rem", "margin": "0"}),
                    ],
                    style={"textAlign": "center", "flex": "1"},
                ),
            ],
            style={"display": "flex", "padding": "0.5rem"},
        ),
    ],
    style=SIDEBAR_STYLE,
)




def get_entity(entity_id):
    return next((entity for entity in ENTITIES if entity["id"] == entity_id), None)


def get_entity_contacts(entity_id):
    return [contact for contact in CONTACTS if contact["entity"] == entity_id]


def get_entity_projects(entity_id):
    return [project for project in PROJECTS if project["entity"] == entity_id]


def get_entity_contracts(entity_id):
    return [contract for contract in CONTRACTS if contract["entity"] == entity_id]


def get_entity_opportunities(entity_id):
    return [opportunity for opportunity in OPPORTUNITIES if opportunity["entity"] == entity_id]


def get_related_entities(entity_id):
    entity = get_entity(entity_id)
    if not entity:
        return []

    relatives = []
    parent_id = entity.get("parent")
    child_ids = {child["id"] for child in ENTITIES if child.get("parent") == entity_id}

    for candidate in ENTITIES:
        if candidate["id"] == entity_id:
            continue
        if candidate["id"] == parent_id or candidate["id"] in child_ids or candidate.get("parent") == parent_id:
            relatives.append(candidate)

    return relatives


def build_teams_meeting_link(entity):
    agenda = [
        f"Client: {entity['name']}",
        "Agenda:",
        "1. Business updates and leadership priorities",
        "2. Current delivery risks and service gaps",
        "3. Next-best opportunities and follow-up owners",
        "Recording + transcription requested",
    ]

    subject = quote(f"CLA relationship review | {entity['name']}")
    body = quote("\n".join(agenda))

    start = quote((datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"))
    end = quote((datetime.now() + timedelta(days=2, hours=1)).strftime("%Y-%m-%dT%H:%M:%S"))

    return (
        "https://outlook.office.com/calendar/0/deeplink/compose"
        f"?subject={subject}"
        f"&body={body}"
        f"&startdt={start}"
        f"&enddt={end}"
        "&allday=false"
        "&path=/calendar/action/compose"
        "&rru=addevent"
    )


def build_mailto_link(entity):
    contacts = get_entity_contacts(entity["id"])
    primary_contact = contacts[0]["email"] if contacts else ""
    subject = quote(f"Follow-up planning for {entity['name']}")
    body = quote(
        "We would like to schedule a structured client conversation covering current priorities, service gaps, and next steps.\n\n"
        "Please let us know a few available times for a Teams meeting."
    )
    return f"mailto:{primary_contact}?subject={subject}&body={body}"


def build_customer_summary_cards():
    def parse_m(rev):
        try:
            return int(rev.replace("$", "").replace("M", ""))
        except Exception:
            return 0

    total_revenue = sum(parse_m(entity["revenue"]) for entity in ENTITIES)
    total_hot = len([opportunity for opportunity in OPPORTUNITIES if opportunity["priority"] == "Hot"])

    return dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        html.P("Portfolio Revenue", style={"color": "#8899aa", "fontSize": "0.8rem", "marginBottom": "0.2rem"}),
                        html.H2(f"${total_revenue}M", style={"color": "#4fc3f7", "marginBottom": "0"}),
                    ],
                    style=CARD_STYLE,
                ),
                xs=12,
                md=4,
            ),
            dbc.Col(
                html.Div(
                    [
                        html.P("Active Clients", style={"color": "#8899aa", "fontSize": "0.8rem", "marginBottom": "0.2rem"}),
                        html.H2(str(len(ENTITIES)), style={"color": "#27ae60", "marginBottom": "0"}),
                    ],
                    style=CARD_STYLE,
                ),
                xs=12,
                md=4,
            ),
            dbc.Col(
                html.Div(
                    [
                        html.P("Immediate Growth Plays", style={"color": "#8899aa", "fontSize": "0.8rem", "marginBottom": "0.2rem"}),
                        html.H2(str(total_hot), style={"color": "#f39c12", "marginBottom": "0"}),
                    ],
                    style=CARD_STYLE,
                ),
                xs=12,
                md=4,
            ),
        ],
        className="g-3 mb-4",
    )


def build_customer_cards():
    cards = []
    for entity in ENTITIES:
        entity_projects = get_entity_projects(entity["id"])
        entity_contacts = get_entity_contacts(entity["id"])
        entity_opportunities = get_entity_opportunities(entity["id"])
        next_priority = entity_opportunities[0]["title"] if entity_opportunities else "Relationship maintenance review"

        cards.append(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            entity["type"].upper(),
                                            className="badge",
                                            style={"backgroundColor": "#2a4a6b", "fontSize": "0.65rem", "marginRight": "0.5rem"},
                                        ),
                                        html.Span(entity["industry"], style={"color": "#9db5c8", "fontSize": "0.75rem"}),
                                    ]
                                ),
                                html.Span(entity["revenue"], style={"color": "#4fc3f7", "fontWeight": "bold", "fontSize": "0.95rem"}),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "gap": "0.75rem",
                                "flexWrap": "wrap",
                                "marginBottom": "0.75rem",
                            },
                        ),
                        html.H4(entity["name"], style={"color": "#fff", "marginBottom": "0.4rem", "fontSize": "1.2rem"}),
                        html.P(
                            f"Lead partner: {entity['relationship_lead']} | {entity['coverage_team']}",
                            style={"color": "#a8bac8", "fontSize": "0.85rem", "marginBottom": "0.75rem"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P("Projects", style={"color": "#6d8597", "fontSize": "0.72rem", "marginBottom": "0.1rem"}),
                                        html.H5(str(len(entity_projects)), style={"color": "#fff", "marginBottom": "0"}),
                                    ],
                                    style={"flex": "1", "minWidth": "90px"},
                                ),
                                html.Div(
                                    [
                                        html.P("Contacts", style={"color": "#6d8597", "fontSize": "0.72rem", "marginBottom": "0.1rem"}),
                                        html.H5(str(len(entity_contacts)), style={"color": "#fff", "marginBottom": "0"}),
                                    ],
                                    style={"flex": "1", "minWidth": "90px"},
                                ),
                                html.Div(
                                    [
                                        html.P("Opportunities", style={"color": "#6d8597", "fontSize": "0.72rem", "marginBottom": "0.1rem"}),
                                        html.H5(str(len(entity_opportunities)), style={"color": "#fff", "marginBottom": "0"}),
                                    ],
                                    style={"flex": "1", "minWidth": "90px"},
                                ),
                            ],
                            style={"display": "flex", "gap": "0.75rem", "marginBottom": "1rem", "flexWrap": "wrap"},
                        ),
                        html.Div(
                            [
                                html.P("Next scripted conversation focus", style={"color": "#6d8597", "fontSize": "0.72rem", "marginBottom": "0.25rem"}),
                                html.P(next_priority, style={"color": "#dbe7f0", "fontSize": "0.9rem", "marginBottom": "0"}),
                            ],
                            style={"backgroundColor": "#122131", "borderRadius": "10px", "padding": "0.85rem", "marginBottom": "1rem"},
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-arrow-right-circle me-2"), "Open Client Workspace"],
                            id={"type": "open-client", "entity": entity["id"]},
                            color="info",
                            className="w-100",
                            style={"borderRadius": "10px", "fontWeight": "bold"},
                        ),
                    ],
                    style={
                        **CARD_STYLE,
                        "height": "100%",
                        "background": "linear-gradient(180deg, #203244 0%, #172635 100%)",
                        "boxShadow": "0 18px 45px rgba(0, 0, 0, 0.18)",
                    },
                ),
                xs=12,
                md=6,
                xl=4,
                className="mb-3",
            )
        )

    return dbc.Row(cards, className="g-3")


