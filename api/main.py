import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = os.environ.get('IPG_BOT_TOKEN')
GUILD_ID = os.environ.get('IPG_GUILD_ID')

url_channels = f'https://discord.com/api/v10/guilds/{GUILD_ID}/channels'
url_messages = f'https://discord.com/api/v10/channels/{{channel_id}}/messages'

@app.route("/")
def index():
    return jsonify({"NOTE": "Do not use this library. It is for experimental purposes only."})

@app.route("/data", methods=["POST"])
def send_data():
    try:
        data = request.json.get("data")

        if not data:
            return jsonify({"error": "Data not provided"}), 400

        new_channel_id = create_channel(data)
        send_message(new_channel_id, data)
        return jsonify("sent successfully")
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

def create_channel(channel_name):
    data = {
        "name": channel_name,
        "type": 0  # 0 for text channel, adjust if needed
    }

    try:
        response = requests.post(url_channels, json=data, headers={
            'Authorization': f'Bot {TOKEN}',
            'Content-Type': 'application/json',
        })

        if response.status_code == 201:
            return response.json()['id']
        else:
            print(f"Failed to create channel. Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print("Error creating channel:", str(e))
        return None

def send_message(channel_id, message):
    if len(message) <= 2000:
        data = {
            "content": message,
        }

        try:
            response = requests.post(url_messages.format(channel_id=channel_id), json=data, headers={
                'Authorization': f'Bot {TOKEN}',
                'Content-Type': 'application/json',
            })

            if response.status_code != 200:
                print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print("Error sending message:", str(e))
    else:
        send_message(channel_id, message[:2000])
        send_message(channel_id, message[2000:])

if __name__ == "__main__":
    app.run()
