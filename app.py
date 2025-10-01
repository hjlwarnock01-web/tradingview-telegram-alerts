import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True) or {"raw": request.data.decode()}
    
    # Extract pair
    pair = payload.get("symbol", "Unknown")
    
    # Extract time (TradingView usually sends timestamp or time string)
    tv_time = payload.get("time", None)
    if tv_time:
        try:
            # Convert timestamp to HH:MM
            timestamp = int(tv_time) / 1000  # if TradingView sends milliseconds
            time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M")
        except:
            time_str = str(tv_time)
    else:
        time_str = "Unknown"
    
    # Final message
    text = f"1H Zone Hit {pair} @{time_str}"
    
    requests.post(TG_API, json={"chat_id": CHAT_ID, "text": text})
    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
