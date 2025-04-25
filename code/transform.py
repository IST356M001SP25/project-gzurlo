import pandas as pd
import os

def clean_standings_data(df):
    """Clean and structure standings data with validation"""
    try:
        # Validate input columns
        required_cols = ["position", "team", "points", "won", "draw", "lost", "goalsFor", "goalsAgainst"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Select and calculate columns
        clean_df = df[required_cols].copy()
        clean_df["goalDifference"] = clean_df["goalsFor"] - clean_df["goalsAgainst"]
        
        # Ensure numeric columns are properly typed
        numeric_cols = ["position", "points", "won", "draw", "lost", "goalsFor", "goalsAgainst"]
        clean_df[numeric_cols] = clean_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        return clean_df
    
    except Exception as e:
        print(f"Error cleaning data: {str(e)}")
        raise

def save_processed_data(df, filename):
    """Save processed data to cache with directory validation"""
    try:
        # Handle case where 'processed' might be a file instead of directory
        processed_dir = "cache/processed"
        if os.path.exists(processed_dir) and not os.path.isdir(processed_dir):
            os.remove(processed_dir)
        
        os.makedirs(processed_dir, exist_ok=True)
        
        # Save with validation
        output_path = f"{processed_dir}/{filename}.csv"
        df.to_csv(output_path, index=False)
        print(f"✅ Data saved to {output_path}")
        
    except Exception as e:
        print(f"Error saving data: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Load raw data
        raw_path = "cache/raw/seriea_standings.csv"
        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Raw data file not found at {raw_path}")
        
        raw_df = pd.read_csv(raw_path)
        print("Raw data loaded successfully:")
        print(raw_df.head())
        
        # Clean data
        clean_df = clean_standings_data(raw_df)
        print("\nCleaned data:")
        print(clean_df.head())
        
        # Save processed data
        save_processed_data(clean_df, "seriea_standings_clean")
        
    except Exception as e:
        print(f"❌ Transformation failed: {str(e)}")