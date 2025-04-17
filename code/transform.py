import pandas as pd
import os

def clean_standings_data(df):
    """Clean and structure standings data"""
    df = df[["position", "team", "points", "won", "draw", "lost", "goalsFor", "goalsAgainst"]]
    df["goalDifference"] = df["goalsFor"] - df["goalsAgainst"]
    return df

def save_processed_data(df, filename):
    """Save processed data to cache"""
    os.makedirs("cache/processed", exist_ok=True)
    df.to_csv(f"cache/processed/{filename}.csv", index=False)

if __name__ == "__main__":
    raw_df = pd.read_csv("cache/raw/seriea_standings.csv")
    clean_df = clean_standings_data(raw_df)
    save_processed_data(clean_df, "seriea_standings_clean")
    print("Data cleaned and saved!")