"""
Helper Functions
================

Utility functions used across the project.
"""

import numpy as np
from typing import Dict, List, Tuple


def print_header(text: str, width: int = 80, char: str = "=") -> None:
    """Print a formatted header."""
    print("\n" + char * width)
    print(text)
    print(char * width)


def print_subheader(text: str, width: int = 80, char: str = "-") -> None:
    """Print a formatted subheader."""
    print("\n" + char * width)
    print(text)
    print(char * width)


def format_number(num: float, decimal_places: int = 2) -> str:
    """Format a number with thousand separators."""
    if isinstance(num, int) or num.is_integer():
        return f"{int(num):,}"
    return f"{num:,.{decimal_places}f}"


def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage safely."""
    if total == 0:
        return 0.0
    return (part / total) * 100


def get_top_k(dictionary: Dict, k: int = 10, reverse: bool = True) -> List[Tuple]:
    """Get top k items from dictionary sorted by value."""
    return sorted(dictionary.items(), key=lambda x: x[1], reverse=reverse)[:k]


def truncate_name(name: str, max_length: int = 20) -> str:
    """Truncate a name to max_length characters."""
    if len(name) <= max_length:
        return name
    return name[:max_length-3] + "..."


def set_random_seed(seed: int) -> None:
    """Set random seed for reproducibility."""
    np.random.seed(seed)
