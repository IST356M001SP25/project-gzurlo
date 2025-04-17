import requests
import pandas as pd
import os

def fetch_seriea_standings(api_key):
    """Fetch current Serie A standings from Football-Data API"""
    url = f"https://api.football-data.org/v4/competitions/SA/standings"
    headers = {"X-Auth-Token": api_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        standings = data["standings"][0]["table"]
        df = pd.DataFrame(standings)
        df["team"] = df["team"].apply(lambda x: x["name"])
        return df
    else:
        raise Exception(f"API Error: {response.status_code}")

def save_raw_data(df, filename):
    """Save raw data to cache"""
    os.makedirs("cache/raw", exist_ok=True)
    df.to_csv(f"cache/raw/{filename}.csv", index=False)

if __name__ == "__main__":
    API_KEY = "69866da051d3469cada34de600c6fb3f"  # Get from https://www.football-data.org/
    standings = fetch_seriea_standings(API_KEY)
    save_raw_data(standings, "seriea_standings")
    print("Data fetched and saved!")