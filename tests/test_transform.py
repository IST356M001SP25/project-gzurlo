import pytest
from code.transform import clean_standings_data, save_processed_data
import pandas as pd
import os

def test_clean_standings():
    """Test if data is cleaned correctly"""
    test_data = pd.DataFrame({
        "position": [1], "team": ["Inter"], "points": [75],
        "won": [23], "draw": [6], "lost": [5],
        "goalsFor": [70], "goalsAgainst": [25]
    })
    cleaned = clean_standings_data(test_data)
    assert "goalDifference" in cleaned.columns