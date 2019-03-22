from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from userbot import API_KEY, API_HASH

with TelegramClient(StringSession(), API_KEY, API_HASH) as client:
    print(client.session.save())