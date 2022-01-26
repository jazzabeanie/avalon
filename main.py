from fastapi import FastAPI
import sqlite3

app = FastAPI()

connection = sqlite3.connect('game.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS game (
  id INTEGER PRIMARY KEY AUTOINCREMENT
  ,status TEXT
  ,num_players INTEGER
)
        """)

connection.commit()
connection.close()

@app.get("/")
async def root():
    connection = sqlite3.connect('game.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO game (status, num_players) VALUES ('not started', 0)")
    cursor.execute("SELECT MAX(id) FROM game")
    row = cursor.fetchall()
    new_game_id = row[0][0]
    connection.commit()
    connection.close()
    return {"message": f"you just created a new game. Your game id is {new_game_id}."} # FIXME: return the link to the new game.

@app.get("/{game_id}")
async def get_status(game_id):
    connection = sqlite3.connect('game.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM game WHERE id = {game_id}")
    row = cursor.fetchall()
    game_status = row[0][1]
    num_players = row[0][2]
    connection.commit()
    connection.close()
    return {"message": f"get status of game id = {game_id}", "game status": f"{game_status}", "number of players": f"{num_players}"}

