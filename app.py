import os

from flask import Flask, jsonify, request
from twilio.rest import Client

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "TradingView Phone Alert is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    # Read the alert sent by TradingView
    data = request.get_json(silent=True) or {}

    symbol = str(data.get("symbol", "TradingView"))
    price = str(data.get("price", "your selected level"))
    message = str(
        data.get(
            "message",
            f"Trading alert. {symbol} has reached {price}."
        )
    )

    # Get private credentials from Render environment variables
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    twilio_number = os.environ["TWILIO_PHONE_NUMBER"]
    my_number = os.environ["MY_PHONE_NUMBER"]

    client = Client(account_sid, auth_token)

   call = client.calls.create(
    url="https://webhooks.twilio.com/v1/Voice/Template/voice_text_to_speech",
    to=my_number,
    from_=twilio_number,
    )

    return jsonify({
        "success": True,
        "call_sid": call.sid
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
