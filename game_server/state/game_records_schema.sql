CREATE TABLE IF NOT EXISTS players (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    createddate INTEGER NOT NULL,
    lastonline INTEGER NOT NULL,
    is_ai BOOLEAN DEFAULT FALSE,
    CONSTRAINT players_name_idx UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    date INTEGER NOT NULL,
    status INTEGER NOT NULL,
    board_size INTEGER DEFAULT 3,
    game_type TEXT DEFAULT 'tick_tack_toe',
    winner_id INTEGER,
    FOREIGN KEY(winner_id) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS moves (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    gameid INTEGER NOT NULL,
    playerid INTEGER NOT NULL,
    idx INTEGER NOT NULL,
    move TEXT NOT NULL,
    date INTEGER NOT NULL,
    q_value REAL DEFAULT NULL,
    FOREIGN KEY(gameid) REFERENCES games(id),
    FOREIGN KEY(playerid) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS game_results (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    gameid INTEGER NOT NULL,
    playerid INTEGER NOT NULL,
    result INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    FOREIGN KEY(gameid) REFERENCES games(id),
    FOREIGN KEY(playerid) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS learning_metrics (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    playerid INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    win_rate REAL DEFAULT 0.0,
    loss_rate REAL DEFAULT 0.0,
    draw_rate REAL DEFAULT 0.0,
    average_q_value REAL DEFAULT NULL,
    games_played INTEGER DEFAULT 0,
    FOREIGN KEY(playerid) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS training_sessions (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    playerid INTEGER NOT NULL,
    start_time INTEGER NOT NULL,
    end_time INTEGER,
    initial_win_rate REAL DEFAULT 0.0,
    final_win_rate REAL DEFAULT 0.0,
    episodes INTEGER DEFAULT 0,
    epsilon_start REAL DEFAULT 1.0,
    epsilon_end REAL DEFAULT NULL,
    FOREIGN KEY(playerid) REFERENCES players(id)
);

CREATE INDEX IF NOT EXISTS idx_games_date ON games(date);
CREATE INDEX IF NOT EXISTS idx_moves_gameid ON moves(gameid);
CREATE INDEX IF NOT EXISTS idx_moves_playerid ON moves(playerid);
CREATE INDEX IF NOT EXISTS idx_learning_metrics_playerid ON learning_metrics(playerid);
CREATE INDEX IF NOT EXISTS idx_learning_metrics_timestamp ON learning_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_training_sessions_playerid ON training_sessions(playerid);
