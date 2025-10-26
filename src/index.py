"""
Main entry point for the Bakery Market Basket Analysis Dash application.
Handles routing, navigation, and application layout.
"""

import sys
import os

# Add project root to path
sys.path.append('/home/kosala/git-repos/bread-basket/')

from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

from src.app import app, server
from src.pages import association_visualization, association_rules
from src.config import NAVBAR_COLOR, APP_HOST, APP_DEBUG


def create_navbar() -> dbc.Navbar:
    """
    Create the navigation bar component.
    
    Returns:
        dbc.Navbar component
    """
    dropdown = dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem(
                "Association Visualization",
                href="/association_visualization"
            ),
            dbc.DropdownMenuItem(
                "Association Rules",
                href="/association_rules"
            ),
        ],
        nav=True,
        in_navbar=True,
        label="Explore",
    )

    return dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src="/assets/icon.png", height="40px")),
                    dbc.Col(dbc.NavbarBrand(
                        "Bakery & Sons",
                        className="ml-3 font-jini"
                    )),
                ], align="center"),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav([dropdown], className="ml-auto", navbar=True),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]),
        color=NAVBAR_COLOR,
        dark=True,
        className="mb-4 navBar",
    )


def toggle_navbar_collapse(n_clicks: int, is_open: bool) -> bool:
    """
    Toggle navbar collapse state.
    
    Args:
        n_clicks: Number of clicks on toggle button
        is_open: Current open state
        
    Returns:
        New open state
    """
    return not is_open if n_clicks else is_open


# Register navbar toggle callback
app.callback(
    Output("navbar-collapse2", "is_open"),
    [Input("navbar-toggler2", "n_clicks")],
    [State("navbar-collapse2", "is_open")],
)(toggle_navbar_collapse)

# Define application layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    create_navbar(),
    html.Div(id='page-content')
], style={"background": "#E4E5E0"})


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname: str):
    """
    Route to appropriate page based on URL pathname.
    
    Args:
        pathname: URL pathname
        
    Returns:
        Page layout
    """
    if pathname == '/association_visualization':
        return association_visualization.layout
    elif pathname == '/association_rules':
        return association_rules.layout
    else:
        return association_rules.layout


if __name__ == '__main__':
    app.run(host=APP_HOST, debug=APP_DEBUG)