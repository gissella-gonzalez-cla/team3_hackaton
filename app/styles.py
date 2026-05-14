"""Style constants and routing maps for the CLA app."""

PAGE_TO_PATH = {
    "my-customers": "/",
    "entity": "/entity",
    "opportunities": "/opportunities",
    "contacts": "/contacts",
    "projects": "/projects",
    "contracts": "/contracts",
    "client-detail": "/client",
}

PATH_TO_PAGE = {v: k for k, v in PAGE_TO_PATH.items()}



SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "260px",
    "padding": "1rem",
    "backgroundColor": "#1a2332",
    "overflowY": "auto",
    "zIndex": 1000,
}

CONTENT_STYLE = {
    "marginLeft": "260px",
    "padding": "2rem",
    "backgroundColor": "#0f1724",
    "minHeight": "100vh",
}

CARD_STYLE = {
    "backgroundColor": "#1e2d3d",
    "border": "1px solid #2a3f55",
    "borderRadius": "12px",
    "padding": "1.5rem",
    "marginBottom": "1rem",
}

TAG_COLORS = {
    "Hot": "#e74c3c",
    "Warm": "#f39c12",
    "Watch": "#3498db",
    "Cold": "#95a5a6",
    "Strong": "#27ae60",
    "Moderate": "#f39c12",
    "Weak": "#e74c3c",
}

