"""
Helper functions for association rule analysis.
This module is deprecated - functionality moved to data_loader.py and utils.py
"""

import warnings

warnings.warn(
    "This module is deprecated. Use src.data_loader and src.utils instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import for backward compatibility
from src.data_loader import (
    DataLoader,
    get_item_counts,
    get_item_percentages,
    get_recommended_associations
)
from src.utils import (
    frozenset_to_list,
    remove_vowels,
    create_cytoscape_elements
)

__all__ = [
    'DataLoader',
    'get_item_counts',
    'get_item_percentages',
    'get_recommended_associations',
    'frozenset_to_list',
    'remove_vowels',
    'create_cytoscape_elements'
]



