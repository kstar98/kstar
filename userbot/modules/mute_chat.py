# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

from userbot import LOGGER, LOGGER_GROUP, HELPER
from userbot.events import register

@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot import MONGO
        except:
            await e.edit('`Running on Non-SQL Mode!`')
        MONGO.mute_chats.delete_one(
                {"chat_id":e.chat_id}
                )
        await e.edit("```Unmuted this chat Successfully```")


@register(outgoing=True, pattern="^.mutechat$")
async def mute_chat(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot import MONGO
        except Exception as er:
            print(er)
            await e.edit("`Running on Non-SQL mode!`")
            return
        await e.edit(str(e.chat_id))
        MONGO.mute_chats.insert_one(
                {"chat_id":e.chat_id}
                )
        await e.edit("`Shush! This chat will be silenced!`")
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                str(e.chat_id) + " was silenced.")


@register(incoming=True)
async def keep_read(e):
    try:
        from userbot import MONGO
    except:
        return
    mute_chat = MONGO.mute_chats.find(
            {"chat_id":e.chat_id}
            )
    if mute_chat:
        for i in mute_chat:
            if i['chat_id'] == str(e.chat_id):
                await e.client.send_read_acknowledge(e.chat_id)
