from initDB import Database


def initialize_sample_data(db):
    teams = (
        "Jamaica", "United States of America", "Iceland", "Japan", "Ghana",
        "Brazil", "Morocco", "Canada", "Mexico", "South Korea",
    )

    players = (
        ("Dante", "Beckford", "11/03/1994", "Goalkeeper", "Jamaica"),
        ("Zuri", "Campbell", "08/17/2003", "Forward", "Jamaica"),
        ("Miles", "Navarro", "02/29/2000", "Midfielder", "United States of America"),
        ("Adrian", "Okafor", "12/09/1997", "Defender", "United States of America"),
        ("Einar", "Sigurdsson", "01/21/1992", "Goalkeeper", "Iceland"),
        ("Ren", "Sakamoto", "05/06/2004", "Midfielder", "Japan"),
        ("Kwame", "Boateng", "09/14/1999", "Forward", "Ghana"),
        ("Caio", "Moreira", "07/27/2002", "Forward", "Brazil"),
        ("Thiago", "Azevedo", "03/11/1996", "Defender", "Brazil"),
        ("Youssef", "El Amrani", "10/30/2001", "Midfielder", "Morocco"),
    )

    matches = (
        ("Jamaica", "United States of America", "06/12/2026", "Mercedes-Benz Stadium"),
        ("Brazil", "Japan", "06/15/2026", "Tokyo Arena"),
        ("Ghana", "Morocco", "06/18/2026", "Copper Canyon Stadium"),
        ("Iceland", "Jamaica", "06/22/2026", "Kingston Field"),
        ("United States of America", "Brazil", "06/27/2026", "MetLife Stadium"),
        ("Japan", "Canada", "06/30/2026", "Maple Crown Arena"),
        ("Mexico", "South Korea", "07/03/2026", "Sierra Verde Stadium"),
        ("Morocco", "Iceland", "07/07/2026", "Atlas Gate Arena"),
    )

    appearances = (
        ("Dante Beckford", "Zuri Campbell", "Miles Navarro", "Adrian Okafor"),
        ("Caio Moreira", "Ren Sakamoto"),
        ("Kwame Boateng",),
        ("Einar Sigurdsson", "Zuri Campbell"),
        ("Thiago Azevedo",),
        (),
        (),
        ("Youssef El Amrani", "Einar Sigurdsson"),
    )

    existing_teams = {nation for team_id, nation in db.get_teams()}
    for nation in teams:
        if nation not in existing_teams:
            db.add_team(nation)

    existing_players = {(first, last, team) for player_id, first, last, dob, position, team in db.get_players()}
    for first, last, dob, position, team in players:

        if (first, last, team) not in existing_players:
            db.add_player(first, last, dob, position, team)

    existing_matches = {(home, away, day): match_id for match_id, home, away, day, venue in db.get_matches()}
    for home, away, day, venue in matches:

        if (home, away, day) not in existing_matches:
            db.add_match(home, away, day, venue)

    match_ids = {(home, away, day): match_id for match_id, home, away, day, venue in db.get_matches()}

    player_ids = {
        (f"{first} {last}", team): player_id
        for player_id, first, last, dob, position, team in db.get_players()
    }
    player_teams = {f"{first} {last}": team for first, last, dob, position, team in players}
    for match, names in zip(matches, appearances):

        match_id = match_ids[match[:3]]
        added_ids = {player_id for player_id, first, last, team in db.get_detailed_participations(match_id)}

        for name in names:
            player_id = player_ids[(name, player_teams[name])]

            if player_id not in added_ids:
                db.add_participation(match_id, player_id)

    print("Sample data created: 10 sample players, 10 sample teams, and 8 sample matches.")

if __name__ == "__main__":
    initialize_sample_data(Database())
