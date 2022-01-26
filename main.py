from fastapi import FastAPI
import sqlite3

app = FastAPI()

connection = sqlite3.connect('game.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS game (
  id INTEGER PRIMARY KEY AUTOINCREMENT
  ,status TEXT
)
        """)
cursor.execute("""

CREATE TABLE IF NOT EXISTS player (
  game_id INTEGER
  ,player_name TEXT
)
        """)

connection.commit()
connection.close()

@app.get("/")
async def root():
    connection = sqlite3.connect('game.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO game (status) VALUES ('not started')")
    cursor.execute("SELECT MAX(id) FROM game")
    row = cursor.fetchall()
    new_game_id = row[0][0]
    connection.commit()
    connection.close()
    return {"message": f"you just created a new game. Your game id is {new_game_id}."} # FIXME: return the link to the new game.

@app.get("/{game_id}")
async def get_status(game_id: int):
    connection = sqlite3.connect('game.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT status FROM game WHERE id = {game_id}")
    row = cursor.fetchone()
    game_status = row[0]
    cursor.execute(f"SELECT player_name FROM player WHERE game_id = {game_id}")
    rows = cursor.fetchall()
    player_names = [i[0] for i in rows]
    num_players = len(player_names)
    connection.commit()
    connection.close()
    return {"message": f"get status of game id = {game_id}", "game status": f"{game_status}", "number of players": f"{num_players}", "players": f"{sorted(player_names)}"}

@app.get("/{game_id}/{player_name}")
async def player_page(game_id: int, player_name: str):
    connection = sqlite3.connect('game.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT player_name FROM player WHERE game_id = '{game_id}' AND player_name = '{player_name}'")
    row = cursor.fetchone()
    if row == None:
        cursor.execute(f"INSERT INTO player (game_id, player_name) VALUES ('{game_id}', '{player_name}')")
        message = {"message": f"welcome {player_name}, you have been added to the game."}
    elif len(row) == 1:
        message = {"message": f"welcome back {player_name}"}
    else:
        message = {"message": f"error, there are two players named '{player_name}' in game_id = {game_id}"}
    connection.commit()
    connection.close()
    return message

