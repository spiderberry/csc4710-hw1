from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from collections import Counter
import sqlite3

class WorldCupDBManager:

    def __init__(self, root, db):

        self.db = db
        self.editing_ids = {"player": None, "team": None, "match": None}

        root.title("World Cup 2026 — Database Manager")

        mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Label(mainframe, text="World Cup 2026 Database Manager", font=("Helvetica", 16)).grid(column=1, row=0, columnspan=3, sticky=W)
        
        navigation_frame = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
        navigation_frame.grid(column=1, row=1, columnspan=2, sticky=(W))
        ttk.Button(navigation_frame, text="Players", command=self.players).grid(column=1, row=0, sticky=W)
        ttk.Button(navigation_frame, text="Teams", command=self.teams).grid(column=2, row=0, sticky=W)
        ttk.Button(navigation_frame, text="Matches", command=self.matches).grid(column=3, row=0, sticky=W)

        self.players_screen = self.build_players_screen(mainframe)
        self.teams_screen = self.build_teams_screen(mainframe)
        self.matches_screen = self.build_matches_screen(mainframe)

        for screen in (self.players_screen, self.teams_screen, self.matches_screen):
            screen.grid(column=1, row=2, columnspan=2, sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)
        
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        self.teams_screen.grid_remove()
        self.matches_screen.grid_remove()
        self.current_view = self.players_screen

    def show_view(self, frame):
        if self.current_view is not None:
            self.current_view.grid_remove()

        self.current_view = frame
        self.current_view.grid()

    def clear_list(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

    def configure_columns(self, treeview):
        for col in treeview["columns"]:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, minwidth=60)

    def edit_record(self, kind, tree, variables):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Cannot edit", f"Select a {kind} first.")
            return
        
        values = tree.item(selected[0], "values")
        self.editing_ids[kind] = int(values[0])

        for variable, value in zip(variables, values[1:]):
            variable.set(value)

    def delete_record(self, kind, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Cannot delete", f"Select a {kind} first.")
            return
        
        record_id = int(tree.item(selected[0], "values")[0])
        consequences = {
            "player": "Their appearances will also be deleted.",
            "team": "Its players, matches, and related appearances will also be deleted.",
            "match": "Its player appearances will also be deleted.",
        }
        if not messagebox.askyesno("Confirm deletion", f"Delete {kind} #{record_id}?\n{consequences[kind]}"):
            return
        
        try:
            getattr(self.db, f"delete_{kind}")(record_id)

        except sqlite3.Error as e:
            messagebox.showerror("Cannot delete", str(e))
            return

        self.editing_ids = {"player": None, "team": None, "match": None}
        self.refresh_records()

    def refresh_records(self):
        self.clear_list(self.players_list)
        self.load_players(self.players_list)
        self.clear_list(self.teams_list)
        self.load_teams(self.teams_list)
        self.refresh_player_teams()
        self.refresh_match_teams()
        self.reload_matches()

    def save(self):
        if self.current_view == self.players_screen:
            kind = "player"
            values = (
                self.player_firstname.get(), self.player_lastname.get(), self.player_dob.get(),
                self.player_position.get(), self.player_team_name.get(),
            )
        elif self.current_view == self.teams_screen:
            kind = "team"
            values = (self.team_nation.get(),)
        else:
            kind = "match"
            values = (
                self.home_team_position.get(), self.away_team_position.get(),
                self.match_date.get(), self.match_venue.get(),
            )
        record_id = self.editing_ids[kind]
        try:
            if record_id is None:
                getattr(self.db, f"add_{kind}")(*values)
            else:
                getattr(self.db, f"update_{kind}")(record_id, *values)
        except (ValueError, sqlite3.Error) as e:
            messagebox.showerror("Cannot save", str(e))
            return
        self.refresh_records()

    # players 

    def build_players_screen(self, parent):
        screen = ttk.Frame(parent)
        self.build_player_list(screen)
        self.build_player_details(screen)

        return screen

    def build_player_list(self, screen):
        playersframe = ttk.Frame(screen, padding=(3, 3, 12, 12))
        playersframe.grid(column=0, row=0, sticky=(N, W, E, S))
        ttk.Label(playersframe, text="Players").grid(column=1, row=1, sticky=W)
        cols = ("ID", "First Name", "Last Name", "Date of Birth", "Position", "Team")
        self.players_list = ttk.Treeview(playersframe, columns=cols, show="headings")
        self.load_players(self.players_list)
        self.players_list.grid(column=1, row=2, sticky=(N, W, E, S))
        
        playercrud_frame = ttk.Frame(playersframe, padding=(3, 3, 12, 12))
        playercrud_frame.grid(column=1, row=3, sticky=(W))
        ttk.Button(playercrud_frame, text="New Player", command=self.new_player).grid(column=1, row=0, sticky=W)
        ttk.Button(playercrud_frame, text="Edit Selected", command=self.edit_player).grid(column=2, row=0, sticky=W)
        ttk.Button(playercrud_frame, text="Delete Selected", command=self.delete_player).grid(column=3, row=0, sticky=W)

    def build_player_details(self, screen):
        detailsframe = ttk.Frame(screen, padding=(3, 3, 12, 12))
        detailsframe.grid(column=1, row=0, sticky=(N, W, E, S))
        ttk.Label(detailsframe, text="Player Details", font=("Helvetica", 14)).grid(column=1, row=0, columnspan=3, sticky=W)
        
        self.player_firstname = StringVar()
        ttk.Label(detailsframe, text="First Name").grid(column=1, row=1, sticky=W)
        ttk.Entry(detailsframe, width=20, textvariable=self.player_firstname).grid(column=1, row=2, sticky=(W, E))
        
        self.player_lastname = StringVar()
        ttk.Label(detailsframe, text="Last Name").grid(column=1, row=3, sticky=W)
        ttk.Entry(detailsframe, width=20, textvariable=self.player_lastname).grid(column=1, row=4, sticky=(W, E))
        
        self.player_dob = StringVar()
        ttk.Label(detailsframe, text="Date of Birth (MM/DD/YYYY)").grid(column=1, row=5, sticky=W)
        ttk.Entry(detailsframe, width=20, textvariable=self.player_dob).grid(column=1, row=6, sticky=(W, E))
        
        self.player_position = StringVar()
        positions = ("Forward", "Midfielder", "Defender", "Goalkeeper")
        ttk.Label(detailsframe, text="Position").grid(column=1, row=7, sticky=W)
        position_menu = ttk.OptionMenu(detailsframe, self.player_position, positions[0], *positions)
        position_menu.grid(column=1, row=8, sticky=(W, E))

        self.player_team_name = StringVar()
        ttk.Label(detailsframe, text="Team").grid(column=1, row=9, sticky=W)
        self.player_team_menu = ttk.OptionMenu(detailsframe, self.player_team_name, "Select team")
        self.refresh_player_teams()
        self.player_team_menu.grid(column=1, row=10, sticky=(W, E))

        ttk.Button(detailsframe, text="Save", command=self.save).grid(column=1, row=11, sticky=W)

    def players(self):
        self.show_view(self.players_screen)
        self.refresh_player_teams()
        self.clear_list(self.players_list)
        self.load_players(self.players_list)

    def new_player(self):
        try:
            self.db.add_player(self.player_firstname.get(), self.player_lastname.get(), self.player_dob.get(), self.player_position.get(), self.player_team_name.get())

        except ValueError as e:
            messagebox.showerror("Cannot add player", str(e))
            return
        
        self.clear_list(self.players_list)
        self.load_players(self.players_list)
        self.editing_ids["player"] = None

    def load_players(self, players_list):
        players = self.db.get_players()

        for id, first_name, last_name, date_of_birth, position, team_name in players:
            players_list.insert("", "end", values=(id, first_name, last_name, date_of_birth, position, team_name))

        self.configure_columns(players_list)

    def edit_player(self):
        self.edit_record("player", self.players_list, (
            self.player_firstname, self.player_lastname, self.player_dob,
            self.player_position, self.player_team_name,
        ))

    def delete_player(self):
        self.delete_record("player", self.players_list)

    def refresh_player_teams(self):
        team_names = [nation for team_id, nation in self.db.get_teams()]
        selected_team = self.player_team_name.get()
        self.player_team_menu.set_menu("Select team", *team_names)

        if selected_team in team_names:
            self.player_team_name.set(selected_team)

    # teams

    def build_teams_screen(self, parent):
        screen = ttk.Frame(parent)
        self.build_teams_list(screen)
        self.build_team_details(screen)
        return screen

    def build_teams_list(self, screen):
        teamsframe = ttk.Frame(screen, padding=(3, 3, 12, 12))
        teamsframe.grid(column=0, row=0, sticky=(N, W, E, S))
        ttk.Label(teamsframe, text="Teams").grid(column=1, row=1, sticky=W)
        cols = ("ID", "Nation")
        self.teams_list = ttk.Treeview(teamsframe, columns=cols, show="headings")
        self.load_teams(self.teams_list)
        self.teams_list.grid(column=1, row=2, sticky=(N, W, E, S))
        
        teamcrud_frame = ttk.Frame(teamsframe, padding=(3, 3, 12, 12))
        teamcrud_frame.grid(column=1, row=3, sticky=(W))
        ttk.Button(teamcrud_frame, text="New Team", command=self.new_team).grid(column=1, row=0, sticky=W)
        ttk.Button(teamcrud_frame, text="Edit Selected", command=self.edit_team).grid(column=2, row=0, sticky=W)
        ttk.Button(teamcrud_frame, text="Delete Selected", command=self.delete_team).grid(column=3, row=0, sticky=W)

    def build_team_details(self, screen):
        detailsframe = ttk.Frame(screen, padding=(3, 3, 12, 12))
        detailsframe.grid(column=1, row=0, sticky=(N, W, E, S))
        ttk.Label(detailsframe, text="Team Details", font=("Helvetica", 14)).grid(column=1, row=0, columnspan=3, sticky=W)
        
        self.team_nation = StringVar()
        ttk.Label(detailsframe, text="Nation:").grid(column=1, row=1, sticky=W)
        ttk.Entry(detailsframe, width=20, textvariable=self.team_nation).grid(column=1, row=2, sticky=(W, E))

        ttk.Button(detailsframe, text="Save", command=self.save).grid(column=1, row=3, sticky=W)

    def teams(self):
        self.show_view(self.teams_screen)
        self.clear_list(self.teams_list)
        self.load_teams(self.teams_list)

    def new_team(self):
        self.db.add_team(self.team_nation.get())
        self.editing_ids["team"] = None
        self.clear_list(self.teams_list)
        self.load_teams(self.teams_list)
        self.refresh_player_teams()
        self.refresh_match_teams()

    def load_teams(self, teams_list):
        teams = self.db.get_teams()

        for id, nation in teams:
            teams_list.insert("", "end", values=(id, nation))

        self.configure_columns(teams_list)

    def edit_team(self):
        self.edit_record("team", self.teams_list, (self.team_nation,))

    def delete_team(self):
        self.delete_record("team", self.teams_list)

    # Matches view

    def build_matches_screen(self, parent):
        screen = ttk.Frame(parent)
        self.build_match_list(screen)
        self.build_match_appearances(screen)
        self.build_match_details(screen)
        return screen

    def build_match_search(self, screen):
        search_frame = ttk.Frame(screen, padding=(3, 3, 12, 12))
        search_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        self.match_search = StringVar()
        match_search_options = ("Search by team", "Search by date", "Search by player")
        match_search_menu = ttk.OptionMenu(search_frame, self.match_search, match_search_options[0], *match_search_options)
        match_search_menu.grid(column=1, row=0, sticky=W)

        self.match_search_entry = StringVar()
        ttk.Entry(search_frame, width=20, textvariable=self.match_search_entry).grid(column=2, row=0, sticky=(W, E))

        ttk.Button(search_frame, text="Search", command=self.search_matches).grid(column=3, row=0, sticky=W)
        ttk.Button(search_frame, text="Show all", command=self.reload_matches).grid(column=4, row=0, sticky=W)

    def build_match_list(self, screen):
        self.build_match_search(screen)
        matches_frame = ttk.Frame(screen, padding=(3, 3, 12, 12))
        matches_frame.grid(column=0, row=1, sticky=(N, W, E, S))
        ttk.Label(matches_frame, text="Matches").grid(column=1, row=1, sticky=W)
        cols = ("ID", "Home", "Away", "Date", "Venue")
        self.matches_list = ttk.Treeview(matches_frame, columns=cols, show="headings")
        self.matches_list.bind("<<TreeviewSelect>>", self.refresh_match_appearances)
        self.load_matches(self.matches_list)
        self.matches_list.grid(column=1, row=2, sticky=(N, W, E, S))

        matches_crud_frame = ttk.Frame(matches_frame, padding=(3, 3, 12, 12))
        matches_crud_frame.grid(column=1, row=3, sticky=(W))
        ttk.Button(matches_crud_frame, text="New Match", command=self.new_match).grid(column=1, row=3, sticky=W)
        ttk.Button(matches_crud_frame, text="Edit Selected", command=self.edit_match).grid(column=2, row=3, sticky=W)
        ttk.Button(matches_crud_frame, text="Delete Selected", command=self.delete_match).grid(column=3, row=3)

    def build_match_details(self, screen):
        details_frame = ttk.Frame(screen, padding=(3, 3, 12, 12))
        details_frame.grid(column=1, row=1, sticky=(N, W, E, S))
        ttk.Label(details_frame, text="Match Details", font=("Helvetica", 14)).grid(column=1, row=0, columnspan=3, sticky=W)

        ttk.Label(details_frame, text="Home").grid(column=1, row=1, sticky=W)
        self.home_team_position = StringVar()
        self.home_team_menu = ttk.OptionMenu(details_frame, self.home_team_position, "Select home team")
        self.home_team_menu.grid(column=1, row=2, sticky=(W, E))

        ttk.Label(details_frame, text="Away").grid(column=1, row=3, sticky=W)
        self.away_team_position = StringVar()
        self.away_team_menu = ttk.OptionMenu(details_frame, self.away_team_position, "Select away team")
        self.away_team_menu.grid(column=1, row=4, sticky=(W, E))
        self.refresh_match_teams()

        self.match_date = StringVar()
        ttk.Label(details_frame, text="Date (MM/DD/YYYY)").grid(column=1, row=5, sticky=W)
        ttk.Entry(details_frame, width=20, textvariable=self.match_date).grid(column=1, row=6, sticky=(W, E))

        self.match_venue = StringVar()
        ttk.Label(details_frame, text="Venue").grid(column=1, row=7, sticky=W)
        ttk.Entry(details_frame, width=20, textvariable=self.match_venue).grid(column=1, row=8, sticky=(W, E))

        ttk.Button(details_frame, text="Save", command=self.save).grid(column=1, row=9, sticky=W)

    def matches(self):
        self.show_view(self.matches_screen)
        self.refresh_match_teams()
        self.reload_matches()

    def new_match(self):
        self.db.add_match(self.home_team_position.get(), self.away_team_position.get(), self.match_date.get(), self.match_venue.get())
        self.editing_ids["match"] = None
        self.reload_matches()

    def load_matches(self, matches_list):
        matches = self.db.get_matches()

        for id, home_team, away_team, date, venue in matches:
            matches_list.insert("", "end", iid=str(id), values=(id, home_team, away_team, date, venue))

        self.configure_columns(matches_list)

    def edit_match(self):
        self.edit_record("match", self.matches_list, (
            self.home_team_position, self.away_team_position, self.match_date, self.match_venue,
        ))

    def delete_match(self):
        self.delete_record("match", self.matches_list)

    def reload_matches(self):
        match_id = self.selected_match_id()
        self.clear_list(self.matches_list)
        self.load_matches(self.matches_list)

        if match_id is not None and self.matches_list.exists(str(match_id)):
            self.matches_list.selection_set(str(match_id))

        self.refresh_match_appearances()

    def refresh_match_teams(self):
        team_names = [nation for team_id, nation in self.db.get_teams()]

        for menu, variable, placeholder in (
            (self.home_team_menu, self.home_team_position, "Select home team"),
            (self.away_team_menu, self.away_team_position, "Select away team"),
        ):
            selected_team = variable.get()
            menu.set_menu(placeholder, *team_names)
            if selected_team in team_names:
                variable.set(selected_team)

    def selected_match_id(self):
        selected = self.matches_list.selection()

        if not selected:
            return None
        
        return int(self.matches_list.item(selected[0], "values")[0])

    def search_matches(self):
        search_query = self.match_search_entry.get().strip().lower()
        self.clear_list(self.matches_list)

        for match in self.db.get_matches():
            match_id, home_team, away_team, date, venue = match
            if self.match_search.get() == "Search by team":
                fields = (home_team, away_team)

            elif self.match_search.get() == "Search by player":
                fields = [
                    f"{first_name} {last_name}"
                    for player_id, first_name, last_name, team_name
                    in self.db.get_detailed_participations(match_id)
                ]
            else:
                fields = (date,)

            if any(search_query in field.lower() for field in fields):
                self.matches_list.insert("", "end", iid=str(match_id), values=match)

        self.refresh_match_appearances()

    # player appearances

    def build_match_appearances(self, screen):
        appearances_frame = ttk.Frame(screen, padding=(3, 3, 12, 12))
        appearances_frame.grid(column=0, row=2, sticky=(N, W, E, S))
        ttk.Label(appearances_frame, text="Player Appearances").grid(column=1, row=1, sticky=W)
        cols = ("Player", "Team")
        self.appearances_list = ttk.Treeview(appearances_frame, columns=cols, show="headings")
        self.load_player_appearances(self.appearances_list)
        self.appearances_list.grid(column=1, row=2, sticky=(N, W, E, S))

        self.select_player = StringVar()
        self.eligible_player_ids = {}
        self.select_player_menu = ttk.OptionMenu(appearances_frame, self.select_player, "Select a match first")
        self.select_player_menu.grid(column=1, row=3, sticky=W)


        ttk.Button(appearances_frame, text="Add player", command=self.add_player_appearance).grid(column=2, row=3, sticky=W)
        ttk.Button(appearances_frame, text="Remove selected", command=self.remove_player_appearance).grid(column=3, row=3, sticky=W)

    def add_player_appearance(self):
        match_id = self.selected_match_id()
        player_id = self.eligible_player_ids.get(self.select_player.get())

        if match_id is None or player_id is None:
            messagebox.showerror("Cannot add player", "Select a match and an eligible player first.")

            return
        
        try:
            self.db.add_participation(match_id, player_id)

        except ValueError as e:
            messagebox.showerror("Cannot add player", str(e))

        self.refresh_match_appearances()

    def load_player_appearances(self, appearances_list):
        match_id = self.selected_match_id()
        appearances = self.db.get_detailed_participations(match_id) if match_id is not None else []

        for player_id, first_name, last_name, team_name in appearances:
            appearances_list.insert(
                "",
                "end",
                iid=str(player_id),
                values=(f"{first_name} {last_name}", team_name)
            )

        self.configure_columns(appearances_list)

    def remove_player_appearance(self):
        match_id = self.selected_match_id()
        selected = self.appearances_list.selection()
        if match_id is None or not selected:
            messagebox.showerror("Cannot remove player", "Select a match and a player appearance first.")
            return
        self.db.remove_participation(match_id, int(selected[0]))
        self.refresh_match_appearances()

    def refresh_match_appearances(self, event=None):
        self.clear_list(self.appearances_list)
        self.load_player_appearances(self.appearances_list)

        match_id = self.selected_match_id()
        players = self.db.get_eligible_players(match_id) if match_id is not None else []
        labels = [f"{first} {last} ({team})" for player_id, first, last, team in players]
        counts = Counter(labels)

        self.eligible_player_ids = {
            (f"{label} [ID {player[0]}]" if counts[label] > 1 else label): player[0]
            for label, player in zip(labels, players)
        }

        if players:
            placeholder = "Select eligible player"

        else:
            placeholder = "No eligible players"

        if match_id is None:
            placeholder = "Select a match first"

        self.select_player_menu.set_menu(placeholder, *self.eligible_player_ids)