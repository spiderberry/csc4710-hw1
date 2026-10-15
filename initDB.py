import sqlite3

con = sqlite3.connect("worldcup.db")
cur = con.cursor()

cur.execute("""
        CREATE TABLE IF NOT EXISTS player (
            player_id   INTEGER PRIMARY KEY,          
            first_name    VARCHAR(50) NOT NULL,
            last_name     VARCHAR(50) NOT NULL,
            date_of_birth    DATE NOT NULL,
            position        VARCHAR(10) NOT NULL,
            team_id INTEGER NOT NULL,
            FOREIGN KEY (team_id) REFERENCES team(team_id) ON DELETE CASCADE
        )
    """)

cur.execute("""
        CREATE TABLE IF NOT EXISTS team (
            team_id   INTEGER PRIMARY KEY,          
            nation    VARCHAR(50) NOT NULL UNIQUE
        )
    """)

cur.execute("""
        CREATE TABLE IF NOT EXISTS match (
            match_id   INTEGER PRIMARY KEY,          
            home_team    INTEGER NOT NULL,
            away_team     INTEGER NOT NULL,
            date DATE NOT NULL,
            venue VARCHAR(100) NOT NULL,
            FOREIGN KEY (home_team) REFERENCES team(team_id) ON DELETE CASCADE,
            FOREIGN KEY (away_team) REFERENCES team(team_id) ON DELETE CASCADE,
            CHECK (home_team <> away_team)
        )
    """)

cur.execute("""
        CREATE TABLE IF NOT EXISTS participation (
            participation_id INTEGER PRIMARY KEY,
            match_id   INTEGER NOT NULL,          
            player_id    INTEGER NOT NULL,
            FOREIGN KEY (match_id) REFERENCES match(match_id) ON DELETE CASCADE,
            FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE,
            CONSTRAINT unique_participation UNIQUE (match_id, player_id)
        )
    """)

def table_exists(name):
    result = cur.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (name,)
    ).fetchone()

    return result is not None

print("player:", table_exists("player"))
print("team:", table_exists("team"))
print("match:", table_exists("match"))
print("participation:", table_exists("participation"))
con.close()