import requests
import schedule
import time
import threading
from telegram import Bot
from flask import Flask

# === Telegram Bot Credentials ===
BOT_TOKEN = "7944061765:AAHjX3r3pi-qZgrjCTtcvvba3uuWJMpi30o"
CHAT_ID = "5979964993"

bot = Bot(token=BOT_TOKEN)

# === Fetch and Send Jokes ===
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
        print(f"✅ Sent: {joke}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

# ✅ Send a test message on startup
try:
    bot.send_message(chat_id=CHAT_ID, text="✅ Bot restarted and ready.")
except Exception as e:
    print(f"❌ Could not send startup message: {e}")

# === Schedule the joke every 5 minutes ===
schedule.every(5).minutes.do(send_joke)

def run_scheduler():
    while True:
        schedule.run_pending()
        print("⏰ Scheduler running...")
        time.sleep(1)

# Start scheduler in background thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# === Flask Web App to keep Render alive ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Joke Bot is running!"

# ✅ Run Flask in the main thread so Render detects port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
