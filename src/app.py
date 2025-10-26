import dash
from dash import html
import dash_bootstrap_components as dbc
import os

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(
    __name__, 
    meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
    assets_external_path='assets/',
    external_stylesheets=external_stylesheets,
    
    )

server = app.server
app.config.suppress_callback_exceptions = True

