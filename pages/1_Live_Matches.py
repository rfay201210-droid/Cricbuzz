"""
Live Matches page – fetches data from Cricbuzz API via RapidAPI.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.api_client import (
    get_live_matches,
    get_recent_matches,
    get_upcoming_matches,
    get_scorecard,
    get_api_key,
)

st.set_page_config(page_title="Live Matches | Cricbuzz LiveStats", page_icon="📡", layout="wide")

st.title("📡 Live & Recent Matches")
st.caption("Data powered by Cricbuzz Cricket API (RapidAPI)")

if not get_api_key():
    st.warning(
        "⚠️ **RAPIDAPI_KEY not found.**\n\n"
        "To enable live data:\n"
        "1. Sign up at [RapidAPI – Cricbuzz Cricket](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/)\n"
        "2. Subscribe to a free/basic plan\n"
        "3. Set the key in a `.env` file or Streamlit secrets as `RAPIDAPI_KEY=your_key`\n\n"
        "You can still explore the **SQL Analytics** and **CRUD** pages with the local sample database."
    )
    st.stop()

tab_live, tab_recent, tab_upcoming = st.tabs(["🔴 Live", "✅ Recent", "📅 Upcoming"])


def parse_match_list(data: dict, key_hint: str = "typeMatches"):
    """Robustly extract match list from various possible response shapes."""
    if not data or "error" in data:
        return [], data.get("error") if data else "Empty response"

    matches = []
    # Common structures observed
    if "typeMatches" in data:
        for tm in data["typeMatches"]:
            series_matches = tm.get("seriesMatches", [])
            for sm in series_matches:
                series = sm.get("seriesAdWrapper", {})
                for m in series.get("matches", []):
                    info = m.get("matchInfo", {})
                    matches.append(info)
    elif "matches" in data:
        matches = data["matches"]
    elif isinstance(data, list):
        matches = data

    return matches, None


with tab_live:
    st.subheader("Currently Live Matches")
    if st.button("🔄 Refresh Live Data", key="refresh_live"):
        st.cache_data.clear()

    with st.spinner("Fetching live matches..."):
        raw = get_live_matches()

    matches, err = parse_match_list(raw)
    if err:
        st.error(err)
    elif not matches:
        st.info("No live matches at the moment. Check back during a match day!")
    else:
        for m in matches:
            match_id = m.get("matchId") or m.get("id")
            desc = m.get("matchDesc") or m.get("matchDescription") or "Match"
            team1 = m.get("team1", {}).get("teamName") or m.get("team1Name") or "Team 1"
            team2 = m.get("team2", {}).get("teamName") or m.get("team2Name") or "Team 2"
            status = m.get("status") or m.get("stateTitle") or ""
            series = m.get("seriesName") or ""

            with st.expander(f"🏏 {team1} vs {team2}  —  {desc}  |  {status}", expanded=True):
                st.write(f"**Series:** {series}")
                st.write(f"**Match ID:** `{match_id}`")
                if match_id:
                    if st.button(f"Load Scorecard", key=f"sc_{match_id}"):
                        with st.spinner("Loading scorecard..."):
                            sc = get_scorecard(int(match_id))
                        if sc and "error" not in sc:
                            st.json(sc)
                        else:
                            st.warning(sc.get("error", "Could not load scorecard"))

with tab_recent:
    st.subheader("Recently Completed Matches")
    with st.spinner("Fetching recent matches..."):
        raw = get_recent_matches()
    matches, err = parse_match_list(raw)
    if err:
        st.error(err)
    elif not matches:
        st.info("No recent matches found.")
    else:
        rows = []
        for m in matches[:30]:
            rows.append({
                "Match": m.get("matchDesc") or m.get("matchDescription"),
                "Team 1": m.get("team1", {}).get("teamName") or m.get("team1Name"),
                "Team 2": m.get("team2", {}).get("teamName") or m.get("team2Name"),
                "Status": m.get("status") or m.get("stateTitle"),
                "Series": m.get("seriesName"),
                "Match ID": m.get("matchId") or m.get("id"),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

with tab_upcoming:
    st.subheader("Upcoming Matches")
    with st.spinner("Fetching upcoming fixtures..."):
        raw = get_upcoming_matches()
    matches, err = parse_match_list(raw)
    if err:
        st.error(err)
    elif not matches:
        st.info("No upcoming matches returned.")
    else:
        rows = []
        for m in matches[:40]:
            rows.append({
                "Match": m.get("matchDesc") or m.get("matchDescription"),
                "Team 1": m.get("team1", {}).get("teamName") or m.get("team1Name"),
                "Team 2": m.get("team2", {}).get("teamName") or m.get("team2Name"),
                "Start": m.get("startDate") or m.get("startDateTimestamp"),
                "Series": m.get("seriesName"),
                "Venue": (m.get("venueInfo") or {}).get("ground") if isinstance(m.get("venueInfo"), dict) else None,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
