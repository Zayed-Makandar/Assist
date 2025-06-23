import subprocess
import sys
import os
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import requests
import base64
import threading

SPOTIFY_CLIENT_ID = "34a8fc278eeb409ea87d71fd683c6632"
SPOTIFY_CLIENT_SECRET = "02da12db4de146cbad935cf6a95f8ddc"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
SPOTIFY_REFRESH_TOKEN = "AQBEUfhqQEZEfjWndB3iBWEC7H2gEj9pCH8BO0ZQUnkk6uBWQRqAcer9ia4sIcLRdmwBAw-6v-ExX7QRMsA1HvSLYV2wxqbk2wcWH1lzCyJpAMbi2QTuyurqFF2Z1kb9r84"
SPOTIFY_TOKEN_CACHE = ".cache"

def load_spotify_tokens():
    try:
        with open(SPOTIFY_TOKEN_CACHE, "r") as f:
            data = json.load(f)
            return data["access_token"], data.get("refresh_token")
    except Exception:
        return None, None

def save_spotify_tokens(access_token, refresh_token=None):
    data = {"access_token": access_token}
    if refresh_token:
        data["refresh_token"] = refresh_token
    with open(SPOTIFY_TOKEN_CACHE, "w") as f:
        json.dump(data, f)

def refresh_access_token():
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        # Optionally update refresh_token if returned
        refresh_token = token_data.get("refresh_token", SPOTIFY_REFRESH_TOKEN)
        save_spotify_tokens(access_token, refresh_token)
        return access_token
    else:
        print("Failed to refresh Spotify token:", response.text)
        return None

class SystemCalls:
    def __init__(self):
        pass

    def get_spotify_client(self):
        import spotipy
        access_token, _ = load_spotify_tokens()
        if not access_token:
            access_token = refresh_access_token()
        return spotipy.Spotify(auth=access_token)

    def play_spotify_song(self, query):
        import time
        import spotipy
        access_token, _ = load_spotify_tokens()
        if not access_token:
            access_token = refresh_access_token()
            if not access_token:
                print("Spotify access token not found. Please authenticate.")
                try:
                    subprocess.Popen([r"C:\Users\crims\AppData\Roaming\Spotify\Spotify.exe"])
                except Exception:
                    pass
                return
        try:
            sp = spotipy.Spotify(auth=access_token)
            try:
                results = sp.search(q=query, type="track", limit=1)
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 401:
                    # Token expired, refresh and retry
                    access_token = refresh_access_token()
                    sp = spotipy.Spotify(auth=access_token)
                    results = sp.search(q=query, type="track", limit=1)
                else:
                    raise
            if results["tracks"]["items"]:
                track_uri = results["tracks"]["items"][0]["uri"]
                device_id = None
                for _ in range(10):  # Try for ~10 seconds
                    devices = sp.devices()
                    print("Devices found by Spotify API:", devices)  # <-- Debug print
                    if devices["devices"]:
                        device_id = devices["devices"][0]["id"]
                        break
                    else:
                        try:
                            subprocess.Popen([r"C:\Users\crims\AppData\Roaming\Spotify\Spotify.exe"])
                        except Exception:
                            pass
                        time.sleep(1)
                if device_id:
                    sp.start_playback(device_id=device_id, uris=[track_uri])
                else:
                    print("No active Spotify device found after waiting.")
            else:
                print("No track found for the query.")
        except Exception as e:
            print(f"Spotify playback error: {e}")
            try:
                subprocess.Popen([r"C:\Users\crims\AppData\Roaming\Spotify\Spotify.exe"])
            except Exception:
                pass

    def execute(self, intent, params):
        def open_application(app_name, paths):
            for path in paths:
                print(f"Trying {app_name} path: {path}")
                if os.path.exists(path):
                    subprocess.Popen([path])
                    print(f"Opened {app_name} from: {path}")
                    break

        if intent == "open_app":
            app = params.get("app", "").lower().strip()  # Normalize to lowercase and strip spaces

            # Map all PowerPoint and Excel command variants to the correct app name
            powerpoint_variants = [
                "powerpoint", "open powerpoint", "open Powerpoint", "Powerpoint", "Open Powerpoint",
                "open PowerPoint", "Open PowerPoint", "PowerPoint"
            ]
            excel_variants = [
                "excel", "open excel", "open Excel", "Excel", "Open Excel"
            ]

            if app in [v.lower() for v in powerpoint_variants]:
                app = "powerpoint"
            elif app in [v.lower() for v in excel_variants]:
                app = "excel"

            if app == "notepad":
                subprocess.Popen(["notepad.exe"])
            elif app == "calculator":
                subprocess.Popen(["calc.exe"])
            elif app == "word":
                print("Attempting to open Word...")
                try:
                    import win32com.client
                    word = win32com.client.Dispatch("Word.Application")
                    word.Visible = True
                    word.Documents.Add()
                    print("Opened Word via COM.")
                except Exception as e:
                    print(f"COM failed: {e}")
                    word_paths = [
                        r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                        r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                        r"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE",
                        r"C:\Program Files (x86)\Microsoft Office\Office16\WINWORD.EXE"
                    ]
                    threading.Thread(target=open_application, args=("Word", word_paths), daemon=True).start()
            elif app == "excel":
                print("Attempting to open Excel via external script...")
                try:
                    subprocess.Popen([sys.executable, r"c:\Users\crims\Assist\open_excel.py"])
                    print("Triggered open_excel.py script.")
                except Exception as e:
                    print(f"Failed to run open_excel.py: {e}")
            elif app == "powerpoint":
                print("Attempting to open PowerPoint via external script...")
                try:
                    subprocess.Popen([sys.executable, r"c:\Users\crims\Assist\open_powerpoint.py"])
                    print("Triggered open_powerpoint.py script.")
                except Exception as e:
                    print(f"Failed to run open_powerpoint.py: {e}")
            elif app == "spotify":
                try:
                    subprocess.Popen([r"C:\Users\crims\AppData\Roaming\Spotify\Spotify.exe"])
                except Exception:
                    try:
                        subprocess.Popen(["spotify.exe"])
                    except Exception:
                        import webbrowser
                        webbrowser.open("https://open.spotify.com/")
            elif app == "youtube":
                import webbrowser
                webbrowser.open("https://www.youtube.com/")
            # Add more apps as needed
        elif intent == "play_music":
            service = params.get("service", "")
            song = params.get("song", "")
            if service == "spotify":
                if song:
                    self.play_spotify_song(song)
                else:
                    try:
                        subprocess.Popen(["spotify.exe"])
                    except Exception:
                        import webbrowser
                        webbrowser.open("https://open.spotify.com/")
            elif service == "youtube":
                import webbrowser
                if song:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
                else:
                    webbrowser.open("https://www.youtube.com/")
        elif intent == "read_news":
            source = params.get("source", "mediastack").lower()
            if source == "mediastack":
                print("Sure! Here are today's top headlines from Mediastack for you:\n")
                self.get_latest_news()
            elif source == "otherapi":
                print("Sure! Here are today's top headlines from OtherAPI for you:\n")
                self.get_latest_news_from_other_api()
            else:
                print("Sorry, I don't recognize that news source.")
            print("Sure! Here are today's top headlines for you:\n")
            self.get_latest_news()
        # Add more apps as needed
        # Add more intent handling as needed

    def get_latest_news(self, keywords=None, limit=5):
        api_key = "fcb7854887117d44c1c56f5f1d22c91b"
        base_url = "http://api.mediastack.com/v1/news"
        params = {
            "access_key": api_key,
            "languages": "en",
            "limit": limit
        }
        if keywords:
            params["keywords"] = keywords
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                articles = data.get("data", [])
                if not articles:
                    print("No news articles found.")
                else:
                    print("Latest News Headlines:")
                    for article in articles:
                        print(f"- {article.get('title')}")
                        print(f"  Source: {article.get('source')}")
                        print(f"  URL: {article.get('url')}\n")
            else:
                print("Failed to fetch news:", response.text)
        except Exception as e:
            print(f"Error fetching news: {e}")
import os
print("Current working directory:", os.getcwd())