import os, requests
from flask import Flask, request, jsonify

TOKEN = os.getenv("IPG_BOT_TOKEN")
CHANNEL_ID = os.getenv("IPG_CHANNEL_ID")

url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages'
headers = {
    'Authorization': f'Bot {TOKEN}',
    'Content-Type': 'application/json',
}

def send_message(message):
    if len(message) <= 2000:
        data = {
            'content': message,
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')
    else:
        send_message(message[:2000])
        send_message(message[2000:])

app = Flask(__name__)

@app.route('/', methods=['POST'])
def post_example():
    if request.method == 'POST':
        data = request.json
        send_message(data["data"])
        
        return jsonify("sent successfully")

if __name__ == '__main__':
    app.run()