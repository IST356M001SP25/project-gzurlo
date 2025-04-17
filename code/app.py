import streamlit as st
import pandas as pd
import plotly.express as px

# Load processed data
@st.cache_data
def load_data():
    return pd.read_csv("cache/processed/seriea_standings_clean.csv")

def main():
    st.title("Serie A Standings Dashboard")
    df = load_data()

    # Show table
    st.subheader("Current Standings")
    st.dataframe(df)

    # Interactive bar chart
    st.subheader("Points Distribution")
    fig = px.bar(df, x="team", y="points", color="points")
    st.plotly_chart(fig)

    # Goal difference visualization
    st.subheader("Goal Difference")
    fig2 = px.scatter(df, x="team", y="goalDifference", size="points")
    st.plotly_chart(fig2)

if __name__ == "__main__":
    main()