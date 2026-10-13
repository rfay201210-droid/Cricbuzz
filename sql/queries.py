"""
25 SQL Practice Questions for Cricbuzz LiveStats.
Each entry: (id, level, title, description, sql)
"""

QUERIES = [
    # ========== BEGINNER (1-8) ==========
    (
        1,
        "Beginner",
        "Indian Players",
        "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        """
SELECT full_name, playing_role, batting_style, bowling_style
FROM players
WHERE country = 'India'
ORDER BY full_name;
""",
    ),
    (
        2,
        "Beginner",
        "Recent Matches (Last 30 Days)",
        "Show all cricket matches that were played in the last 30 days. Include match description, both team names, venue name with city, and match date. Sort by most recent first.",
        """
SELECT m.match_description,
       t1.team_name AS team1,
       t2.team_name AS team2,
       v.venue_name || ', ' || v.city AS venue,
       m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= date('now', '-30 days')
ORDER BY m.match_date DESC;
""",
    ),
    (
        3,
        "Beginner",
        "Top 10 ODI Run Scorers",
        "List the top 10 highest run scorers in ODI cricket. Show player name, total runs, batting average, and centuries. Highest first.",
        """
SELECT p.full_name,
       SUM(b.runs) AS total_runs,
       ROUND(AVG(b.runs), 2) AS batting_average,
       SUM(CASE WHEN b.runs >= 100 THEN 1 ELSE 0 END) AS centuries
FROM batting_stats b
JOIN players p ON b.player_id = p.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE m.match_format = 'ODI'
GROUP BY p.player_id, p.full_name
ORDER BY total_runs DESC
LIMIT 10;
""",
    ),
    (
        4,
        "Beginner",
        "Large Capacity Venues",
        "Display all cricket venues with seating capacity > 50,000. Show venue name, city, country, capacity. Order by largest first.",
        """
SELECT venue_name, city, country, capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
""",
    ),
    (
        5,
        "Beginner",
        "Team Wins Count",
        "Calculate how many matches each team has won. Show team name and total wins. Most wins first.",
        """
SELECT t.team_name, COUNT(*) AS total_wins
FROM matches m
JOIN teams t ON m.winner_id = t.team_id
WHERE m.winner_id IS NOT NULL
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;
""",
    ),
    (
        6,
        "Beginner",
        "Players by Role",
        "Count how many players belong to each playing role. Show role and count.",
        """
SELECT playing_role, COUNT(*) AS player_count
FROM players
WHERE playing_role IS NOT NULL
GROUP BY playing_role
ORDER BY player_count DESC;
""",
    ),
    (
        7,
        "Beginner",
        "Highest Score by Format",
        "Find the highest individual batting score in each format (Test, ODI, T20I). Display format and highest score.",
        """
SELECT m.match_format AS format,
       MAX(b.runs) AS highest_score
FROM batting_stats b
JOIN matches m ON b.match_id = m.match_id
WHERE m.match_format IN ('Test', 'ODI', 'T20I')
GROUP BY m.match_format
ORDER BY highest_score DESC;
""",
    ),
    (
        8,
        "Beginner",
        "Series Starting in 2024",
        "Show all cricket series that started in 2024. Include series name, host country, match type, start date, total matches.",
        """
SELECT series_name, host_country, match_type, start_date, total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY start_date;
""",
    ),
    # ========== INTERMEDIATE (9-16) ==========
    (
        9,
        "Intermediate",
        "All-rounders 1000+ Runs & 50+ Wickets",
        "Find all-rounder players who have scored >1000 runs AND taken >50 wickets. Display name, total runs, total wickets, format.",
        """
SELECT p.full_name,
       SUM(b.runs) AS total_runs,
       SUM(bo.wickets) AS total_wickets,
       m.match_format
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
JOIN bowling_stats bo ON p.player_id = bo.player_id AND b.match_id = bo.match_id
JOIN matches m ON b.match_id = m.match_id
WHERE p.playing_role = 'All-rounder'
GROUP BY p.player_id, p.full_name, m.match_format
HAVING SUM(b.runs) > 1000 AND SUM(bo.wickets) > 50
ORDER BY total_runs DESC;
""",
    ),
    (
        10,
        "Intermediate",
        "Last 20 Completed Matches",
        "Get details of the last 20 completed matches. Show description, teams, winner, margin, victory type, venue. Most recent first.",
        """
SELECT m.match_description,
       t1.team_name AS team1,
       t2.team_name AS team2,
       tw.team_name AS winner,
       m.victory_margin,
       m.victory_type,
       v.venue_name
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams tw ON m.winner_id = tw.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.status = 'Completed'
ORDER BY m.match_date DESC
LIMIT 20;
""",
    ),
    (
        11,
        "Intermediate",
        "Player Performance Across Formats",
        "For players who played at least 2 formats, show total runs in Test, ODI, T20I and overall batting average.",
        """
SELECT p.full_name,
       SUM(CASE WHEN m.match_format = 'Test' THEN b.runs ELSE 0 END) AS test_runs,
       SUM(CASE WHEN m.match_format = 'ODI' THEN b.runs ELSE 0 END) AS odi_runs,
       SUM(CASE WHEN m.match_format = 'T20I' THEN b.runs ELSE 0 END) AS t20i_runs,
       ROUND(AVG(b.runs), 2) AS overall_avg
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
JOIN matches m ON b.match_id = m.match_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT m.match_format) >= 2
ORDER BY overall_avg DESC;
""",
    ),
    (
        12,
        "Intermediate",
        "Home vs Away Wins",
        "Analyze each international team's performance at home vs away. Count wins in both conditions.",
        """
SELECT t.team_name,
       SUM(CASE WHEN v.country = t.country THEN 1 ELSE 0 END) AS home_wins,
       SUM(CASE WHEN v.country != t.country THEN 1 ELSE 0 END) AS away_wins
FROM matches m
JOIN teams t ON m.winner_id = t.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE t.team_type = 'International' AND m.winner_id IS NOT NULL
GROUP BY t.team_id, t.team_name
ORDER BY home_wins + away_wins DESC;
""",
    ),
    (
        13,
        "Intermediate",
        "Century Partnerships",
        "Identify batting partnerships of 100+ runs by consecutive batsmen. Show both players, combined runs, innings.",
        """
SELECT p1.full_name AS batsman1,
       p2.full_name AS batsman2,
       pt.runs AS partnership_runs,
       pt.innings
FROM partnerships pt
JOIN players p1 ON pt.player1_id = p1.player_id
JOIN players p2 ON pt.player2_id = p2.player_id
WHERE pt.runs >= 100
  AND ABS(pt.batting_pos1 - pt.batting_pos2) = 1
ORDER BY pt.runs DESC;
""",
    ),
    (
        14,
        "Intermediate",
        "Bowling at Venues",
        "For bowlers with ≥3 matches at same venue, calculate avg economy, total wickets, matches. Focus on ≥4 overs per match.",
        """
SELECT p.full_name,
       v.venue_name,
       ROUND(AVG(bo.economy), 2) AS avg_economy,
       SUM(bo.wickets) AS total_wickets,
       COUNT(DISTINCT bo.match_id) AS matches_at_venue
FROM bowling_stats bo
JOIN players p ON bo.player_id = p.player_id
JOIN matches m ON bo.match_id = m.match_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE bo.overs >= 4
GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name
HAVING COUNT(DISTINCT bo.match_id) >= 3
ORDER BY avg_economy ASC;
""",
    ),
    (
        15,
        "Intermediate",
        "Performance in Close Matches",
        "Players in close matches (<50 runs or <5 wickets). Avg runs, total close matches, wins when they batted.",
        """
SELECT p.full_name,
       ROUND(AVG(b.runs), 2) AS avg_runs_close,
       COUNT(DISTINCT b.match_id) AS close_matches_played,
       SUM(CASE WHEN m.winner_id = b.team_id THEN 1 ELSE 0 END) AS team_wins_when_batted
FROM batting_stats b
JOIN players p ON b.player_id = p.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE m.is_close_match = 1
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT b.match_id) >= 2
ORDER BY avg_runs_close DESC;
""",
    ),
    (
        16,
        "Intermediate",
        "Yearly Batting Trends (since 2020)",
        "For matches since 2020, show each player's avg runs and strike rate per year (≥5 matches that year).",
        """
SELECT p.full_name,
       strftime('%Y', m.match_date) AS year,
       ROUND(AVG(b.runs), 2) AS avg_runs,
       ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate,
       COUNT(*) AS matches_played
FROM batting_stats b
JOIN players p ON b.player_id = p.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE m.match_date >= '2020-01-01'
GROUP BY p.player_id, p.full_name, strftime('%Y', m.match_date)
HAVING COUNT(*) >= 5
ORDER BY p.full_name, year;
""",
    ),
    # ========== ADVANCED (17-25) ==========
    (
        17,
        "Advanced",
        "Toss Advantage Analysis",
        "Percentage of matches won by the team that won the toss, broken down by bat-first vs bowl-first decision.",
        """
SELECT m.toss_decision,
       COUNT(*) AS total_matches,
       SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) AS toss_winner_also_match_winner,
       ROUND(
           100.0 * SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) / COUNT(*),
           2
       ) AS win_pct_after_winning_toss
FROM matches m
WHERE m.winner_id IS NOT NULL AND m.toss_winner_id IS NOT NULL
GROUP BY m.toss_decision;
""",
    ),
    (
        18,
        "Advanced",
        "Most Economical Limited-Overs Bowlers",
        "Most economical bowlers in ODI & T20. ≥10 matches, avg ≥2 overs per match.",
        """
SELECT p.full_name,
       ROUND(AVG(bo.economy), 2) AS overall_economy,
       SUM(bo.wickets) AS total_wickets,
       COUNT(DISTINCT bo.match_id) AS matches_bowled
FROM bowling_stats bo
JOIN players p ON bo.player_id = p.player_id
JOIN matches m ON bo.match_id = m.match_id
WHERE m.match_format IN ('ODI', 'T20I', 'T20')
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT bo.match_id) >= 10
   AND AVG(bo.overs) >= 2
ORDER BY overall_economy ASC
LIMIT 15;
""",
    ),
    (
        19,
        "Advanced",
        "Most Consistent Batsmen",
        "Avg runs and standard deviation of runs (lower SD = more consistent). ≥10 balls/innings, played since 2022.",
        """
SELECT p.full_name,
       ROUND(AVG(b.runs), 2) AS avg_runs,
       ROUND(
           -- Approximate sample standard deviation
           SQRT(AVG(b.runs * b.runs) - AVG(b.runs) * AVG(b.runs)),
           2
       ) AS std_dev_runs,
       COUNT(*) AS innings
FROM batting_stats b
JOIN players p ON b.player_id = p.player_id
JOIN matches m ON b.match_id = m.match_id
WHERE b.balls_faced >= 10
  AND m.match_date >= '2022-01-01'
GROUP BY p.player_id, p.full_name
HAVING COUNT(*) >= 5
ORDER BY std_dev_runs ASC
LIMIT 20;
""",
    ),
    (
        20,
        "Advanced",
        "Matches & Averages by Format",
        "Count of Test/ODI/T20 matches and batting average in each format. Only players with ≥20 total matches.",
        """
SELECT p.full_name,
       SUM(CASE WHEN m.match_format = 'Test' THEN 1 ELSE 0 END) AS test_matches,
       ROUND(AVG(CASE WHEN m.match_format = 'Test' THEN b.runs END), 2) AS test_avg,
       SUM(CASE WHEN m.match_format = 'ODI' THEN 1 ELSE 0 END) AS odi_matches,
       ROUND(AVG(CASE WHEN m.match_format = 'ODI' THEN b.runs END), 2) AS odi_avg,
       SUM(CASE WHEN m.match_format IN ('T20I', 'T20') THEN 1 ELSE 0 END) AS t20_matches,
       ROUND(AVG(CASE WHEN m.match_format IN ('T20I', 'T20') THEN b.runs END), 2) AS t20_avg
FROM players p
JOIN batting_stats b ON p.player_id = b.player_id
JOIN matches m ON b.match_id = m.match_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT b.match_id) >= 20
ORDER BY (test_matches + odi_matches + t20_matches) DESC;
""",
    ),
    (
        21,
        "Advanced",
        "Comprehensive Performance Ranking",
        "Weighted score combining batting, bowling and fielding. Rank top performers per format.",
        """
WITH player_agg AS (
    SELECT p.player_id, p.full_name, m.match_format,
           SUM(b.runs) AS runs_scored,
           AVG(b.runs) AS batting_average,
           AVG(b.strike_rate) AS strike_rate,
           SUM(bo.wickets) AS wickets_taken,
           AVG(CASE WHEN bo.wickets > 0 THEN bo.runs_conceded * 1.0 / bo.wickets END) AS bowling_average,
           AVG(bo.economy) AS economy_rate,
           SUM(f.catches) AS catches,
           SUM(f.stumpings) AS stumpings
    FROM players p
    LEFT JOIN batting_stats b ON p.player_id = b.player_id
    LEFT JOIN matches m ON b.match_id = m.match_id
    LEFT JOIN bowling_stats bo ON p.player_id = bo.player_id AND bo.match_id = m.match_id
    LEFT JOIN fielding_stats f ON p.player_id = f.player_id AND f.match_id = m.match_id
    WHERE m.match_format IS NOT NULL
    GROUP BY p.player_id, p.full_name, m.match_format
)
SELECT full_name, match_format,
       ROUND(
           (COALESCE(runs_scored,0) * 0.01) + (COALESCE(batting_average,0) * 0.5) + (COALESCE(strike_rate,0) * 0.3)
           + (COALESCE(wickets_taken,0) * 2)
           + ((50 - COALESCE(bowling_average,50)) * 0.5)
           + ((6 - COALESCE(economy_rate,6)) * 2)
           + (COALESCE(catches,0) * 3) + (COALESCE(stumpings,0) * 5)
       , 2) AS performance_score
FROM player_agg
WHERE runs_scored IS NOT NULL OR wickets_taken IS NOT NULL
ORDER BY match_format, performance_score DESC;
""",
    ),
    (
        22,
        "Advanced",
        "Head-to-Head Analysis (last 3 years)",
        "Pairs of teams with ≥5 matches. Total matches, wins each side, win %. ",
        """
SELECT t1.team_name AS team_a,
       t2.team_name AS team_b,
       COUNT(*) AS total_matches,
       SUM(CASE WHEN m.winner_id = m.team1_id THEN 1 ELSE 0 END) AS team_a_wins,
       SUM(CASE WHEN m.winner_id = m.team2_id THEN 1 ELSE 0 END) AS team_b_wins,
       ROUND(100.0 * SUM(CASE WHEN m.winner_id = m.team1_id THEN 1 ELSE 0 END) / COUNT(*), 1) AS team_a_win_pct
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
WHERE m.match_date >= date('now', '-3 years')
  AND m.winner_id IS NOT NULL
GROUP BY m.team1_id, m.team2_id, t1.team_name, t2.team_name
HAVING COUNT(*) >= 5
ORDER BY total_matches DESC;
""",
    ),
    (
        23,
        "Advanced",
        "Recent Player Form Categorization",
        "Last 10 batting performances: compare last-5 vs last-10 avg, SR trend, 50+ scores, consistency. Categorize form.",
        """
WITH ranked AS (
    SELECT b.player_id, p.full_name, b.runs, b.strike_rate, m.match_date,
           ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY m.match_date DESC) AS rn
    FROM batting_stats b
    JOIN players p ON b.player_id = p.player_id
    JOIN matches m ON b.match_id = m.match_id
),
form AS (
    SELECT player_id, full_name,
           AVG(CASE WHEN rn <= 5 THEN runs END) AS avg_last5,
           AVG(CASE WHEN rn <= 10 THEN runs END) AS avg_last10,
           AVG(CASE WHEN rn <= 5 THEN strike_rate END) AS sr_last5,
           SUM(CASE WHEN rn <= 10 AND runs >= 50 THEN 1 ELSE 0 END) AS fifties_last10,
           COUNT(CASE WHEN rn <= 10 THEN 1 END) AS innings_last10
    FROM ranked
    WHERE rn <= 10
    GROUP BY player_id, full_name
    HAVING COUNT(CASE WHEN rn <= 10 THEN 1 END) >= 5
)
SELECT full_name,
       ROUND(avg_last5, 1) AS avg_last_5,
       ROUND(avg_last10, 1) AS avg_last_10,
       ROUND(sr_last5, 1) AS sr_last_5,
       fifties_last10,
       CASE
           WHEN avg_last5 >= 45 AND fifties_last10 >= 3 THEN 'Excellent Form'
           WHEN avg_last5 >= 30 AND fifties_last10 >= 1 THEN 'Good Form'
           WHEN avg_last5 >= 18 THEN 'Average Form'
           ELSE 'Poor Form'
       END AS form_category
FROM form
ORDER BY avg_last5 DESC;
""",
    ),
    (
        24,
        "Advanced",
        "Best Batting Partnerships",
        "Pairs with ≥5 partnerships as consecutive batsmen. Avg runs, 50+ count, highest, success rate.",
        """
SELECT p1.full_name AS partner1,
       p2.full_name AS partner2,
       COUNT(*) AS partnerships,
       ROUND(AVG(pt.runs), 1) AS avg_partnership,
       SUM(CASE WHEN pt.runs >= 50 THEN 1 ELSE 0 END) AS partnerships_50plus,
       MAX(pt.runs) AS highest_partnership,
       ROUND(100.0 * SUM(CASE WHEN pt.runs >= 50 THEN 1 ELSE 0 END) / COUNT(*), 1) AS success_rate_pct
FROM partnerships pt
JOIN players p1 ON pt.player1_id = p1.player_id
JOIN players p2 ON pt.player2_id = p2.player_id
WHERE ABS(pt.batting_pos1 - pt.batting_pos2) = 1
GROUP BY pt.player1_id, pt.player2_id, p1.full_name, p2.full_name
HAVING COUNT(*) >= 5
ORDER BY avg_partnership DESC
LIMIT 20;
""",
    ),
    (
        25,
        "Advanced",
        "Career Trajectory (Quarterly)",
        "Quarterly avg runs & SR, compare to previous quarter, overall trajectory (Ascending/Declining/Stable).",
        """
WITH quarterly AS (
    SELECT p.player_id, p.full_name,
           strftime('%Y', m.match_date) || '-Q' || ((CAST(strftime('%m', m.match_date) AS INTEGER)-1)/3 + 1) AS quarter,
           AVG(b.runs) AS avg_runs,
           AVG(b.strike_rate) AS avg_sr,
           COUNT(*) AS matches
    FROM batting_stats b
    JOIN players p ON b.player_id = p.player_id
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY p.player_id, p.full_name, quarter
    HAVING COUNT(*) >= 3
),
with_lag AS (
    SELECT *,
           LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY quarter) AS prev_avg_runs
    FROM quarterly
)
SELECT full_name, quarter,
       ROUND(avg_runs, 1) AS avg_runs,
       ROUND(avg_sr, 1) AS avg_sr,
       matches,
       CASE
           WHEN prev_avg_runs IS NULL THEN 'First Quarter'
           WHEN avg_runs > prev_avg_runs * 1.1 THEN 'Improving'
           WHEN avg_runs < prev_avg_runs * 0.9 THEN 'Declining'
           ELSE 'Stable'
       END AS quarter_trend,
       CASE
           WHEN AVG(avg_runs) OVER (PARTITION BY player_id) >
                (SELECT AVG(avg_runs) FROM quarterly q2 WHERE q2.player_id = with_lag.player_id
                 AND q2.quarter < (SELECT MIN(quarter) FROM quarterly q3 WHERE q3.player_id = with_lag.player_id) + '2')
           THEN 'Career Ascending'
           ELSE 'Career Stable / Mixed'
       END AS career_phase
FROM with_lag
ORDER BY full_name, quarter;
""",
    ),
]


def get_query_by_id(qid: int):
    for q in QUERIES:
        if q[0] == qid:
            return q
    return None


def get_queries_by_level(level: str = None):
    if level:
        return [q for q in QUERIES if q[1].lower() == level.lower()]
    return QUERIES
