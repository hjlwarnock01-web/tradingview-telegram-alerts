import os, requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True) or {"raw": request.data.decode()}
    text = "📢 TradingView Alert\n\n"
    if isinstance(payload, dict):
        text += "\n".join(f"{k}: {v}" for k, v in payload.items())
    else:
        text += str(payload)

    requests.post(TG_API, json={"chat_id": CHAT_ID, "text": text})
    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
