"""
Configuration file for the Bakery Market Basket Analysis application.
Contains all constants, file paths, and configuration parameters.
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
MODELS_DIR = os.path.join(SRC_DIR, 'models')
ASSETS_DIR = os.path.join(SRC_DIR, 'assets')

# Model file paths
BAKERY_INITIAL_MODEL = os.path.join(MODELS_DIR, 'bakery_initial.sav')
FINAL_APRIORI_MODEL = os.path.join(MODELS_DIR, 'final_model_appriori.sav')

# Association rules parameters
LIFT_THRESHOLD = 0.1
MIN_LIFT = 1
MIN_CONFIDENCE = 0.2

# Display parameters
TOP_N_ITEMS = 10
TOP_N_ASSOCIATIONS = 10

# App configuration
APP_HOST = '127.0.0.1'
APP_PORT = 8050
APP_DEBUG = True

# Color scheme
NAVBAR_COLOR = "#796b56"
CARD_HEADER_COLOR = "#6495ED"
CARD_SECONDARY_COLOR = "#F08080"
NODE_COLOR = '#BFD7B5'
EDGE_COLOR = '#A3C4BC'

# Column mappings
COLS_KEEP = {
    'antecedents': 'antecedents',
    'consequents': 'consequents',
    'support': 'support',
    'confidence': 'confidence',
    'lift': 'lift'
}

COLS_DROP = ['antecedent support', 'consequent support', 'leverage', 'conviction']

# Network graph stylesheet
DEFAULT_CYTOSCAPE_STYLESHEET = [
    {
        'selector': 'node',
        'style': {
            'background-color': NODE_COLOR,
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': EDGE_COLOR
        }
    }
]
