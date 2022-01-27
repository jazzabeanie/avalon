from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

html_template = """
<html>
    <head>
        <title>Avalon</title>
    </head>
    <body>
{html_body}
    </body>
</html>
"""

body_template = """
<p style='font-size:30px'>{body_message}</p>
"""

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
    message = f"you just created a new game. Your game id is {new_game_id}."
    body = body_template.format(body_message = message)
    return HTMLResponse(content=html_template.format(html_body = body), status_code=200) # FIXME: return the link to the new game.

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
    message = f"game: {game_id}<br>status: {game_status}<br>number of players: {num_players}"
    body = body_template.format(body_message = message)
    return HTMLResponse(content=html_template.format(html_body = body), status_code=200)

@app.get("/{game_id}/{player_name}")
async def player_page(game_id: int, player_name: str):
    connection = sqlite3.connect('game.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT player_name FROM player WHERE game_id = '{game_id}' AND player_name = '{player_name}'")
    row = cursor.fetchone()
    if row == None:
        cursor.execute(f"INSERT INTO player (game_id, player_name) VALUES ('{game_id}', '{player_name}')")
        message = f"welcome {player_name}, you have been added to the game."
    elif len(row) == 1:
        message = f"welcome back {player_name}"
    else:
        message = f"error, there are two players named '{player_name}' in game_id = {game_id}"
    connection.commit()
    connection.close()
    body = body_template.format(body_message = message)
    return HTMLResponse(content=html_template.format(html_body = body), status_code=200)

