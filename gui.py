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

        playersframe = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
        playersframe.grid(column=1, row=2, sticky=(N, W, E, S))
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

        detailsframe = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
        detailsframe.grid(column=2, row=2, sticky=(N, W, E, S))

        ttk.Label(detailsframe, text="Player Details", font=("Helvetica", 14)).grid(column=1, row=0, columnspan=3, sticky=W)
        
        ttk.Label(detailsframe, text="First Name:").grid(column=1, row=1, sticky=W)
        self.player_firstname = StringVar()
        ttk.Entry(detailsframe, width=20, textvariable=self.player_firstname).grid(column=2, row=1, sticky=(W, E))
        
        ttk.Label(detailsframe, text="Last Name:").grid(column=1, row=2, sticky=W)
        self.player_lastname = StringVar()
        ttk.Entry(detailsframe, width=20, textvariable=self.player_lastname).grid(column=2, row=2, sticky=(W, E))
        
        ttk.Label(detailsframe, text="Date of Birth (YYYY-MM-DD):").grid(column=1, row=3, sticky=W)
        self.player_dob = StringVar()
        ttk.Entry(detailsframe, width=20, textvariable=self.player_dob).grid(column=2, row=3, sticky=(W, E))
        
        ttk.Label(detailsframe, text="Position:").grid(column=1, row=4, sticky=W)
        self.player_position = StringVar()
        ttk.Entry(detailsframe, width=20, textvariable=self.player_position).grid(column=2, row=4, sticky=(W, E))
        
        ttk.Label(detailsframe, text="Team:").grid(column=1, row=5, sticky=W)
        self.player_team_id = StringVar()
        ttk.Entry(detailsframe, width=20, textvariable=self.player_team_id).grid(column=2, row=5, sticky=(W, E))

        ttk.Button(detailsframe, text="Save", command=self.save).grid(column=2, row=6, sticky=W)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)
        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def players(self):
        pass

    def matches(self):
        pass

    def teams(self):
        pass

    def new_player(self):
        self.db.add_player(self.player_firstname.get(), self.player_lastname.get(), self.player_dob.get(), self.player_position.get(), self.player_team_id.get())

    def edit_player(self):
        pass

    def delete_player(self):
        pass

    def save(self):
        pass

    def load_players(self, players_list):
        players = self.db.get_players()

        for id, first_name, last_name, date_of_birth, position, team_id in players:
            players_list.insert("", "end", values=(id, first_name, last_name, date_of_birth, position, team_id))

        for col in players_list["columns"]:
            players_list.heading(col, text=col)
            players_list.column(col, width=100, minwidth=60)
        players_list.grid(column=1, row=2, columnspan=3, sticky=(N, S, W, E))

root = Tk()
WorldCupDBManager(root)
root.mainloop()