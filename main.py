import os
from fastapi import FastAPI, Request
import httpx
from groq import Groq

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_KEY)

app = FastAPI()
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    async with httpx.AsyncClient() as http_client:
        await http_client.post(url, json={"chat_id": chat_id, "text": text})

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    if "message" in body:
        chat_id = body["message"]["chat"]["id"]
        user_text = body["message"]["text"]

        # Generate poem using Groq
        response = client.chat.completions.create(
            model="llama3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a poetic AI that writes mystical, romantic, deep poems."},
                {"role": "user", "content": f"Write a poem about {user_text}."}
            ]
        )

        poem = response.choices[0].message["content"]
        await send_message(chat_id, poem)

    return {"ok": True}
