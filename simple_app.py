import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Create simple sample data for demonstration
sample_data = pd.DataFrame({
    'Item': ['Coffee', 'Bread', 'Cake', 'Tea', 'Pastry', 'Sandwich', 'Muffin', 'Juice', 'Cookie', 'Salad'],
    'Count': [120, 95, 80, 75, 65, 60, 45, 40, 35, 30]
})

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Bakery Market Basket Analysis", className="text-center mb-4"), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H3("Item Sales Count"),
                dcc.Graph(id='item-chart')
            ], width=12)
        ])
    ])
])

# Callback for updating the chart
@app.callback(
    Output('item-chart', 'figure'),
    [Input('item-chart', 'id')]
)
def update_chart(_):
    fig = px.bar(sample_data, x='Item', y='Count', 
                 title='Bakery Item Sales Count',
                 labels={'Count': 'Number of Sales', 'Item': 'Bakery Items'})
    fig.update_layout(template='plotly_white')
    return fig

if __name__ == '__main__':
    print("Starting Dash application...")
    print("Open your browser and go to: http://127.0.0.1:8050")
    app.run_server(host='127.0.0.1', port=8050, debug=True)