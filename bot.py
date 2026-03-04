import requests
import time
import os

CHANNEL = "dj___shige"

WEBHOOK = os.getenv("DISCORD_WEBHOOK")
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

last_title = None

TWITCH_COLOR = 9146


def get_token():

    r = requests.post(
        "https://id.twitch.tv/oauth2/token",
        params={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
    )

    return r.json()["access_token"]


def get_stream(token):

    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(
        f"https://api.twitch.tv/helix/streams?user_login={CHANNEL}",
        headers=headers
    ).json()

    if not r["data"]:
        return None

    return r["data"][0]


def send_title(old, new):

    embed = {
        "title": "✏️ Twitch Title Updated",
        "url": f"https://twitch.tv/{CHANNEL}",
        "color": TWITCH_COLOR,
        "fields": [
            {
                "name": "Before",
                "value": old,
                "inline": False
            },
            {
                "name": "After",
                "value": new,
                "inline": False
            }
        ],
        "footer": {
            "text": "Twitch Monitor"
        }
    }

    requests.post(WEBHOOK, json={"embeds":[embed]})


def main():

    global last_title

    token = get_token()

    while True:

        stream = get_stream(token)

        if stream:

            title = stream["title"]

            # 初回保存
            if last_title is None:
                last_title = title

            # タイトル変更検知
            if title != last_title:

                send_title(last_title, title)

                last_title = title

        time.sleep(60)


main()
