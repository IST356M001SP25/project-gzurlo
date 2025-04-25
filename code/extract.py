import requests
import pandas as pd
import os

def fetch_seriea_standings(api_key):
    """Fetch current Serie A standings from Football-Data API"""
    url = "https://api.football-data.org/v4/competitions/SA/standings"
    headers = {"X-Auth-Token": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        data = response.json()
        standings = data["standings"][0]["table"]
        df = pd.DataFrame(standings)
        df["team"] = df["team"].apply(lambda x: x["name"])
        return df[["position", "team", "playedGames", "won", "draw", "lost", "points", "goalsFor", "goalsAgainst", "goalDifference"]]
    except Exception as e:
        raise Exception(f"Failed to fetch standings: {str(e)}")

def save_raw_data(df, filename):
    """Save raw data to cache with proper directory handling"""
    cache_dir = "cache/raw"
    
    # Remove any existing file named 'raw'
    if os.path.exists(cache_dir) and not os.path.isdir(cache_dir):
        os.remove(cache_dir)
    
    # Create directory (including parent directories if needed)
    os.makedirs(cache_dir, exist_ok=True)
    
    # Save the file
    df.to_csv(f"{cache_dir}/{filename}.csv", index=False)

if __name__ == "__main__":
    try:
        API_KEY = "69866da051d3469cada34de600c6fb3f"  # Replace with your actual API key
        standings = fetch_seriea_standings(API_KEY)
        save_raw_data(standings, "seriea_standings")
        print("✅ Data successfully fetched and saved to cache/raw/seriea_standings.csv")
        print(standings.head())
    except Exception as e:
        print(f"❌ Error: {str(e)}")