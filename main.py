import os
from fastapi import FastAPI, Request
import httpx
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT = OpenAI()

app = FastAPI()
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={"chat_id": chat_id, "text": text})

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    if "message" in body:
        chat_id = body["message"]["chat"]["id"]
        user_text = body["message"]["text"]

        completion = CLIENT.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a poet that writes deep, romantic, mystical poems."},
                {"role": "user", "content": f"Write a poem about {user_text}."}
            ]
        )
        poem = completion.choices[0].message["content"]

        await send_message(chat_id, poem)

    return {"ok": True}
