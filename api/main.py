import os
import requests
import uvicorn
from fastapi import FastAPI, Request

TOKEN = os.environ.get("IPG_BOT_TOKEN")
CHANNEL_ID = os.environ.get("IPG_CHANNEL_ID")

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

app = FastAPI()

@app.get("/", response_model=dict)
async def root():
    return {"message": "Hi!"}

@app.post("/data", response_model=str)
async def send_data(request: Request):
    data = await request.json()
    send_message(data["data"])
    return "sent successfully"