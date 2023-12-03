import os 
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = os.environ.get('IPG_BOT_TOKEN')
CHANNEL_ID = os.environ.get('IPG_CHANNEL_ID')

url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages'

@app.route("/")
def index():
    return jsonify({"NOTE": "Do not use this library. It is for experimental purposes only."})

@app.route("/data", methods=["POST"])
def send_data():
    try:
        data = request.json.get("data")

        if not data:
            return jsonify({"error": "Data not provided"}), 400

        send_message(data)
        return jsonify("sent successfully")
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

def send_message(message):
    if len(message) <= 2000:
        data = {
            "content": message,
        }

        try:
            response = requests.post(url, json=data, headers={
                'Authorization': f'Bot {TOKEN}',
                'Content-Type': 'application/json',
            })

            if response.status_code != 200:
                print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print("Error sending message:", str(e))
    else:
        send_message(message[:2000])
        send_message(message[2000:])

if __name__ == "__main__":
    app.run()   