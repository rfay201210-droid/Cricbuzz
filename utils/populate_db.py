"""
Populate the Cricbuzz LiveStats SQLite database with realistic sample data
sufficient to answer all 25 SQL practice questions.
"""

import random
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.db_connection import get_connection, init_db, DB_PATH

random.seed(42)

# -------------------- Reference Data --------------------
TEAMS = [
    ("India", "India", "International"),
    ("Australia", "Australia", "International"),
    ("England", "England", "International"),
    ("South Africa", "South Africa", "International"),
    ("New Zealand", "New Zealand", "International"),
    ("Pakistan", "Pakistan", "International"),
    ("Sri Lanka", "Sri Lanka", "International"),
    ("West Indies", "West Indies", "International"),
    ("Bangladesh", "Bangladesh", "International"),
    ("Afghanistan", "Afghanistan", "International"),
    ("Mumbai Indians", "India", "Franchise"),
    ("Chennai Super Kings", "India", "Franchise"),
    ("Royal Challengers Bangalore", "India", "Franchise"),
    ("Kolkata Knight Riders", "India", "Franchise"),
]

PLAYERS = [
    # India
    ("Virat Kohli", "Batsman", "Right-hand bat", "Right-arm medium", "India", "1988-11-05"),
    ("Rohit Sharma", "Batsman", "Right-hand bat", "Right-arm offbreak", "India", "1987-04-30"),
    ("Jasprit Bumrah", "Bowler", "Right-hand bat", "Right-arm fast", "India", "1993-12-06"),
    ("Ravindra Jadeja", "All-rounder", "Left-hand bat", "Left-arm orthodox", "India", "1988-12-06"),
    ("KL Rahul", "Wicket-keeper", "Right-hand bat", None, "India", "1992-04-18"),
    ("Hardik Pandya", "All-rounder", "Right-hand bat", "Right-arm medium-fast", "India", "1993-10-11"),
    ("Mohammed Shami", "Bowler", "Right-hand bat", "Right-arm fast", "India", "1990-09-03"),
    ("Rishabh Pant", "Wicket-keeper", "Left-hand bat", None, "India", "1997-10-04"),
    ("Shubman Gill", "Batsman", "Right-hand bat", "Right-arm offbreak", "India", "1999-09-08"),
    ("Yuzvendra Chahal", "Bowler", "Right-hand bat", "Right-arm legbreak", "India", "1990-07-23"),
    # Australia
    ("Steve Smith", "Batsman", "Right-hand bat", "Right-arm legbreak", "Australia", "1989-06-02"),
    ("David Warner", "Batsman", "Left-hand bat", "Right-arm legbreak", "Australia", "1986-10-27"),
    ("Pat Cummins", "Bowler", "Right-hand bat", "Right-arm fast", "Australia", "1993-05-08"),
    ("Mitchell Starc", "Bowler", "Left-hand bat", "Left-arm fast", "Australia", "1990-01-30"),
    ("Glenn Maxwell", "All-rounder", "Right-hand bat", "Right-arm offbreak", "Australia", "1988-10-14"),
    ("Alex Carey", "Wicket-keeper", "Left-hand bat", None, "Australia", "1991-08-27"),
    ("Travis Head", "Batsman", "Left-hand bat", "Right-arm offbreak", "Australia", "1993-12-29"),
    ("Josh Hazlewood", "Bowler", "Left-hand bat", "Right-arm fast-medium", "Australia", "1991-01-08"),
    # England
    ("Joe Root", "Batsman", "Right-hand bat", "Right-arm offbreak", "England", "1990-12-30"),
    ("Ben Stokes", "All-rounder", "Left-hand bat", "Right-arm fast-medium", "England", "1991-06-04"),
    ("Jos Buttler", "Wicket-keeper", "Right-hand bat", None, "England", "1990-09-08"),
    ("Jofra Archer", "Bowler", "Right-hand bat", "Right-arm fast", "England", "1995-04-01"),
    ("Harry Brook", "Batsman", "Right-hand bat", "Right-arm medium", "England", "1999-02-22"),
    ("Mark Wood", "Bowler", "Right-hand bat", "Right-arm fast", "England", "1990-01-11"),
    # South Africa
    ("Quinton de Kock", "Wicket-keeper", "Left-hand bat", None, "South Africa", "1992-12-17"),
    ("Kagiso Rabada", "Bowler", "Left-hand bat", "Right-arm fast", "South Africa", "1995-05-25"),
    ("Aiden Markram", "Batsman", "Right-hand bat", "Right-arm offbreak", "South Africa", "1994-10-04"),
    ("Keshav Maharaj", "Bowler", "Right-hand bat", "Left-arm orthodox", "South Africa", "1990-02-07"),
    # New Zealand
    ("Kane Williamson", "Batsman", "Right-hand bat", "Right-arm offbreak", "New Zealand", "1990-08-08"),
    ("Trent Boult", "Bowler", "Right-hand bat", "Left-arm fast-medium", "New Zealand", "1989-07-22"),
    ("Devon Conway", "Wicket-keeper", "Left-hand bat", None, "New Zealand", "1991-07-08"),
    ("Rachin Ravindra", "All-rounder", "Left-hand bat", "Left-arm orthodox", "New Zealand", "1999-09-18"),
    # Pakistan
    ("Babar Azam", "Batsman", "Right-hand bat", "Right-arm offbreak", "Pakistan", "1994-10-15"),
    ("Shaheen Afridi", "Bowler", "Left-hand bat", "Left-arm fast", "Pakistan", "2000-04-06"),
    ("Mohammad Rizwan", "Wicket-keeper", "Right-hand bat", None, "Pakistan", "1992-06-01"),
    ("Shadab Khan", "All-rounder", "Right-hand bat", "Right-arm legbreak", "Pakistan", "1998-10-04"),
    # Sri Lanka
    ("Angelo Mathews", "All-rounder", "Right-hand bat", "Right-arm medium", "Sri Lanka", "1987-06-02"),
    ("Wanindu Hasaranga", "All-rounder", "Right-hand bat", "Right-arm legbreak", "Sri Lanka", "1997-07-29"),
    # West Indies
    ("Nicholas Pooran", "Wicket-keeper", "Left-hand bat", None, "West Indies", "1995-10-02"),
    ("Jason Holder", "All-rounder", "Right-hand bat", "Right-arm medium-fast", "West Indies", "1991-11-05"),
    # Bangladesh
    ("Shakib Al Hasan", "All-rounder", "Left-hand bat", "Left-arm orthodox", "Bangladesh", "1987-03-24"),
    ("Mustafizur Rahman", "Bowler", "Left-hand bat", "Left-arm fast-medium", "Bangladesh", "1995-09-06"),
    # Afghanistan
    ("Rashid Khan", "Bowler", "Right-hand bat", "Right-arm legbreak", "Afghanistan", "1998-09-20"),
    ("Rahmanullah Gurbaz", "Wicket-keeper", "Right-hand bat", None, "Afghanistan", "2001-11-28"),
]

VENUES = [
    ("Narendra Modi Stadium", "Ahmedabad", "India", 132000),
    ("Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
    ("Eden Gardens", "Kolkata", "India", 68000),
    ("Wankhede Stadium", "Mumbai", "India", 33108),
    ("Lord's", "London", "England", 31100),
    ("The Oval", "London", "England", 25500),
    ("Sydney Cricket Ground", "Sydney", "Australia", 48000),
    ("Newlands", "Cape Town", "South Africa", 25000),
    ("Eden Park", "Auckland", "New Zealand", 50000),
    ("Gaddafi Stadium", "Lahore", "Pakistan", 27000),
    ("R. Premadasa Stadium", "Colombo", "Sri Lanka", 35000),
    ("Kensington Oval", "Bridgetown", "West Indies", 28000),
    ("Shere Bangla National Stadium", "Dhaka", "Bangladesh", 25000),
    ("Sharjah Cricket Stadium", "Sharjah", "UAE", 16000),
    ("Dubai International Cricket Stadium", "Dubai", "UAE", 25000),
    ("Chinnaswamy Stadium", "Bengaluru", "India", 40000),
    ("MA Chidambaram Stadium", "Chennai", "India", 50000),
    ("Optus Stadium", "Perth", "Australia", 60000),
    ("Old Trafford", "Manchester", "England", 26000),
    ("SuperSport Park", "Centurion", "South Africa", 22000),
]

SERIES = [
    ("ICC Cricket World Cup 2023", "India", "ODI", "2023-10-05", "2023-11-19", 48),
    ("Border-Gavaskar Trophy 2023", "India", "Test", "2023-02-09", "2023-03-13", 4),
    ("India tour of Australia 2023", "Australia", "T20I", "2023-11-23", "2023-12-03", 5),
    ("The Ashes 2023", "England", "Test", "2023-06-16", "2023-07-31", 5),
    ("IPL 2024", "India", "T20", "2024-03-22", "2024-05-26", 74),
    ("Pakistan Super League 2024", "Pakistan", "T20", "2024-02-17", "2024-03-18", 34),
    ("South Africa tour of India 2024", "India", "Test", "2024-10-10", "2024-11-05", 3),
    ("T20 World Cup 2024", "USA/WI", "T20I", "2024-06-01", "2024-06-29", 55),
    ("Asia Cup 2023", "Sri Lanka", "ODI", "2023-08-30", "2023-09-17", 13),
    ("New Zealand tour of England 2024", "England", "Test", "2024-05-30", "2024-06-28", 3),
]


def populate():
    init_db(force=True)
    conn = get_connection()
    cur = conn.cursor()

    # Teams
    for name, country, ttype in TEAMS:
        cur.execute(
            "INSERT INTO teams (team_name, country, team_type) VALUES (?, ?, ?)",
            (name, country, ttype),
        )
    team_map = {row[1]: row[0] for row in cur.execute("SELECT team_id, team_name FROM teams")}

    # Players
    for p in PLAYERS:
        cur.execute(
            """INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country, date_of_birth)
               VALUES (?, ?, ?, ?, ?, ?)""",
            p,
        )
    player_map = {row[1]: row[0] for row in cur.execute("SELECT player_id, full_name FROM players")}
    player_ids = list(player_map.values())
    player_country = {row[0]: row[1] for row in cur.execute("SELECT player_id, country FROM players")}

    # Venues
    for v in VENUES:
        cur.execute(
            "INSERT INTO venues (venue_name, city, country, capacity) VALUES (?, ?, ?, ?)",
            v,
        )
    venue_ids = [row[0] for row in cur.execute("SELECT venue_id FROM venues")]

    # Series
    for s in SERIES:
        cur.execute(
            """INSERT INTO series (series_name, host_country, match_type, start_date, end_date, total_matches)
               VALUES (?, ?, ?, ?, ?, ?)""",
            s,
        )
    series_ids = [row[0] for row in cur.execute("SELECT series_id FROM series")]

    # Generate matches (approx 120 matches spanning 2020-2025)
    formats = ["Test", "ODI", "T20I", "T20"]
    match_ids = []
    base_date = datetime(2020, 1, 15)

    for i in range(120):
        fmt = random.choice(formats)
        t1, t2 = random.sample(list(team_map.keys())[:10], 2)  # mainly international
        if random.random() < 0.25:
            t1, t2 = random.sample(list(team_map.keys())[10:], 2)  # franchise sometimes
        team1_id = team_map[t1]
        team2_id = team_map[t2]
        venue_id = random.choice(venue_ids)
        series_id = random.choice(series_ids)
        match_date = (base_date + timedelta(days=random.randint(0, 1800))).strftime("%Y-%m-%d")
        toss_winner = random.choice([team1_id, team2_id])
        toss_dec = random.choice(["bat", "bowl"])
        winner = random.choice([team1_id, team2_id, None])
        margin = random.randint(1, 150) if winner else None
        vtype = random.choice(["runs", "wickets"]) if winner else None
        is_close = 1 if margin and ((vtype == "runs" and margin < 50) or (vtype == "wickets" and margin < 5)) else 0
        status = "Completed" if random.random() > 0.05 else "Live"

        cur.execute(
            """INSERT INTO matches
               (series_id, match_description, team1_id, team2_id, venue_id, match_date,
                match_format, toss_winner_id, toss_decision, winner_id, victory_margin,
                victory_type, status, is_close_match)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                series_id,
                f"{t1} vs {t2} - {fmt}",
                team1_id,
                team2_id,
                venue_id,
                match_date,
                fmt,
                toss_winner,
                toss_dec,
                winner,
                margin,
                vtype,
                status,
                is_close,
            ),
        )
        match_ids.append(cur.lastrowid)

    # Batting, bowling, fielding, partnerships for each match
    for mid in match_ids:
        # Pick 11 players roughly matching countries of the two teams (simplified)
        selected = random.sample(player_ids, min(22, len(player_ids)))
        team1_players = selected[:11]
        team2_players = selected[11:22] if len(selected) > 11 else selected[:11]

        # Insert match_players
        for pos, pid in enumerate(team1_players, 1):
            cur.execute(
                "INSERT OR IGNORE INTO match_players (match_id, player_id, team_id, batting_position) VALUES (?, ?, ?, ?)",
                (mid, pid, team_map[list(team_map.keys())[0]], pos),  # simplified team link
            )
        for pos, pid in enumerate(team2_players, 1):
            cur.execute(
                "INSERT OR IGNORE INTO match_players (match_id, player_id, team_id, batting_position) VALUES (?, ?, ?, ?)",
                (mid, pid, team_map[list(team_map.keys())[1]], pos),
            )

        # Batting stats (two innings sometimes)
        for innings in [1, 2]:
            for pos, pid in enumerate(random.sample(selected, min(11, len(selected))), 1):
                runs = max(0, int(random.gauss(28, 25)))
                balls = max(runs, int(runs * random.uniform(0.7, 1.6)) + random.randint(0, 15))
                fours = random.randint(0, min(12, runs // 4))
                sixes = random.randint(0, min(6, runs // 6))
                sr = round((runs / balls) * 100, 2) if balls else 0
                cur.execute(
                    """INSERT INTO batting_stats
                       (match_id, player_id, team_id, innings, runs, balls_faced, fours, sixes, strike_rate, is_out)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (mid, pid, random.choice([team1_id, team2_id]) if False else 1, innings, runs, balls, fours, sixes, sr, 1),
                )

        # Bowling stats
        for innings in [1, 2]:
            for pid in random.sample(selected, min(6, len(selected))):
                overs = round(random.uniform(2.0, 10.0), 1)
                runs_c = int(overs * random.uniform(4.5, 9.5))
                wkts = random.randint(0, 5)
                economy = round(runs_c / overs, 2) if overs else 0
                cur.execute(
                    """INSERT INTO bowling_stats
                       (match_id, player_id, team_id, innings, overs, maidens, runs_conceded, wickets, economy)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (mid, pid, 1, innings, overs, random.randint(0, 2), runs_c, wkts, economy),
                )

        # Fielding
        for pid in random.sample(selected, min(8, len(selected))):
            cur.execute(
                """INSERT INTO fielding_stats (match_id, player_id, catches, stumpings, run_outs)
                   VALUES (?, ?, ?, ?, ?)""",
                (mid, pid, random.randint(0, 3), random.randint(0, 1), random.randint(0, 1)),
            )

        # Partnerships (consecutive positions)
        for innings in [1, 2]:
            for pos in range(1, 8):
                p1 = random.choice(selected)
                p2 = random.choice([p for p in selected if p != p1])
                runs = random.randint(5, 180)
                cur.execute(
                    """INSERT INTO partnerships
                       (match_id, innings, player1_id, player2_id, runs, batting_pos1, batting_pos2)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (mid, innings, p1, p2, runs, pos, pos + 1),
                )

    # Fix some team_id references properly for a few records (simplified for demo)
    # Update a subset of batting/bowling team_ids to real values
    cur.execute("UPDATE batting_stats SET team_id = (SELECT team_id FROM teams ORDER BY RANDOM() LIMIT 1)")
    cur.execute("UPDATE bowling_stats SET team_id = (SELECT team_id FROM teams ORDER BY RANDOM() LIMIT 1)")

    conn.commit()
    conn.close()
    print(f"✅ Database populated successfully at {DB_PATH}")
    print(f"   Teams: {len(TEAMS)}, Players: {len(PLAYERS)}, Venues: {len(VENUES)}, Series: {len(SERIES)}, Matches: {len(match_ids)}")


if __name__ == "__main__":
    populate()
