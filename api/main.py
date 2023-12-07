import os
from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

TOKEN = os.environ.get('IPG_BOT_TOKEN')
GUILD_ID = os.environ.get('IPG_GUILD_ID')

create_channel_url = f'https://discord.com/api/v10/guilds/{GUILD_ID}/channels'
send_message_url = f'https://discord.com/api/v10/channels/{{}}/messages'

@app.route("/")
def index():
    return jsonify({"NOTE": "Do not use this library. It is for experimental purposes only."})

@app.route("/data", methods=["POST"])
def send_data():
    try:
        data = request.json.get("data")

        if not data:
            return jsonify({"error": "Data not provided"}), 400

        channel_id = create_channel_and_send_message(data)
        return jsonify({"channel_id": channel_id})
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

def create_channel_and_send_message(message):
    try:
        current_time = datetime.datetime.now().strftime("%d/%m/%Y")
        try:
            channel_name = message.split("\n")[8].split(":")[1].strip() + f"-{current_time}"
        except IndexError:
            channel_name = f"channel_{current_time}"
        
        create_channel_data = {
            "name": channel_name,
            "type": 0
        }

        create_channel_response = requests.post(create_channel_url, json=create_channel_data, headers={
            'Authorization': f'Bot {TOKEN}',
            'Content-Type': 'application/json',
        })

        if create_channel_response.status_code not in [200, 201]:
            print(f"Failed to create channel. Status code: {create_channel_response.status_code}, Response: {create_channel_response.text}")
            return None

        channel_id = create_channel_response.json().get('id')

        send_message_recursive(channel_id, message)

        return channel_id
    except Exception as e:
        print("Error creating channel and sending message:", str(e))
        return None

def send_message_recursive(channel_id, message):
    if len(message) <= 2000:
        send_message_data = {
            "content": message,
        }

        try:
            response = requests.post(send_message_url.format(channel_id), json=send_message_data, headers={
                'Authorization': f'Bot {TOKEN}',
                'Content-Type': 'application/json',
            })

            if response.status_code != 200:
                print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print("Error sending message:", str(e))
    else:
        send_message_recursive(channel_id, message[:2000])
        send_message_recursive(channel_id, message[2000:])

if __name__ == "__main__":
    app.run()