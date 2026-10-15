# csc4710-hw1

Run the application from this directory:

```sh
python3 main.py
```

`main.py` initializes the SQLite database, loads the sample data, then opens the
Tkinter interface. Existing sample records are skipped; missing ones are inserted
on startup.

To add fictional sample teams, players, matches, and appearances, run:

```sh
python3 sample_data.py
```

Existing records are kept, and rerunning the script skips existing sample records.
The script inserts 10 sample players across seven of the 10 national teams, plus eight matches with player appearances.
