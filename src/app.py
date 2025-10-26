"""
Main Dash application configuration.
Initializes the Dash app with Bootstrap theme and configuration settings.
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

# Bootstrap theme - https://bootswatch.com/lux/
EXTERNAL_STYLESHEETS = [dbc.themes.LUX]

# Meta tags for responsive design
META_TAGS = [{
    'name': 'viewport',
    'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'
}]

# Initialize Dash application
app = dash.Dash(
    __name__,
    meta_tags=META_TAGS,
    assets_external_path='assets/',
    external_stylesheets=EXTERNAL_STYLESHEETS,
    suppress_callback_exceptions=True
)

# Expose server for deployment
server = app.server

