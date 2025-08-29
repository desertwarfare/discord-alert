"""
Discord Alert Monitor Script (Self Automation)
Author: desert.warfare

This is a script I made a while back, the story behind it is that I was part of a SWAT team in a roleplay game.
The idea behind it is whenever they needed SWAT ingame, they would tag us in a channel and ask us to hop in, however I would miss these tags because I don't check discord often.
Instead, this script would poll for any tags with keywords such as "requesting SWAT" and play a continous alarm sound and prompt me whether to confirm response and hop ingame.

This is one of my first Python scripts ever, so if it looks messy or not good, then I don't really care. As long as it worked for me, that was good enough until I received a warning from Discord.

Requirements:
- Python 3.8+
- Libraries: requests, pygame


WARNING: This script uses a user token, which is **against Discord's Terms of Service** for automation.
Using a user token for automation can result in your Discord account being permanently banned.
This script is intended for educational purposes only. **DO NOT** use it with your main Discord account. BETTER YET, use it with a bot or something.

For safe automation, consider using a **Discord bot** and the official [discord.py](https://discordpy.readthedocs.io/en/stable/) library.
"""



# --- Config ---


import logging

# --- Logging setup ---
logging.basicConfig(
    filename="discord_alerts.log",
    filemode="a",
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)
import requests
import pygame
import winsound
import subprocess
import ctypes
import threading
import time
import os
from datetime import datetime

# --- Config ---
TOKEN = "1234" # REPLACE WITH YOUR DISCORD TOKEN
PAGER_CHANNEL_ID = 1234 # REPLACE WITH CHANNEL ID
KEYWORDS = ["@SOD: SEB", "barricaded", "active", "requesting", "Need a team", "HRAW", "DEPLOY", "SEB assets", "STATUS: ACTIVE"]
ALERT_SOUND = "alert.wav"
ALARM_SOUND = "bugle_call.mp3"
GAME_PATH = r"C:\GAME\game.exe"
SERVER_IP = "localhost:22005"
HEADERS = {
    "Authorization": TOKEN,
    "User-Agent": "Mozilla/5.0"
}
LOG_FILE = "alert_log.txt"

last_message_id = None
alarm_playing = False

def log_alert(content):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {content}\n")


def play_alert():
    for _ in range(2):
        winsound.PlaySound(ALERT_SOUND, winsound.SND_FILENAME)


def play_startup_alarm():
    global alarm_playing
    pygame.mixer.init()
    pygame.mixer.music.load(ALARM_SOUND)
    pygame.mixer.music.play(-1)
    while alarm_playing:
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()


def launch_game():
    try:
        subprocess.Popen([GAME_PATH])
        time.sleep(8)  # Give the game time to load
        #subprocess.Popen([r"C:\game\autoconnect_ragemp.exe"])
    except Exception as e:
        print("Game launch failed:", e)



def check_channel():
    global last_message_id, alarm_playing
    url = f"https://discord.com/api/v9/channels/{PAGER_CHANNEL_ID}/messages?limit=1"

    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("Failed to fetch messages:", response.text)
            return

        message = response.json()[0]
        message_id = message["id"]
        message_content = message["content"].lower()

        if message_id != last_message_id and any(k in message_content for k in KEYWORDS):
            last_message_id = message_id
            print("\n🚨 Alert Detected!")
            log_alert(message["content"])

            alarm_playing = True
            threading.Thread(target=play_startup_alarm).start()

            ctypes.windll.user32.MessageBoxW(0, message["content"], "🚨 Discord Game Alert", 0x40 | 0x1 | 0x40000)

            alarm_playing = False
            response_box = ctypes.windll.user32.MessageBoxW(
                0,
                f"Do you wish to send a message confirming your response?\n\nSituation:\n{message['content']}",
                "Confirm response",
                0x04 | 0x20 | 0x40000
            )
            if response_box == 6:  # IDYES
                send_response("Enroute.")
                launch = ctypes.windll.user32.MessageBoxW(
                    0,
                    "Launch game?",
                    "Confirm Game Launch",
                    0x04 | 0x20 | 0x40000
                )
                if launch == 6:
                    launch_game()

    except Exception as e:
        print("Error checking messages:", e)


def send_response(content):
    url = f"https://discord.com/api/v9/channels/{PAGER_CHANNEL_ID}/messages"
    payload = {"content": content}
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print("Failed to send message:", response.text)


# --- Main loop ---
if __name__ == "__main__":
    print("✅ Alert Monitor Running (Polling mode)...")
    play_alert()
    while True:
        check_channel()
        time.sleep(10)  # Check every 10 seconds, this may help avoid being flagged by Discord and receiving a ban for self-automation