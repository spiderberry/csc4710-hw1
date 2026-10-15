from tkinter import Tk

from gui import WorldCupDBManager
from initDB import Database
from sample_data import initialize_sample_data


def main():
    db = Database()
    initialize_sample_data(db)
    root = Tk()
    WorldCupDBManager(root, db)
    root.mainloop()


if __name__ == "__main__":
    main()
