# Default modules:
import os
import asyncio
import openai

# External modules:
from flask import Flask, request
from telethon import TelegramClient, events
from telethon.sessions import StringSession

app = Flask(__name__)
client = TelegramClient(
        StringSession(os.environ['SESSION_STRING']),
        api_id=int(os.environ["API_ID"]),
        api_hash=os.environ["API_HASH"])
openai.api_key = os.environ["OPENAI_TOKEN"]

@app.before_request
def main_handler():
    if request.form.get(os.environ["MAIN_PASS"]):
        asyncio.run(main_def())

async def main_def():
    await client.connect()

    @client.on(event=events.NewMessage(chats=[-1001801400562], outgoing=True))
    async def explain_word(event):
        if event.reply_to.reply_to_msg_id == 31:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": 'You are very experienced English teacher. Don`t say "Sure", '
                                                  'just give a response'},
                    {"role": "user", "content": f"Please, give me the definition and show 5 middle-level "
                                                f"use examples of the word (phrase) {event.message.message}"}
                ],
                max_tokens=2048,
                temperature=0.5,
            )
            await client.send_message(entity=-1001801400562, message=response['choices'][0]['message']['content'],
                                      reply_to=event.message.id)

    @client.on(event=events.NewMessage(chats=['me'], outgoing=True))
    async def check_stability(event):
        await client.send_message(entity='me', message="I`m here",
                                  reply_to=event.message.id)

    await client.run_until_disconnected()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT", 3000))





