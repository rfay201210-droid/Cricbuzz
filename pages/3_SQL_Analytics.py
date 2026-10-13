"""
SQL Queries & Analytics page – 25 practice questions + custom SQL runner.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.db_connection import execute_query, DB_PATH
from sql.queries import QUERIES, get_query_by_id

st.set_page_config(page_title="SQL Analytics | Cricbuzz LiveStats", page_icon="📊", layout="wide")

st.title("📊 SQL Queries & Analytics")
st.caption("25 practice questions (Beginner → Intermediate → Advanced) + free-form SQL")

if not DB_PATH.exists():
    st.error("Database not found. Please initialise it from the Home page.")
    st.stop()

tab_practice, tab_custom = st.tabs(["📝 Practice Questions (25)", "💻 Custom SQL"])

with tab_practice:
    levels = ["All", "Beginner", "Intermediate", "Advanced"]
    selected_level = st.selectbox("Filter by level", levels)

    filtered = QUERIES if selected_level == "All" else [q for q in QUERIES if q[1] == selected_level]

    q_options = {f"Q{q[0]} [{q[1]}] – {q[2]}": q[0] for q in filtered}
    choice = st.selectbox("Select a question", list(q_options.keys()))
    qid = q_options[choice]
    q = get_query_by_id(qid)

    st.markdown(f"### Question {q[0]} – {q[2]}")
    st.info(q[3])

    with st.expander("View SQL", expanded=True):
        st.code(q[4].strip(), language="sql")

    if st.button("▶️ Run Query", type="primary", key=f"run_{qid}"):
        try:
            with st.spinner("Executing..."):
                result = execute_query(q[4])
            if result:
                df = pd.DataFrame(result)
                st.success(f"Returned {len(df)} rows")
                st.dataframe(df, use_container_width=True)
                # Simple chart if numeric columns exist
                numeric_cols = df.select_dtypes(include="number").columns.tolist()
                if len(numeric_cols) >= 1 and len(df) <= 50:
                    label_col = df.columns[0]
                    st.bar_chart(df.set_index(label_col)[numeric_cols[0]])
            else:
                st.warning("Query returned no rows. (Sample data may not satisfy every filter.)")
        except Exception as e:
            st.error(f"Execution error: {e}")

with tab_custom:
    st.subheader("Write your own SQL")
    st.write("You can run any SELECT statement against the local database. Write operations are disabled here for safety.")

    default_sql = """SELECT p.full_name, p.playing_role, p.country,
       SUM(b.runs) AS total_runs
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
GROUP BY p.player_id
ORDER BY total_runs DESC
LIMIT 10;"""

    user_sql = st.text_area("SQL Query", value=default_sql, height=220)

    col_a, col_b = st.columns([1, 4])
    with col_a:
        run_btn = st.button("▶️ Execute", type="primary", key="custom_run")
    with col_b:
        st.caption("Only SELECT / WITH queries are allowed.")

    if run_btn:
        cleaned = user_sql.strip().lower()
        if not (cleaned.startswith("select") or cleaned.startswith("with")):
            st.error("Only SELECT (or CTE WITH) statements are permitted on this page.")
        else:
            try:
                result = execute_query(user_sql)
                if result:
                    df = pd.DataFrame(result)
                    st.success(f"{len(df)} rows returned")
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download CSV", csv, "query_result.csv", "text/csv")
                else:
                    st.info("Query returned 0 rows.")
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("### Schema Quick Reference")
with st.expander("Tables & key columns"):
    st.markdown("""
| Table | Key Columns |
|-------|-------------|
| **teams** | team_id, team_name, country, team_type |
| **players** | player_id, full_name, playing_role, batting_style, bowling_style, country |
| **venues** | venue_id, venue_name, city, country, capacity |
| **series** | series_id, series_name, host_country, match_type, start_date, total_matches |
| **matches** | match_id, series_id, team1_id, team2_id, venue_id, match_date, match_format, toss_winner_id, toss_decision, winner_id, victory_margin, victory_type, is_close_match |
| **batting_stats** | match_id, player_id, innings, runs, balls_faced, fours, sixes, strike_rate |
| **bowling_stats** | match_id, player_id, overs, runs_conceded, wickets, economy |
| **fielding_stats** | match_id, player_id, catches, stumpings, run_outs |
| **partnerships** | match_id, innings, player1_id, player2_id, runs, batting_pos1, batting_pos2 |
""")
