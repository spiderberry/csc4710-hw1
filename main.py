from tkinter import Tk

from gui import WorldCupDBManager
from initDB import Database


def main():
    db = Database()
    root = Tk()
    WorldCupDBManager(root, db)
    root.mainloop()


if __name__ == "__main__":
    main()
