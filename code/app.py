import streamlit as st
import pandas as pd
import plotly.express as px
import os

@st.cache_data
def load_data():
    """Load and validate the data with proper error handling"""
    try:
        # Construct path
        script_dir = os.path.dirname(__file__)
        csv_path = os.path.join(script_dir, "..", "cache", "processed", "seriea_standings_clean.csv")
        
        # Read CSV with explicit formatting
        df = pd.read_csv(
            csv_path,
            header=0,        # First row is header
            skipinitialspace=True,  # Ignore spaces after commas
            quotechar='"',   # Handle quoted team names
            engine='python'  # More flexible parser
        )
        
        # Clean column names (remove \n and other artifacts)
        df.columns = df.columns.str.strip()
        
        # Validate required columns
        required = ['team', 'points', 'goalDifference']
        if not all(col in df.columns for col in required):
            st.error(f"Missing required columns. Needed: {required}, Found: {list(df.columns)}")
            return pd.DataFrame()
            
        return df

    except Exception as e:
        st.error(f"Failed to load data: {str(e)}")
        return pd.DataFrame()

def main():
    st.title("Serie A Standings Dashboard")
    
    df = load_data()
    if df.empty:
        st.warning("No data available - check CSV file format")
        return
    
    # Show raw data for debugging
    if st.checkbox("Show raw data"):
        st.write("CSV Contents:", df)
    
    # Standings Table
    st.subheader("Current Standings")
    st.dataframe(df.sort_values("points", ascending=False))
    
    # Points Visualization
    st.subheader("Points Distribution")
    try:
        fig = px.bar(
            df.sort_values("points", ascending=False),
            x="team", y="points", color="points",
            title="Team Points"
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Points chart error: {str(e)}")
    
    # Goal Difference Visualization
    st.subheader("Goal Difference")
    try:
        # Ensure numeric data
        df['goalDifference'] = pd.to_numeric(df['goalDifference'], errors='coerce')
        
        fig = px.scatter(
            df.sort_values("points", ascending=False),
            x="team", y="goalDifference", size="points",
            title="Goal Difference vs Points",
            hover_data=['points']
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Goal difference chart error: {str(e)}")

if __name__ == "__main__":
    main()