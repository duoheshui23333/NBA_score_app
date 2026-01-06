import time, json, requests, threading
from datetime import datetime

PUSHOVER_USER_KEY = "ubcom8mjarv2i13vr15gqsm32g3f33"
PUSHOVER_API_TOKEN = "arxdvtqbqa9udvi4ojcv82nvharzqn"

HISTORY_FILE = "/data/notified_50pts.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_history(h):
    with open(HISTORY_FILE, "w") as f:
        json.dump(list(h), f)

def send_push(title, msg):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={"token": PUSHOVER_API_TOKEN, "user": PUSHOVER_USER_KEY,
              "title": title, "message": msg},
        timeout=10
    )

def fetch_games():
    url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    return r.json()["scoreboard"]["games"]

def watch_loop():
    print("Watcher started")
    history = load_history()

    while True:
        try:
            games = fetch_games()

            for g in games:
                gid = g["gameId"]
                
                # Extract game leaders (available in the API)
                leaders = []
                if "gameLeaders" in g:
                    gl = g["gameLeaders"]
                    if "homeLeaders" in gl:
                        leaders.append(gl["homeLeaders"])
                    if "awayLeaders" in gl:
                        leaders.append(gl["awayLeaders"])

                for leader in leaders:
                    pts = leader.get("points", 0)
                    name = leader.get("name", "Unknown")

                    if pts >= 50:
                        key = f"{gid}-{name}"
                        if key not in history:
                            send_push(f"{name} scored {pts}", f"{pts} points")
                            print("PUSH:", name, pts)
                            history.add(key)

            save_history(history)

        except Exception as e:
            print("Error:", e)
            import traceback
            traceback.print_exc()

        time.sleep(300)

def start_background():
    print("Starting watcher thread")
    t = threading.Thread(target=watch_loop, daemon=True)
    t.start()
