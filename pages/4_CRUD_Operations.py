"""
CRUD Operations page – Create, Read, Update, Delete for Players (and view Matches).
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.db_connection import execute_query, execute_write, DB_PATH

st.set_page_config(page_title="CRUD | Cricbuzz LiveStats", page_icon="✏️", layout="wide")

st.title("✏️ CRUD Operations")
st.caption("Manage player records in the local database")

if not DB_PATH.exists():
    st.error("Database not found. Initialise it from the Home page first.")
    st.stop()

tab_read, tab_create, tab_update, tab_delete = st.tabs([
    "📖 Read / Search",
    "➕ Create",
    "📝 Update",
    "🗑️ Delete",
])

ROLES = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
BAT_STYLES = ["Right-hand bat", "Left-hand bat"]
BOWL_STYLES = [
    "Right-arm fast", "Right-arm fast-medium", "Right-arm medium",
    "Left-arm fast", "Left-arm fast-medium", "Left-arm orthodox",
    "Right-arm offbreak", "Right-arm legbreak", "Left-arm chinaman", None
]

# -------------------- READ --------------------
with tab_read:
    st.subheader("Browse & Search Players")
    col1, col2, col3 = st.columns(3)
    with col1:
        search_name = st.text_input("Name contains", "")
    with col2:
        filter_country = st.selectbox("Country", ["All"] + sorted({r["country"] for r in execute_query("SELECT DISTINCT country FROM players WHERE country IS NOT NULL")}))
    with col3:
        filter_role = st.selectbox("Role", ["All"] + ROLES)

    sql = "SELECT player_id, full_name, playing_role, batting_style, bowling_style, country, date_of_birth, is_active FROM players WHERE 1=1"
    params = []
    if search_name:
        sql += " AND full_name LIKE ?"
        params.append(f"%{search_name}%")
    if filter_country != "All":
        sql += " AND country = ?"
        params.append(filter_country)
    if filter_role != "All":
        sql += " AND playing_role = ?"
        params.append(filter_role)
    sql += " ORDER BY full_name LIMIT 200"

    rows = execute_query(sql, tuple(params))
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    st.caption(f"Showing {len(df)} players")

# -------------------- CREATE --------------------
with tab_create:
    st.subheader("Add New Player")
    with st.form("create_player"):
        full_name = st.text_input("Full Name *")
        col_a, col_b = st.columns(2)
        with col_a:
            playing_role = st.selectbox("Playing Role", ROLES)
            batting_style = st.selectbox("Batting Style", BAT_STYLES)
            country = st.text_input("Country", "India")
        with col_b:
            bowling_style = st.selectbox("Bowling Style", [s for s in BOWL_STYLES if s] + ["None"])
            dob = st.date_input("Date of Birth", value=None)
            is_active = st.checkbox("Active", value=True)

        submitted = st.form_submit_button("➕ Create Player", type="primary")
        if submitted:
            if not full_name.strip():
                st.error("Full Name is required.")
            else:
                try:
                    result = execute_write(
                        """INSERT INTO players
                           (full_name, playing_role, batting_style, bowling_style, country, date_of_birth, is_active)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (
                            full_name.strip(),
                            playing_role,
                            batting_style,
                            None if bowling_style == "None" else bowling_style,
                            country.strip(),
                            str(dob) if dob else None,
                            1 if is_active else 0,
                        ),
                    )
                    st.success(f"Player created successfully (ID: {result['lastrowid']})")
                except Exception as e:
                    st.error(f"Insert failed: {e}")

# -------------------- UPDATE --------------------
with tab_update:
    st.subheader("Update Existing Player")
    all_players = execute_query("SELECT player_id, full_name FROM players ORDER BY full_name")
    options = {f"{p['full_name']} (ID {p['player_id']})": p["player_id"] for p in all_players}
    selected = st.selectbox("Select player to update", list(options.keys()))
    pid = options[selected]

    current = execute_query("SELECT * FROM players WHERE player_id = ?", (pid,), fetch="one")
    if current:
        with st.form("update_player"):
            full_name = st.text_input("Full Name", current["full_name"])
            col_a, col_b = st.columns(2)
            with col_a:
                playing_role = st.selectbox("Playing Role", ROLES, index=ROLES.index(current["playing_role"]) if current["playing_role"] in ROLES else 0)
                batting_style = st.selectbox("Batting Style", BAT_STYLES, index=BAT_STYLES.index(current["batting_style"]) if current["batting_style"] in BAT_STYLES else 0)
                country = st.text_input("Country", current["country"] or "")
            with col_b:
                bowl_opts = [s for s in BOWL_STYLES if s] + ["None"]
                current_bowl = current["bowling_style"] or "None"
                bowling_style = st.selectbox("Bowling Style", bowl_opts, index=bowl_opts.index(current_bowl) if current_bowl in bowl_opts else len(bowl_opts)-1)
                is_active = st.checkbox("Active", value=bool(current["is_active"]))

            submitted = st.form_submit_button("💾 Save Changes", type="primary")
            if submitted:
                try:
                    execute_write(
                        """UPDATE players
                           SET full_name=?, playing_role=?, batting_style=?, bowling_style=?,
                               country=?, is_active=?
                           WHERE player_id=?""",
                        (
                            full_name.strip(),
                            playing_role,
                            batting_style,
                            None if bowling_style == "None" else bowling_style,
                            country.strip(),
                            1 if is_active else 0,
                            pid,
                        ),
                    )
                    st.success("Player updated successfully.")
                except Exception as e:
                    st.error(f"Update failed: {e}")

# -------------------- DELETE --------------------
with tab_delete:
    st.subheader("Delete Player")
    st.warning("Deleting a player will also remove related batting/bowling/fielding/partnership records if foreign-key cascades are active. Proceed with caution.")

    all_players = execute_query("SELECT player_id, full_name, country FROM players ORDER BY full_name")
    options = {f"{p['full_name']} ({p['country']}) – ID {p['player_id']}": p["player_id"] for p in all_players}
    selected = st.selectbox("Select player to delete", list(options.keys()), key="del_select")
    pid = options[selected]

    confirm = st.checkbox("I understand this action cannot be undone")
    if st.button("🗑️ Delete Player", type="primary", disabled=not confirm):
        try:
            # Clean dependent rows first (SQLite FK may not cascade depending on pragma)
            for table in ["batting_stats", "bowling_stats", "fielding_stats", "match_players"]:
                execute_write(f"DELETE FROM {table} WHERE player_id = ?", (pid,))
            execute_write("DELETE FROM partnerships WHERE player1_id = ? OR player2_id = ?", (pid, pid))
            result = execute_write("DELETE FROM players WHERE player_id = ?", (pid,))
            if result["rowcount"]:
                st.success("Player and related records deleted.")
            else:
                st.info("No rows deleted.")
        except Exception as e:
            st.error(f"Delete failed: {e}")
