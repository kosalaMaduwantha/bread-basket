"""
Association Rules page for the Bakery Market Basket Analysis.
Displays top associations and allows filtering by specific items.
"""

import pandas as pd
from dash import dcc, html, Input, Output, dash_table as dt
import dash_bootstrap_components as dbc

from src.app import app
from src.data_loader import DataLoader, get_recommended_associations, format_rules_dataframe
from src.config import (
    TOP_N_ASSOCIATIONS,
    MIN_LIFT,
    MIN_CONFIDENCE,
    CARD_HEADER_COLOR,
    CARD_SECONDARY_COLOR
)

# Initialize data loader
data_loader = DataLoader()

# Load and prepare data
rules = data_loader.get_association_rules()
recommendation = get_recommended_associations(MIN_LIFT, MIN_CONFIDENCE)
recommendation_items = get_recommended_associations(MIN_LIFT, MIN_CONFIDENCE)

# Get top items by consequent support
sorted_rules = rules.sort_values(
    ["consequent support"],
    ascending=False
).drop_duplicates(["consequent support"], keep='last')

top_confidence_items = format_rules_dataframe(
    sorted_rules,
    sort_by='confidence',
    ascending=False
)


def generate_item_card(item_data: pd.Series) -> dbc.Row:
    """
    Generate a card component for displaying an item.
    
    Args:
        item_data: Series containing item information
        
    Returns:
        dbc.Row component with card
    """
    return dbc.Row([
        dbc.Col(
            dbc.Card([
                html.H5(
                    children=item_data[1],
                    className="text-left text-dark bg-white text-nav"
                ),
                html.H6(
                    children=item_data[3],
                    className="text-left text-dark bg-white text-nav mt-2"
                )
            ], body=True, color="light", className="card-col-k"),
            className="mt-1 mb-1",
        )
    ])


def create_table_row(item_data: pd.Series) -> html.Tr:
    """
    Create a table row for association rules.
    
    Args:
        item_data: Series containing association rule data
        
    Returns:
        html.Tr component
    """
    return html.Tr([
        html.Td(html.P(item_data[0])),
        html.Td(item_data[1]),
        html.Td(item_data[3]),
        html.Td(item_data[4])
    ])


# Table components
TABLE_HEADER_CLASS = "main-topic-color"

table_header = [
    html.Thead(html.Tr([
        html.Th("antecedents", className=TABLE_HEADER_CLASS),
        html.Th("consequents", className=TABLE_HEADER_CLASS),
        html.Th("confidence", className=TABLE_HEADER_CLASS),
        html.Th("lift", className=TABLE_HEADER_CLASS)
    ]))
]

table_body = [
    html.Tbody([
        create_table_row(row)
        for _, row in recommendation.head(TOP_N_ASSOCIATIONS).iterrows()
    ])
]

table = dbc.Table(
    children=table_header + table_body,
    bordered=True,
    striped=True,
    hover=True
)

# Card content for top associations table
card_content = [
    dbc.CardHeader(
        html.H5("Highest selling combos", className=TABLE_HEADER_CLASS),
        className="card-header-k"
    ),
    dbc.CardBody(
        children=[html.P([table], className="card-text")],
        className="card-body-k"
    ),
]

# Card content for item-specific associations
card_content2 = [
    dbc.CardBody(
        children=[
            html.H2("Best Selling Combos", className="card-title main-topic-color"),
            html.P([html.Div(id="final_table")], className="card-text"),
        ],
        className="card-body-k"
    ),
]






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
                className="mb-2 mr-4"
            )
        ], className="main-topic"),
        
        # Sub topic
        dbc.Row([
            dbc.Col(
                html.H6(
                    children='Visualising Bakery Association rules',
                    className="main-topic-color"
                ),
                className="mb-2"
            )
        ], className="main-topic"),

        # Association rules header
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.H4(
                        children="Association rules",
                        className="text-center text-nav main-topic-color"
                    )
                ], body=True, color="light", className="card-col-main-row"),
                className="mt-2 mb-1",
            )
        ], className="main-row"),

        # Top confidence items and associations table
        dbc.Row([
            dbc.Col([
                generate_item_card(row)
                for _, row in top_confidence_items.head(10).iterrows()
            ], width=3),
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            children=card_content,
                            color=CARD_HEADER_COLOR,
                            outline=True,
                            className='card-k'
                        )
                    ),
                ])
            ], width=9, className="mt-1")
        ], className="f-card"),

        # Item association header
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.H4(
                        children="Item association",
                        className="text-center text-nav main-topic-color"
                    )
                ], body=True, color="light", className="card-col-main-row"),
                className="mt-5 mb-1",
            )
        ], className="main-row"),

        # Item selection and specific associations
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            html.H5(
                                children="Select an item",
                                className="text-left text-dark bg-white text-nav"
                            ),
                            dcc.Dropdown(
                                id='dropdown_d1',
                                options=[
                                    {'label': item, 'value': item}
                                    for item in recommendation_items['antecedents'].unique()
                                ],
                                value=None
                            ),
                            html.H3(
                                id="dyna-word",
                                className="text-left text-dark bg-white text-nav mt-4"
                            ),
                        ], body=True, color="light", className="card-col-k-2"),
                        className="mt-1 mb-1",
                    )
                ])
            ], width=3),
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            card_content2,
                            color=CARD_SECONDARY_COLOR,
                            outline=True,
                            className='card-k-2'
                        )
                    ),
                ])
            ], width=9, className="mt-1")
        ], className="f-card"),

    ], className="container-out")
])


# Callbacks
@app.callback(
    Output('final_table', 'children'),
    [Input('dropdown_d1', 'value')]
)
def update_table(selected_item: str):
    """
    Update the association table based on selected item.
    
    Args:
        selected_item: Selected item from dropdown
        
    Returns:
        DataTable component with filtered associations
    """
    if selected_item is None:
        return []
    
    filtered_df = recommendation_items[
        recommendation_items["antecedents"] == selected_item
    ]
    
    return [dt.DataTable(
        id='table',
        columns=[{"name": col, "id": col} for col in filtered_df.columns],
        data=filtered_df.to_dict('records'),
    )]


@app.callback(
    Output('dyna-word', 'children'),
    [Input('dropdown_d1', 'value')]
)
def update_text(selected_item: str):
    """
    Update the dynamic text based on selected item.
    
    Args:
        selected_item: Selected item from dropdown
        
    Returns:
        Selected item text or empty string
    """
    return selected_item if selected_item else ""







