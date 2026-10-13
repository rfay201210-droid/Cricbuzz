"""
Top Player Stats – derived from the local SQLite database.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.db_connection import execute_query, DB_PATH

st.set_page_config(page_title="Top Stats | Cricbuzz LiveStats", page_icon="🏆", layout="wide")

st.title("🏆 Top Player Statistics")
st.caption("Leaderboards computed from the local cricket database")

if not DB_PATH.exists():
    st.error("Database not found. Please go to the Home page and initialise the database first.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs([
    "🏏 Most Runs",
    "🎯 Highest Scores",
    "🎳 Most Wickets",
    "📈 Batting Averages",
])

with tab1:
    st.subheader("Top Run Scorers (All Formats)")
    limit = st.slider("Show top N", 5, 30, 10, key="runs_limit")
    df = pd.DataFrame(execute_query(f"""
        SELECT p.full_name AS Player,
               p.country AS Country,
               p.playing_role AS Role,
               SUM(b.runs) AS Total_Runs,
               COUNT(DISTINCT b.match_id) AS Innings,
               ROUND(AVG(b.runs), 2) AS Average,
               ROUND(AVG(b.strike_rate), 2) AS Strike_Rate,
               SUM(CASE WHEN b.runs >= 100 THEN 1 ELSE 0 END) AS Centuries,
               SUM(CASE WHEN b.runs >= 50 AND b.runs < 100 THEN 1 ELSE 0 END) AS Fifties
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_id, p.full_name, p.country, p.playing_role
        ORDER BY Total_Runs DESC
        LIMIT {limit}
    """))
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        st.bar_chart(df.set_index("Player")["Total_Runs"])

with tab2:
    st.subheader("Highest Individual Scores")
    limit = st.slider("Show top N", 5, 30, 15, key="hs_limit")
    df = pd.DataFrame(execute_query(f"""
        SELECT p.full_name AS Player,
               b.runs AS Score,
               b.balls_faced AS Balls,
               b.strike_rate AS SR,
               m.match_format AS Format,
               m.match_date AS Date,
               m.match_description AS Match
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        ORDER BY b.runs DESC
        LIMIT {limit}
    """))
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("Leading Wicket Takers")
    limit = st.slider("Show top N", 5, 30, 10, key="wkt_limit")
    df = pd.DataFrame(execute_query(f"""
        SELECT p.full_name AS Player,
               p.country AS Country,
               SUM(bo.wickets) AS Wickets,
               ROUND(AVG(bo.economy), 2) AS Avg_Economy,
               ROUND(SUM(bo.runs_conceded) * 1.0 / NULLIF(SUM(bo.wickets), 0), 2) AS Bowling_Avg,
               COUNT(DISTINCT bo.match_id) AS Matches,
               ROUND(SUM(bo.overs), 1) AS Overs
        FROM bowling_stats bo
        JOIN players p ON bo.player_id = p.player_id
        GROUP BY p.player_id, p.full_name, p.country
        HAVING SUM(bo.wickets) > 0
        ORDER BY Wickets DESC
        LIMIT {limit}
    """))
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        st.bar_chart(df.set_index("Player")["Wickets"])

with tab4:
    st.subheader("Best Batting Averages (min 10 innings)")
    limit = st.slider("Show top N", 5, 30, 10, key="avg_limit")
    df = pd.DataFrame(execute_query(f"""
        SELECT p.full_name AS Player,
               p.country AS Country,
               ROUND(AVG(b.runs), 2) AS Batting_Average,
               SUM(b.runs) AS Total_Runs,
               COUNT(*) AS Innings,
               ROUND(AVG(b.strike_rate), 2) AS Strike_Rate
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY p.player_id, p.full_name, p.country
        HAVING COUNT(*) >= 10
        ORDER BY Batting_Average DESC
        LIMIT {limit}
    """))
    st.dataframe(df, use_container_width=True)
