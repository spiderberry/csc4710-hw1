import sqlite3

class Database:
    # Database setup

    def __init__(self):
        self.init_db()

    def get_connection(self):
        con = sqlite3.connect("worldcup.db")
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def init_db(self):
        try:
            with self.get_connection() as con:

                print("Database connection established for initialization.")

                con.execute("""
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

                con.execute("""
                    CREATE TABLE IF NOT EXISTS team (
                        team_id   INTEGER PRIMARY KEY,          
                        nation    VARCHAR(50) NOT NULL UNIQUE
                    )
                """)

                con.execute("""
                    CREATE TABLE IF NOT EXISTS match (
                        match_id   INTEGER PRIMARY KEY,          
                        home_team    INTEGER NOT NULL,
                        away_team     INTEGER NOT NULL,
                        date DATE NOT NULL,
                        venue VARCHAR(100) NOT NULL,
                        FOREIGN KEY (home_team) REFERENCES team(team_id) ON DELETE CASCADE,
                        FOREIGN KEY (away_team) REFERENCES team(team_id) ON DELETE CASCADE,
                        CONSTRAINT unique_match UNIQUE (home_team, away_team, date),
                        CHECK (home_team <> away_team)
                    )
                """)

                con.execute("""
                    CREATE TABLE IF NOT EXISTS participation (
                        participation_id INTEGER PRIMARY KEY,
                        match_id   INTEGER NOT NULL,          
                        player_id    INTEGER NOT NULL,
                        FOREIGN KEY (match_id) REFERENCES match(match_id) ON DELETE CASCADE,
                        FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE,
                        CONSTRAINT unique_participation UNIQUE (match_id, player_id)
                    )
                """)

            print("Database initialized successfully.")

        except sqlite3.Error as e:
            print(f"Error occurred while initializing the database: {e}")
            raise

        finally:
            if con is not None:
                con.close()
                print("Database connection closed.")

    def add_player(self, first_name, last_name, date_of_birth, position, team_name):
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                team_id = self.get_team_id(con, team_name)

                cur.execute("""
                    INSERT INTO player (
                        first_name,
                        last_name,
                        date_of_birth,
                        position,
                        team_id
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (first_name, last_name, date_of_birth, position, team_id))
            print("Player added successfully.")

        except sqlite3.Error as e:
            print(f"Error occurred while adding player: {e}")
            raise

    def get_players(self):
        try:
            with self.get_connection() as con:
                players = con.execute("""
                    SELECT p.player_id, p.first_name, p.last_name,
                           p.date_of_birth, p.position, t.nation
                    FROM player p
                    JOIN team t ON p.team_id = t.team_id
                """).fetchall()
                return players

        except sqlite3.Error as e:
            print(f"Error occurred while retrieving players: {e}")
            raise

    def update_player(self, player_id, first_name, last_name, date_of_birth, position, team_name):
        with self.get_connection() as con:
            team_id = self.get_team_id(con, team_name)
            invalid = con.execute("""
                SELECT 1 FROM participation p
                JOIN match m ON p.match_id = m.match_id
                WHERE p.player_id = ? AND ? NOT IN (m.home_team, m.away_team)
            """, (player_id, team_id)).fetchone()

            if invalid:
                raise ValueError("Remove this player's appearances in incompatible matches before changing teams.")
            
            cur = con.execute("""
                UPDATE player
                SET first_name = ?, last_name = ?, date_of_birth = ?, position = ?, team_id = ?
                WHERE player_id = ?
            """, (first_name, last_name, date_of_birth, position, team_id, player_id))

            if cur.rowcount == 0:
                raise ValueError("Player no longer exists.")

    def delete_player(self, player_id):
        with self.get_connection() as con:
            con.execute("DELETE FROM player WHERE player_id = ?", (player_id,))

    def add_team(self, nation):
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO team (nation)
                    VALUES (?)
                """, (nation,))
            print("Team added successfully.")

        except sqlite3.Error as e:
            print(f"Error occurred while adding team: {e}")
            raise

    def get_teams(self):
        try:
            with self.get_connection() as con:
                teams = con.execute("SELECT * FROM team").fetchall()
                return teams

        except sqlite3.Error as e:
            print(f"Error occurred while retrieving teams: {e}")
            raise

    def update_team(self, team_id, nation):
        with self.get_connection() as con:
            cur = con.execute("UPDATE team SET nation = ? WHERE team_id = ?", (nation, team_id))

            if cur.rowcount == 0:
                raise ValueError("Team no longer exists.")

    def delete_team(self, team_id):
        with self.get_connection() as con:
            con.execute("DELETE FROM team WHERE team_id = ?", (team_id,))

    def get_team_id(self, con, team_name):
        team = con.execute("SELECT team_id FROM team WHERE nation = ?", (team_name,)).fetchone()
        if team is None:
            raise ValueError(f"Team not found: {team_name}")
        return team[0]

    def add_match(self, home_team, away_team, date, venue):
        try:
            with self.get_connection() as con:
                cur = con.cursor()

                home_team_id = self.get_team_id(con, home_team)
                away_team_id = self.get_team_id(con, away_team)

                cur.execute("""
                    INSERT INTO match (home_team, away_team, date, venue)
                    VALUES (?, ?, ?, ?)
                """, (home_team_id, away_team_id, date, venue))
            print("Match added successfully.")

        except sqlite3.Error as e:
            print(f"Error occurred while adding match: {e}")
            raise

    def get_matches(self):
        try:
            with self.get_connection() as con:
                matches = con.execute("""
                    SELECT
                        match_id,
                        t.nation AS home_team,
                        t2.nation AS away_team,
                        date,
                        venue
                    FROM match m
                    JOIN team t ON m.home_team = t.team_id
                    JOIN team t2 ON m.away_team = t2.team_id
                """).fetchall()
                return matches

        except sqlite3.Error as e:
            print(f"Error occurred while retrieving matches: {e}")
            raise

    def update_match(self, match_id, home_team, away_team, date, venue):
        with self.get_connection() as con:
            home_team_id = self.get_team_id(con, home_team)
            away_team_id = self.get_team_id(con, away_team)
            
            if home_team_id == away_team_id:
                raise ValueError("Home and away teams must be different.")
            
            invalid = con.execute("""
                SELECT 1 FROM participation p
                JOIN player pl ON p.player_id = pl.player_id
                WHERE p.match_id = ? AND pl.team_id NOT IN (?, ?)
            """, (match_id, home_team_id, away_team_id)).fetchone()

            if invalid:
                raise ValueError("Remove appearances from incompatible teams before changing this match's teams.")
            
            cur = con.execute("""
                UPDATE match SET home_team = ?, away_team = ?, date = ?, venue = ?
                WHERE match_id = ?
            """, (home_team_id, away_team_id, date, venue, match_id))

            if cur.rowcount == 0:
                raise ValueError("Match no longer exists.")

    def delete_match(self, match_id):
        with self.get_connection() as con:
            con.execute("DELETE FROM match WHERE match_id = ?", (match_id,))

    def add_participation(self, match_id, player_id):
        try:
            with self.get_connection() as con:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO participation (match_id, player_id)
                    SELECT m.match_id, pl.player_id
                    FROM match m JOIN player pl
                        ON pl.team_id IN (m.home_team, m.away_team)
                    WHERE m.match_id = ? AND pl.player_id = ?
                      AND NOT EXISTS (
                          SELECT 1 FROM participation p
                          WHERE p.match_id = m.match_id AND p.player_id = pl.player_id
                      )
                """, (match_id, player_id))
                if cur.rowcount == 0:
                    raise ValueError("Player is not eligible or is already added to this match.")
            print("Participation added successfully.")

        except sqlite3.Error as e:
            print(f"Error occurred while adding participation: {e}")
            raise

    def get_detailed_participations(self, match_id):
        try:
            with self.get_connection() as con:
                detailed_participations = con.execute("""
                    SELECT
                        pl.player_id,
                        pl.first_name,
                        pl.last_name,
                        t.nation AS team_name
                    FROM participation p
                    JOIN player pl ON p.player_id = pl.player_id
                    JOIN team t ON pl.team_id = t.team_id
                    WHERE p.match_id = ?
                    ORDER BY pl.last_name, pl.first_name, pl.player_id
                """, (match_id,)).fetchall()
                return detailed_participations

        except sqlite3.Error as e:
            print(f"Error occurred while retrieving detailed participations: {e}")
            raise

    def get_eligible_players(self, match_id):
        with self.get_connection() as con:
            players = con.execute("""
                SELECT pl.player_id, pl.first_name, pl.last_name, t.nation
                FROM player pl
                JOIN team t ON pl.team_id = t.team_id
                JOIN match m ON pl.team_id IN (m.home_team, m.away_team)
                WHERE m.match_id = ?
                  AND NOT EXISTS (
                      SELECT 1 FROM participation p
                      WHERE p.match_id = m.match_id AND p.player_id = pl.player_id
                  )
                ORDER BY pl.last_name, pl.first_name, pl.player_id
            """, (match_id,)).fetchall()
            return players

    def remove_participation(self, match_id, player_id):
        with self.get_connection() as con:
            con.execute("DELETE FROM participation WHERE match_id = ? AND player_id = ?", (match_id, player_id))
