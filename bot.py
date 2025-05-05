import requests
import schedule
import time
import threading
from telegram import Bot
from flask import Flask
from threading import Thread

# === Telegram Bot Credentials ===
BOT_TOKEN = "7944061765:AAHjX3r3pi-qZgrjCTtcvvba3uuWJMpi30o"
CHAT_ID = "5979964993"

# Initialize Telegram bot
bot = Bot(token=BOT_TOKEN)

# === Function to fetch joke from JokeAPI ===
def fetch_joke():
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Programming,Miscellaneous?type=single")
        data = res.json()
        return data.get("joke", "No joke today 😅")
    except Exception as e:
        return f"API error: {e}"

# === Function to send joke to Telegram ===
def send_joke():
    joke = fetch_joke()
    try:
        bot.send_message(chat_id=CHAT_ID, text=joke)
        print(f"✅ Sent: {joke}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

# === Manual test to confirm bot works ===
try:
    bot.send_message(chat_id=CHAT_ID, text="✅ Test message from bot")
    print("✅ Test message sent.")
except Exception as e:
    print(f"❌ Failed to send test message: {e}")

# === Schedule joke every 5 minutes ===
schedule.every(5).minutes.do(send_joke)

def run_scheduler():
    while True:
        schedule.run_pending()
        print("⏰ Scheduler running...")
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# === Minimal Flask app to keep Render alive ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()
