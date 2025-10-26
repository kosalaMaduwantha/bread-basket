"""
Utility functions for the Bakery Market Basket Analysis application.
Contains reusable helper functions for data processing and visualization.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd


def frozenset_to_list(frozen_set) -> List[str]:
    """
    Convert a frozenset to a list of strings.
    
    Args:
        frozen_set: A frozenset object
        
    Returns:
        List of strings
    """
    return list(frozen_set) if isinstance(frozen_set, frozenset) else [str(frozen_set)]


def remove_vowels(text: str) -> str:
    """
    Remove vowels from a string (used for node IDs in network graphs).
    
    Args:
        text: Input string
        
    Returns:
        String with vowels removed
    """
    vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
    return ''.join(char for char in text if char not in vowels)


def create_cytoscape_elements(
    antecedents: List[str],
    consequents: List[str]
) -> List[Dict[str, Any]]:
    """
    Create Cytoscape graph elements from antecedents and consequents.
    
    Args:
        antecedents: List of antecedent items
        consequents: List of consequent items
        
    Returns:
        List of Cytoscape element dictionaries
    """
    # Get unique items
    unique_items = list(set(antecedents + consequents))
    
    # Create node elements
    elements = []
    for item in unique_items:
        elements.append({
            'data': {
                'id': remove_vowels(item),
                'label': item
            }
        })
    
    # Create edge elements
    for ant, cons in zip(antecedents, consequents):
        elements.append({
            'data': {
                'source': remove_vowels(ant),
                'target': remove_vowels(cons)
            }
        })
    
    return elements


def extract_items_from_rules(rules: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Extract antecedents and consequents from association rules.
    
    Args:
        rules: DataFrame containing association rules
        
    Returns:
        Tuple of (antecedents_list, consequents_list)
    """
    antecedents = []
    consequents = []
    
    for _, row in rules.iterrows():
        ant = frozenset_to_list(row['antecedents'])[0]
        cons = frozenset_to_list(row['consequents'])[0]
        antecedents.append(ant)
        consequents.append(cons)
    
    return antecedents, consequents


def filter_dataframe_by_column(
    df: pd.DataFrame,
    column: str,
    value: Any
) -> pd.DataFrame:
    """
    Filter DataFrame by column value.
    
    Args:
        df: DataFrame to filter
        column: Column name
        value: Value to filter by
        
    Returns:
        Filtered DataFrame
    """
    return df[df[column] == value].copy()


def validate_file_exists(file_path: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file exists, False otherwise
    """
    import os
    return os.path.exists(file_path)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value to return if division fails
        
    Returns:
        Result of division or default value
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default
