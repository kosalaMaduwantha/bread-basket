"""
Data loading and processing utilities for the Bakery Market Basket Analysis.
Centralizes all data loading operations to avoid redundant reads.
"""

import pickle
import pandas as pd
from typing import Optional
from mlxtend.frequent_patterns import association_rules
from src.config import (
    BAKERY_INITIAL_MODEL,
    FINAL_APRIORI_MODEL,
    LIFT_THRESHOLD,
    COLS_KEEP,
    COLS_DROP
)


class DataLoader:
    """Singleton class to load and cache model data."""
    
    _instance = None
    _initial_model = None
    _apriori_model = None
    _rules = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
        return cls._instance
    
    def load_initial_model(self) -> pd.DataFrame:
        """Load the initial bakery data model."""
        if self._initial_model is None:
            with open(BAKERY_INITIAL_MODEL, 'rb') as f:
                self._initial_model = pickle.load(f)
        return self._initial_model
    
    def load_apriori_model(self) -> pd.DataFrame:
        """Load the final Apriori model."""
        if self._apriori_model is None:
            with open(FINAL_APRIORI_MODEL, 'rb') as f:
                self._apriori_model = pickle.load(f)
        return self._apriori_model
    
    def get_association_rules(self) -> pd.DataFrame:
        """Get association rules from the Apriori model."""
        if self._rules is None:
            apriori_model = self.load_apriori_model()
            self._rules = association_rules(
                apriori_model,
                metric='lift',
                min_threshold=LIFT_THRESHOLD
            )
        return self._rules.copy()
    
    def reset_cache(self):
        """Reset all cached data."""
        self._initial_model = None
        self._apriori_model = None
        self._rules = None


def get_item_counts(top_n: int = 10) -> pd.DataFrame:
    """
    Get count of items from the initial model.
    
    Args:
        top_n: Number of top items to return
        
    Returns:
        DataFrame with items and their counts
    """
    loader = DataLoader()
    model = loader.load_initial_model()
    count_items = model.Item.value_counts()[:top_n]
    return pd.DataFrame({
        'items': count_items.index,
        'count': count_items.values
    })


def get_item_percentages(top_n: int = 10) -> pd.DataFrame:
    """
    Get percentage distribution of items from the initial model.
    
    Args:
        top_n: Number of top items to return
        
    Returns:
        DataFrame with items and their percentages
    """
    loader = DataLoader()
    model = loader.load_initial_model()
    percentage_items = model.Item.value_counts(normalize=True)[:top_n]
    return pd.DataFrame({
        'items': percentage_items.index,
        'percentage': percentage_items.values
    })


def format_rules_dataframe(
    rules: pd.DataFrame,
    sort_by: str = 'lift',
    ascending: bool = False
) -> pd.DataFrame:
    """
    Format association rules DataFrame for display.
    
    Args:
        rules: Raw association rules DataFrame
        sort_by: Column to sort by
        ascending: Sort order
        
    Returns:
        Formatted DataFrame
    """
    formatted = rules.rename(columns=COLS_KEEP)
    formatted = formatted.drop(columns=COLS_DROP, errors='ignore')
    formatted = formatted.sort_values(by=[sort_by], ascending=ascending)
    
    # Convert frozensets to strings
    if 'antecedents' in formatted.columns:
        formatted['antecedents'] = formatted['antecedents'].apply(
            lambda x: ','.join(list(x)) if isinstance(x, frozenset) else str(x)
        )
    if 'consequents' in formatted.columns:
        formatted['consequents'] = formatted['consequents'].apply(
            lambda x: ','.join(list(x)) if isinstance(x, frozenset) else str(x)
        )
    
    return formatted


def get_recommended_associations(
    min_lift: float = 1,
    min_confidence: float = 0.2
) -> pd.DataFrame:
    """
    Get recommended item associations based on lift and confidence thresholds.
    
    Args:
        min_lift: Minimum lift value
        min_confidence: Minimum confidence value
        
    Returns:
        DataFrame with recommended associations
    """
    loader = DataLoader()
    rules = loader.get_association_rules()
    
    # Filter by lift and confidence
    filtered_rules = rules[
        (rules['lift'] > min_lift) &
        (rules['confidence'] >= min_confidence)
    ]
    
    return format_rules_dataframe(filtered_rules)


def get_pivot_for_heatmap() -> pd.DataFrame:
    """
    Create a pivot table for heatmap visualization.
    
    Returns:
        Pivot DataFrame with antecedents as index, consequents as columns
    """
    loader = DataLoader()
    rules = loader.get_association_rules()
    formatted = format_rules_dataframe(rules)
    
    return formatted.pivot(
        index='antecedents',
        columns='consequents',
        values='lift'
    )
