from tkinter import *
from tkinter import ttk
import initDB

class WorldCupDBManager:

    def __init__(self, root):

        self.db = initDB.Database()

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

    def build_players_screen(self, parent):
        screen = ttk.Frame(parent)
        self.build_player_list(screen)
        self.build_player_details(screen)

        return screen

    def build_player_list(self, screen):
        playersframe = ttk.Frame(screen, padding=(3, 3, 12, 12))
        playersframe.grid(column=0, row=0, sticky=(N, W, E, S))
        ttk.Label(playersframe, text="Players").grid(column=1, row=1, sticky=W)
        cols = ("ID", "First Name", "Last Name", "Date of Birth", "Position", "Team ID")
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
        ttk.Label(detailsframe, text="First Name:").grid(column=1, row=1, sticky=W)
        ttk.Entry(detailsframe, width=20, textvariable=self.player_firstname).grid(column=1, row=2, sticky=(W, E))
        
        self.player_lastname = StringVar()
        ttk.Label(detailsframe, text="Last Name:").grid(column=1, row=3, sticky=W)
        ttk.Entry(detailsframe, width=20, textvariable=self.player_lastname).grid(column=1, row=4, sticky=(W, E))
        
        self.player_dob = StringVar()
        ttk.Label(detailsframe, text="Date of Birth (MM/DD/YYYY):").grid(column=1, row=5, sticky=W)
        ttk.Entry(detailsframe, width=20, textvariable=self.player_dob).grid(column=1, row=6, sticky=(W, E))
        
        self.player_position = StringVar()
        positions = ("Forward", "Midfielder", "Defender", "Goalkeeper")
        ttk.Label(detailsframe, text="Position:").grid(column=1, row=7, sticky=W)
        position_menu = ttk.OptionMenu(detailsframe, self.player_position, positions[0], *positions)
        position_menu.grid(column=1, row=8, sticky=(W, E))

        self.player_team_id = StringVar()
        ttk.Label(detailsframe, text="Team:").grid(column=1, row=9, sticky=W)
        ttk.Entry(detailsframe, width=20, textvariable=self.player_team_id).grid(column=1, row=10, sticky=(W, E))

        ttk.Button(detailsframe, text="Save", command=self.save).grid(column=1, row=11, sticky=W)

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

    def build_matches_screen(self, parent):
        return ttk.Frame(parent)

    # Navigation and button actions
    def show_view(self, frame):
        if self.current_view is not None:
            self.current_view.grid_remove()

        self.current_view = frame
        self.current_view.grid()
    
    def players(self):
        self.show_view(self.players_screen)
        self.clear_list(self.players_list)
        self.load_players(self.players_list)
        

    def matches(self):
        self.show_view(self.matches_screen)

    def teams(self):
        self.show_view(self.teams_screen)
        self.clear_list(self.teams_list)
        self.load_teams(self.teams_list)
        

    def clear_list(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

    def load_teams(self, teams_list):
        teams = self.db.get_teams()

        for id, nation in teams:
            teams_list.insert("", "end", values=(id, nation))

        for col in teams_list["columns"]:
            teams_list.heading(col, text=col)
            teams_list.column(col, width=100, minwidth=60)
        
    def new_team(self):
        self.db.add_team(self.team_nation.get())

    def edit_team(self):
        pass

    def delete_team(self):
        pass

    def load_players(self, players_list):
        players = self.db.get_players()

        for id, first_name, last_name, date_of_birth, position, team_id in players:
            players_list.insert("", "end", values=(id, first_name, last_name, date_of_birth, position, team_id))

        for col in players_list["columns"]:
            players_list.heading(col, text=col)
            players_list.column(col, width=100, minwidth=60)

    def new_player(self):
        self.db.add_player(self.player_firstname.get(), self.player_lastname.get(), self.player_dob.get(), self.player_position.get(), self.player_team_id.get())

    def edit_player(self):
        pass

    def delete_player(self):
        pass

    def save(self):
        pass

    

root = Tk()
WorldCupDBManager(root)
root.mainloop()