from tkinter import *
from tkinter import ttk

class WorldCupDBManager:

    def __init__(self, root):

        root.title("World Cup 2026 — Database Manager")

        mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Label(mainframe, text="World Cup 2026 Database Manager", font=("Helvetica", 16)).grid(column=1, row=0, columnspan=3, sticky=W)
        #ttk.Label(mainframe, text="Select an option below to manage the database.").grid(column=1, row=1, columnspan=3, sticky=W)
        ttk.Button(mainframe, text="Players", command=self.players).grid(column=1, row=1, sticky=W)
        ttk.Button(mainframe, text="Teams", command=self.matches).grid(column=2, row=1, sticky=W)
        ttk.Button(mainframe, text="Matches", command=self.teams).grid(column=3, row=1, sticky=W)

        playersframe = ttk.Frame(mainframe, padding=(3, 3, 12, 12))
        playersframe.grid(column=1, row=2, sticky=(N, W, E, S))

        ttk.Button(playersframe, text="New Player", command=self.new_player).grid(column=2, row=2, sticky=W)
        ttk.Button(playersframe, text="Edit Selected", command=self.edit_player).grid(column=3, row=2, sticky=W)
        ttk.Button(playersframe, text="Delete Selected", command=self.delete_player).grid(column=4, row=2, sticky=W)

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
        
    def calculate(self, *args):
        try:
            value = float(self.player_firstname.get())
            self.meters.set(round(0.3048 * value, 4))
        except ValueError:
            pass

    def players(self):
        pass

    def matches(self):
        pass

    def teams(self):
        pass

    def new_player(self):
        pass

    def edit_player(self):
        pass

    def delete_player(self):
        pass

    def save(self):
        pass

root = Tk()
WorldCupDBManager(root)
root.mainloop()