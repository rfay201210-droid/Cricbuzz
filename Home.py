"""
Cricbuzz LiveStats - Home Page
Run with: streamlit run Home.py
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))
from utils.db_connection import init_db, DB_PATH, execute_query

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a237e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #455a64;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #1565c0;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #c62828;
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏏 Cricbuzz LiveStats</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Real-Time Cricket Insights & SQL-Based Analytics</p>',
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>⚡ Live Matches</h4>
        <p>Real-time scorecards, batsmen & bowler info, match status and venue details pulled from the Cricbuzz API.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>📊 Top Player Stats</h4>
        <p>Most runs, highest scores, leading wicket-takers and more – visualised cleanly for quick insights.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>🔍 SQL Analytics</h4>
        <p>25 carefully crafted SQL practice questions (Beginner → Advanced) with live results from the local database.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.subheader("🛠️ Project Overview")
st.write("""
**Cricbuzz LiveStats** is an end-to-end cricket analytics platform that combines:

- **REST API Integration** – Live and recent match data from the official Cricbuzz Cricket API (via RapidAPI)
- **SQL Database** – SQLite backend with a rich schema supporting complex analytical queries
- **Interactive Dashboard** – Multi-page Streamlit application
- **Full CRUD** – Create, Read, Update, Delete operations on players and matches
""")

st.subheader("📁 Navigation")
st.info("""
Use the **sidebar** to navigate between pages:

1. **🏠 Home** – This page  
2. **📡 Live Matches** – Real-time scores from Cricbuzz API  
3. **🏆 Top Stats** – Leaderboards for batting & bowling  
4. **📊 SQL Analytics** – 25 practice queries + custom SQL  
5. **✏️ CRUD Operations** – Manage players & matches  
""")

st.subheader("⚙️ Quick Setup")
with st.expander("How to run this project"):
    st.code("""
# 1. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\\Scripts\\activate         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key (optional for live data)
# Create a .env file or set Streamlit secrets:
# RAPIDAPI_KEY=your_rapidapi_key_here

# 4. Populate the database (first time only)
python -m utils.populate_db

# 5. Launch the dashboard
streamlit run Home.py
    """, language="bash")

st.subheader("🗄️ Database Status")
try:
    if not DB_PATH.exists():
        st.warning("Database not found. Click below to initialise & populate sample data.")
        if st.button("🚀 Initialise & Populate Database"):
            with st.spinner("Creating schema and inserting sample data..."):
                from utils.populate_db import populate
                populate()
            st.success("Database ready!")
            st.rerun()
    else:
        counts = {
            "Teams": execute_query("SELECT COUNT(*) AS c FROM teams")[0]["c"],
            "Players": execute_query("SELECT COUNT(*) AS c FROM players")[0]["c"],
            "Venues": execute_query("SELECT COUNT(*) AS c FROM venues")[0]["c"],
            "Series": execute_query("SELECT COUNT(*) AS c FROM series")[0]["c"],
            "Matches": execute_query("SELECT COUNT(*) AS c FROM matches")[0]["c"],
            "Batting records": execute_query("SELECT COUNT(*) AS c FROM batting_stats")[0]["c"],
            "Bowling records": execute_query("SELECT COUNT(*) AS c FROM bowling_stats")[0]["c"],
        }
        st.success(f"Database loaded from `{DB_PATH.name}`")
        st.json(counts)
except Exception as e:
    st.error(f"Database check failed: {e}")

st.markdown("---")
st.caption("Built with ❤️ using Python • Streamlit • SQLite • Cricbuzz API | Skills: Python, SQL, REST API, Data Analytics")
