"""
Association Visualization page for the Bakery Market Basket Analysis.
Displays various visualizations including bar charts, heatmaps, and network graphs.
"""

import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto

from src.app import app
from src.data_loader import (
    DataLoader,
    get_item_counts,
    get_item_percentages,
    get_pivot_for_heatmap
)
from src.utils import create_cytoscape_elements, extract_items_from_rules
from src.config import TOP_N_ITEMS, DEFAULT_CYTOSCAPE_STYLESHEET

# Load data
data_loader = DataLoader()
count_items = get_item_counts(TOP_N_ITEMS)
percentage_items = get_item_percentages(TOP_N_ITEMS)
pivot = get_pivot_for_heatmap()

# Prepare network graph data
rules_raw = data_loader.get_association_rules()
antecedents_list, consequents_list = extract_items_from_rules(rules_raw)
network_elements = create_cytoscape_elements(antecedents_list, consequents_list)





# Layout
layout = html.Div([
    dbc.Container([
        # Main topic
        dbc.Row([
            dbc.Col(
                html.H1(
                    children='Bakery Market Basket',
                    className="main-topic-color"
                ),
                className="mb-2"
            )
        ], className="main-topic"),
        
        # Sub topic
        dbc.Row([
            dbc.Col(
                html.H6(
                    children='Visualising Bakery Transactions and association',
                    className="main-topic-color"
                ),
                className="mb-2"
            )
        ], className="main-topic"),

        # Bakery item count header
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.H4(
                        children="Bakery Item Count",
                        className="text-center text-nav main-topic-color"
                    )
                ], body=True, color="light", className="card-col-main-row"),
                className="mt-2 mb-1",
            )
        ], className="main-row"),

        # Count and percentage graphs
        dbc.Row([
            dbc.Col(dcc.Graph(id='count-bar'), width=6),
            dbc.Col(dcc.Graph(id='percentage-bar'), width=6)
        ], className="f-card"),

        # Heat map header
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.H4(
                        children="Visualization Of Association Rules",
                        className="text-center text-dark bg-white text-nav"
                    )
                ], body=True, color="light", className="card-col-main-row"),
                className="mt-5 mb-1",
            )
        ], className="main-row"),
        
        # Heat map
        dbc.Row([
            dbc.Col(dcc.Graph(id='graph-heat'))
        ], className="f-card"),

        # Network graph header
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.H4(
                        children="Visualization Of Association Rules Using Network Graph",
                        className="text-center text-dark bg-white text-nav"
                    )
                ], body=True, color="light", className="card-col-main-row"),
                className="mt-5 mb-1",
            )
        ], className="main-row"),
        
        # Network graph
        dbc.Row([
            dbc.Col(
                html.Div([
                    cyto.Cytoscape(
                        id='cytoscape',
                        elements=network_elements,
                        stylesheet=DEFAULT_CYTOSCAPE_STYLESHEET,
                        layout={'name': 'circle'},
                        style={'width': '80%', 'height': '500px'}
                    )
                ], style={"background": "white"})
            )
        ], className="f-card"),

    ], className="container-out")
])


# Callbacks
@app.callback(
    [
        Output(component_id='count-bar', component_property='figure'),
        Output(component_id='percentage-bar', component_property='figure')
    ],
    [Input('count-bar', 'hoverData')]
)
def update_bar_charts(hover_data):
    """
    Update count and percentage bar charts.
    
    Args:
        hover_data: Hover data from chart (not used but required for callback)
        
    Returns:
        Tuple of (count_figure, percentage_figure)
    """
    barchart_count = px.bar(
        data_frame=count_items,
        title='Total Number of Sales by Item',
        x='items',
        y='count',
        labels={"items": "Items", "count": "Count"}
    )
    barchart_count.layout.template = 'seaborn'

    barchart_percentage = px.bar(
        data_frame=percentage_items,
        title='Percentage of Sales by Item',
        x='items',
        y='percentage',
        labels={"items": "Items", "percentage": "Percentage"}
    )
    barchart_percentage.layout.template = 'seaborn'

    return barchart_count, barchart_percentage


@app.callback(
    Output("graph-heat", "figure"),
    [Input("graph-heat", "hoverData")]
)
def update_heatmap(hover_data):
    """
    Update the heatmap visualization.
    
    Args:
        hover_data: Hover data from heatmap (not used but required for callback)
        
    Returns:
        Plotly figure for heatmap
    """
    fig = px.imshow(
        pivot,
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Heat Map"
    )
    fig.update_layout(
        title_font={'size': 27},
        title_x=0.5,
        width=1254,
        height=800,
        template='seaborn'
    )
    fig.update_traces(
        hoverongaps=False,
        hovertemplate=(
            "antecedent: %{y}<br>"
            "consequent: %{x}<br>"
            "lift: %{z}<extra></extra>"
        )
    )

    return fig





