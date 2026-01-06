import requests
import json

url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
data = r.json()

if data['scoreboard']['games']:
    g = data['scoreboard']['games'][0]
    print("Game ID:", g.get('gameId'))
    print("\nGameLeaders structure:")
    print(json.dumps(g.get('gameLeaders'), indent=2))
