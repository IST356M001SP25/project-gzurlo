import sys
import os
import pytest
import pandas as pd
from unittest.mock import Mock, patch

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code.extract import fetch_seriea_standings, save_raw_data

def test_fetch_standings():
    """Test API response handling with mock"""
    # Create mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "standings": [{
            "table": [
                {
                    "position": 1,
                    "team": {"name": "Inter"},
                    "points": 75,
                    "won": 23,
                    "draw": 6,
                    "lost": 5,
                    "goalsFor": 70,
                    "goalsAgainst": 25
                }
            ]
        }]
    }

    with patch('requests.get', return_value=mock_response) as mock_get:
        # Call function with dummy API key
        standings = fetch_seriea_standings("dummy_key")
        
        # Verify requests was called correctly
        mock_get.assert_called_once_with(
            "https://api.football-data.org/v4/competitions/SA/standings",
            headers={"X-Auth-Token": "dummy_key"}
        )
        
        # Verify response handling
        assert isinstance(standings, pd.DataFrame)
        assert standings.iloc[0]["team"] == "Inter"
        assert standings.iloc[0]["points"] == 75
        assert list(standings.columns) == [
            "position", "team", "points", "won", "draw", "lost",
            "goalsFor", "goalsAgainst"
        ]

def test_fetch_standings_api_error():
    """Test API error handling"""
    mock_response = Mock()
    mock_response.status_code = 403  # Forbidden
    mock_response.json.return_value = {"message": "Invalid API key"}

    with patch('requests.get', return_value=mock_response):
        with pytest.raises(Exception, match="API Error: 403"):
            fetch_seriea_standings("invalid_key")

def test_save_raw_data(tmp_path):
    """Test file saving functionality"""
    # Create test data
    test_data = pd.DataFrame({
        "team": ["Inter", "Milan"],
        "points": [75, 70]
    })
    
    # Create temp directory
    test_dir = tmp_path / "raw"
    
    # Test saving
    save_raw_data(test_data, "test_standings", str(test_dir))
    
    # Verify file was created
    output_path = test_dir / "test_standings.csv"
    assert output_path.exists()
    
    # Verify content
    saved_data = pd.read_csv(output_path)
    assert saved_data.equals(test_data)

def test_save_raw_data_directory_handling(tmp_path):
    """Test directory creation handling"""
    test_data = pd.DataFrame({"team": ["Juventus"], "points": [70]})
    
    # Create a file that conflicts with directory name
    conflict_path = tmp_path / "raw"
    conflict_path.write_text("conflict")
    
    # Test saving (should handle the conflict)
    save_raw_data(test_data, "test_conflict", str(tmp_path))
    
    # Verify it worked
    assert (tmp_path / "raw").is_dir()
    assert pd.read_csv(tmp_path / "raw" / "test_conflict.csv").equals(test_data)