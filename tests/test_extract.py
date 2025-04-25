import pytest
from code.extract import fetch_seriea_standings, save_raw_data
import pandas as pd
import os

def test_fetch_standings(monkeypatch):
    """Mock API response to test standings fetch"""
    class MockResponse:
        def json(self):
            return {
                "standings": [{
                    "table": [{"team": {"name": "Juventus"}, "points": 70}]
                }]
            }
    
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())
    standings = fetch_seriea_standings("dummy_key")
    assert standings.iloc[0]["team"] == "Juventus"