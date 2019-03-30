#A module made by sunda001
from telethon import events
from userbot import bot 
from userbot.events import register
import asyncio
import requests


@register(outgoing=True, pattern="^.kod (.*)")
async def _(event):
    if event.fwd_from:
        return
    textx = await event.get_reply_message()
    code = event.text
    if code[8:]:
            code = str(code[8:])
    elif textx:
            code = str(textx.message)
    lang = 'python'
    url = "http://apikuu.herokuapp.com/api/v0/sakty/karbon"
    a = requests.get(url, params={
        "code": code,
        "lang": lang,
        "line": True
    }).json()
    img_url = a["hasil"]["karbon"]
    try:
        await bot.send_file(
            event.chat_id,
            img_url,
            force_document=False,
            allow_cache=False,
        )
        await event.delete()
    except Exception as e:
        await event.edit(str(e))

