"""
Cricbuzz Cricket API client (via RapidAPI).
Requires RAPIDAPI_KEY environment variable or Streamlit secrets.
"""

import os
import requests
from typing import Optional, Dict, Any, List
import streamlit as st

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
HOST = "cricbuzz-cricket.p.rapidapi.com"


def get_api_key() -> Optional[str]:
    """Retrieve API key from Streamlit secrets or environment."""
    try:
        return st.secrets.get("RAPIDAPI_KEY") or os.getenv("RAPIDAPI_KEY")
    except Exception:
        return os.getenv("RAPIDAPI_KEY")


def _headers() -> Dict[str, str]:
    key = get_api_key()
    if not key:
        return {}
    return {
        "x-rapidapi-key": key,
        "x-rapidapi-host": HOST,
        "Content-Type": "application/json",
    }


def _get(endpoint: str, params: dict = None) -> Optional[Dict[str, Any]]:
    """Generic GET request with error handling."""
    key = get_api_key()
    if not key:
        return {"error": "API key not configured. Set RAPIDAPI_KEY in .env or Streamlit secrets."}

    url = f"{BASE_URL}{endpoint}"
    try:
        resp = requests.get(url, headers=_headers(), params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 204:
            return {"message": "No content / no live matches at the moment"}
        else:
            return {"error": f"API returned status {resp.status_code}", "detail": resp.text[:300]}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}


# -------------------- Public helpers --------------------

def get_live_matches() -> Dict[str, Any]:
    """Fetch currently live matches."""
    return _get("/matches/v1/live")


def get_recent_matches() -> Dict[str, Any]:
    """Fetch recently completed matches."""
    return _get("/matches/v1/recent")


def get_upcoming_matches() -> Dict[str, Any]:
    """Fetch upcoming matches."""
    return _get("/matches/v1/upcoming")


def get_match_info(match_id: int) -> Dict[str, Any]:
    """Basic match info (venue, teams, toss...)."""
    return _get(f"/mcenter/v1/{match_id}")


def get_scorecard(match_id: int) -> Dict[str, Any]:
    """Full scorecard."""
    return _get(f"/mcenter/v1/{match_id}/scard")


def get_miniscore(match_id: int) -> Dict[str, Any]:
    """Compact live score."""
    return _get(f"/mcenter/v1/{match_id}/miniscorecard")


def get_player_search(name: str) -> Dict[str, Any]:
    """Search players by name."""
    return _get("/stats/v1/player/search", params={"plrN": name})


def get_player_career(player_id: int) -> Dict[str, Any]:
    """Player career summary."""
    return _get(f"/stats/v1/player/{player_id}/career")


def get_series_list(series_type: str = "international") -> Dict[str, Any]:
    """Current series (international / league / domestic / women)."""
    return _get(f"/series/v1/{series_type}")


def get_icc_rankings(category: str = "batsmen", format_type: str = "test") -> Dict[str, Any]:
    """
    ICC rankings.
    category: batsmen | bowlers | allrounders | teams
    format_type: test | odi | t20
    """
    # Note: exact endpoint may vary; this is a common pattern
    return _get(f"/stats/v1/rankings/{category}", params={"formatType": format_type})
