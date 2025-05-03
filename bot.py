import requests
import schedule
import time
import threading
from telegram import Bot
from flask import Flask
from threading import Thread

# Keep-alive web server
app = Flask('')
@app.route('/')
def home():
    return "Bot is running."

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN"
CHAT_ID = "PASTE_YOUR_CHAT_ID"

bot = Bot(token=BOT_TOKEN)

def fetch_joke():
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Programming,Miscellaneous?type=single")
        data = res.json()
        return data.get("joke", "No joke today 😅")
    except Exception as e:
        return f"API error: {e}"

def send_joke():
    joke = fetch_joke()
    try:
        bot.send_message(chat_id=CHAT_ID, text=joke)
        print(f"Sent: {joke}")
    except Exception as e:
        print(f"Telegram error: {e}")

schedule.every(2).hours.do(send_joke)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler).start()
