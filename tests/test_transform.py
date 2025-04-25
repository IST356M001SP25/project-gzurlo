import sys
import os
import pytest
import pandas as pd

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code.transform import clean_standings_data, save_processed_data

def test_clean_standings():
    """Test if data is cleaned correctly"""
    # Create test data
    test_data = pd.DataFrame({
        "position": [1, 2],
        "team": ["Inter", "Milan"],
        "points": [75, 70],
        "won": [23, 21],
        "draw": [6, 7],
        "lost": [5, 6],
        "goalsFor": [70, 65],
        "goalsAgainst": [25, 30]
    })
    
    # Clean the data
    cleaned = clean_standings_data(test_data)
    
    # Test assertions
    assert "goalDifference" in cleaned.columns
    assert cleaned.shape == (2, 9)  # 2 rows, 9 columns (original 8 + new 1)
    assert cleaned.iloc[0]["goalDifference"] == 45  # 70-25=45
    assert cleaned.iloc[1]["goalDifference"] == 35  # 65-30=35
    assert list(cleaned.columns) == [
        "position", "team", "points", "won", "draw", "lost",
        "goalsFor", "goalsAgainst", "goalDifference"
    ]

def test_save_processed_data(tmp_path):
    """Test if data is saved correctly"""
    # Create test data
    test_data = pd.DataFrame({
        "position": [1],
        "team": ["Inter"],
        "points": [75],
        "goalDifference": [45]
    })
    
    # Create temp directory
    test_dir = tmp_path / "processed"
    
    # Test saving
    save_processed_data(test_data, "test_output", str(test_dir))
    
    # Verify file was created
    output_path = test_dir / "test_output.csv"
    assert output_path.exists()
    
    # Verify content
    saved_data = pd.read_csv(output_path)
    assert saved_data.equals(test_data)

def test_clean_standings_missing_columns():
    """Test handling of missing columns"""
    with pytest.raises(ValueError):
        # Missing required columns
        test_data = pd.DataFrame({
            "position": [1],
            "team": ["Inter"]
        })
        clean_standings_data(test_data)