-- Cricbuzz LiveStats Database Schema
-- Designed to support all 25 SQL practice questions

PRAGMA foreign_keys = ON;

-- ===================== TEAMS =====================
CREATE TABLE IF NOT EXISTS teams (
    team_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name   TEXT NOT NULL UNIQUE,
    country     TEXT NOT NULL,
    team_type   TEXT DEFAULT 'International'  -- International / Franchise
);

-- ===================== PLAYERS =====================
CREATE TABLE IF NOT EXISTS players (
    player_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name       TEXT NOT NULL,
    playing_role    TEXT,               -- Batsman / Bowler / All-rounder / Wicket-keeper
    batting_style   TEXT,               -- Right-hand bat / Left-hand bat
    bowling_style   TEXT,               -- Right-arm fast / Left-arm orthodox / etc.
    country         TEXT,
    date_of_birth   DATE,
    is_active       INTEGER DEFAULT 1
);

-- ===================== VENUES =====================
CREATE TABLE IF NOT EXISTS venues (
    venue_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name  TEXT NOT NULL,
    city        TEXT,
    country     TEXT,
    capacity    INTEGER
);

-- ===================== SERIES =====================
CREATE TABLE IF NOT EXISTS series (
    series_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name     TEXT NOT NULL,
    host_country    TEXT,
    match_type      TEXT,               -- Test / ODI / T20I / T20
    start_date      DATE,
    end_date        DATE,
    total_matches   INTEGER
);

-- ===================== MATCHES =====================
CREATE TABLE IF NOT EXISTS matches (
    match_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id           INTEGER REFERENCES series(series_id),
    match_description   TEXT,
    team1_id            INTEGER REFERENCES teams(team_id),
    team2_id            INTEGER REFERENCES teams(team_id),
    venue_id            INTEGER REFERENCES venues(venue_id),
    match_date          DATE,
    match_format        TEXT,           -- Test / ODI / T20I / T20
    toss_winner_id      INTEGER REFERENCES teams(team_id),
    toss_decision       TEXT,           -- bat / bowl
    winner_id           INTEGER REFERENCES teams(team_id),
    victory_margin      INTEGER,
    victory_type        TEXT,           -- runs / wickets
    status              TEXT DEFAULT 'Completed',  -- Live / Completed / Upcoming
    is_close_match      INTEGER DEFAULT 0           -- 1 if decided by <50 runs or <5 wickets
);

-- ===================== MATCH PLAYERS (playing XI link) =====================
CREATE TABLE IF NOT EXISTS match_players (
    match_id        INTEGER REFERENCES matches(match_id),
    player_id       INTEGER REFERENCES players(player_id),
    team_id         INTEGER REFERENCES teams(team_id),
    batting_position INTEGER,
    PRIMARY KEY (match_id, player_id)
);

-- ===================== BATTING STATS =====================
CREATE TABLE IF NOT EXISTS batting_stats (
    batting_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id        INTEGER REFERENCES matches(match_id),
    player_id       INTEGER REFERENCES players(player_id),
    team_id         INTEGER REFERENCES teams(team_id),
    innings         INTEGER,
    runs            INTEGER DEFAULT 0,
    balls_faced     INTEGER DEFAULT 0,
    fours           INTEGER DEFAULT 0,
    sixes           INTEGER DEFAULT 0,
    strike_rate     REAL,
    is_out          INTEGER DEFAULT 1,
    dismissal_type  TEXT
);

-- ===================== BOWLING STATS =====================
CREATE TABLE IF NOT EXISTS bowling_stats (
    bowling_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id        INTEGER REFERENCES matches(match_id),
    player_id       INTEGER REFERENCES players(player_id),
    team_id         INTEGER REFERENCES teams(team_id),
    innings         INTEGER,
    overs           REAL DEFAULT 0,
    maidens         INTEGER DEFAULT 0,
    runs_conceded   INTEGER DEFAULT 0,
    wickets         INTEGER DEFAULT 0,
    economy         REAL,
    dots            INTEGER DEFAULT 0
);

-- ===================== FIELDING STATS =====================
CREATE TABLE IF NOT EXISTS fielding_stats (
    fielding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id    INTEGER REFERENCES matches(match_id),
    player_id   INTEGER REFERENCES players(player_id),
    catches     INTEGER DEFAULT 0,
    stumpings   INTEGER DEFAULT 0,
    run_outs    INTEGER DEFAULT 0
);

-- ===================== PARTNERSHIPS =====================
CREATE TABLE IF NOT EXISTS partnerships (
    partnership_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id        INTEGER REFERENCES matches(match_id),
    innings         INTEGER,
    player1_id      INTEGER REFERENCES players(player_id),
    player2_id      INTEGER REFERENCES players(player_id),
    runs            INTEGER,
    batting_pos1    INTEGER,
    batting_pos2    INTEGER
);

-- ===================== INDEXES for performance =====================
CREATE INDEX IF NOT EXISTS idx_players_country ON players(country);
CREATE INDEX IF NOT EXISTS idx_players_role ON players(playing_role);
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_format ON matches(match_format);
CREATE INDEX IF NOT EXISTS idx_batting_player ON batting_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player ON bowling_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_batting_match ON batting_stats(match_id);
CREATE INDEX IF NOT EXISTS idx_venues_capacity ON venues(capacity);
