# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

An interactive multi-page cricket analytics dashboard built with **Python, Streamlit, SQLite and the Cricbuzz Cricket API (RapidAPI)**.

It delivers:
- ⚡ Real-time / recent / upcoming match data
- 📊 Player & team leaderboards
- 🔍 25 SQL practice questions (Beginner → Advanced)
- ✏️ Full CRUD operations on player records
- 🗄️ Clean, well-indexed relational schema ready for analytics

---

## 📁 Project Structure

```
Cricbuzz_LiveStats/
├── Home.py                     # Entry point – project overview & DB status
├── pages/
│   ├── 1_Live_Matches.py       # Live / Recent / Upcoming from Cricbuzz API
│   ├── 2_Top_Stats.py          # Leaderboards (runs, wickets, averages…)
│   ├── 3_SQL_Analytics.py      # 25 practice queries + custom SQL runner
│   └── 4_CRUD_Operations.py    # Create / Read / Update / Delete players
├── utils/
│   ├── db_connection.py        # SQLite helpers (connection, execute, init)
│   ├── api_client.py           # Cricbuzz API wrapper
│   └── populate_db.py          # Schema + rich sample data seeder
├── sql/
│   ├── schema.sql              # Full DDL
│   └── queries.py              # All 25 SQL practice questions
├── data/                       # SQLite DB created here (cricbuzz.db)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone / Unzip & create virtual environment

```bash
cd Cricbuzz_LiveStats
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure Cricbuzz API key for live data

1. Go to [RapidAPI – Cricbuzz Cricket](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/)
2. Subscribe to the free / basic plan
3. Copy your key and create a `.env` file:

```bash
cp .env.example .env
# edit .env and set:
RAPIDAPI_KEY=your_actual_key_here
```

Or use Streamlit secrets (`~/.streamlit/secrets.toml`):

```toml
RAPIDAPI_KEY = "your_actual_key_here"
```

> Without a key you can still use **SQL Analytics**, **Top Stats** and **CRUD** pages with the local sample database.

### 4. Initialise & populate the database

```bash
python -m utils.populate_db
```

This creates `data/cricbuzz.db` with teams, players, venues, series, ~120 matches and thousands of batting/bowling/partnership records – enough to exercise all 25 SQL questions.

### 5. Launch the dashboard

```bash
streamlit run Home.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

---

## 📊 Database Schema (high level)

| Table            | Purpose                                      |
|------------------|----------------------------------------------|
| teams            | International & franchise teams              |
| players          | Player profiles (role, styles, country)      |
| venues           | Stadiums with capacity                       |
| series           | Tournaments / bilateral series               |
| matches          | Match metadata, toss, result, close-match flag |
| batting_stats    | Per-innings batting figures                  |
| bowling_stats    | Per-innings bowling figures                  |
| fielding_stats   | Catches, stumpings, run-outs                 |
| partnerships     | Consecutive batting partnerships             |
| match_players    | Playing XI link                              |

Indexes are created on frequently filtered columns (country, role, date, format, player_id…).

---

## 🧮 SQL Practice Questions

- **Beginner (1-8)** – SELECT, WHERE, GROUP BY, ORDER BY, simple aggregates
- **Intermediate (9-16)** – JOINs, sub-queries, conditional aggregation, window-friendly logic
- **Advanced (17-25)** – CTEs, window functions, ranking systems, form analysis, head-to-head, career trajectory

All questions are available inside the **SQL Analytics** page with one-click execution.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** – multi-page interactive UI
- **SQLite** – zero-config relational store
- **pandas** – tabular display & light transforms
- **requests** – REST API client
- **python-dotenv** – environment variable loading (optional)

---

## 📌 Notes & Tips

- The sample data is randomised but realistic; some advanced filters (exact century partnerships of consecutive players, etc.) may return fewer rows – that is expected.
- For production use you can swap SQLite for PostgreSQL / MySQL by changing the connection string in `utils/db_connection.py`.
- Always keep your RapidAPI key private; never commit `.env` or secrets files.
- Follow PEP 8; all modules contain docstrings and basic error handling.

---

## 📄 License

This project is intended for educational / portfolio purposes. Cricbuzz data remains the property of its owners; use the API according to RapidAPI terms of service.

---

**Happy analysing! 🏏**
