
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import inspect
import subprocess
import time
from getpass import getuser

import hastebin
from telethon import TelegramClient, events
from userbot import bot
from telethon.events import StopPropagation

from userbot import *
from userbot.events import register
from userbot import bot


@register(outgoing=True, pattern="^.eval")
async def evaluate(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.is_channel and not e.is_group:
            await e.edit("`Eval isn't permitted on channels`")
            return
        evaluation = eval(e.text[6:])
        if evaluation:
            if isinstance(evaluation) == "str":
                if len(evaluation) > 4096:
                    f = open("output.txt", "w+")
                    f.write(evaluation)
                    f.close()
                await e.client.send_file(
                    e.chat_id,
                    "output.txt",
                    reply_to=e.id,
                    caption="`Output too large, sending as file`",
                )
                subprocess.run(["rm", "sender.txt"], stdout=subprocess.PIPE)
        await e.edit(
            "**Query: **\n`"
            + e.text[6:]
            + "`\n**Result: **\n`"
            + str(evaluation)
            + "`"
        )
    else:
        await e.edit(
            "**Query: **\n`"
            + e.text[6:]
            + "`\n**Result: **\n`No Result Returned/False`"
        )
    if LOGGER:
        await e.client.send_message(
            LOGGER_GROUP, "Eval query " +
            e.text[6:] + " was executed successfully"
        )


@register(outgoing=True, pattern=r"^.exec (.*)")
async def run(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.is_channel and not e.is_group:
            await e.edit("`Exec isn't permitted on channels`")
            return
        code = e.raw_text[5:]
        exec(f"async def __ex(e): " + "".join(f"\n {l}" for l in code.split("\n")))
        result = await locals()["__ex"](e)
        if result:
            if len(result) > 4096:
                f = open("output.txt", "w+")
                f.write(result)
                f.close()
                await e.client.send_file(
                    e.chat_id,
                    "output.txt",
                    reply_to=e.id,
                    caption="`Output too large, sending as file`",
                )
                subprocess.run(["rm", "output.txt"], stdout=subprocess.PIPE)
            await e.edit(
                "**Query: **\n`" + e.text[5:] + "`\n**Result: **\n`" + str(result) + "`"
            )
        else:
            await e.edit(
                "**Query: **\n`"
                + e.text[5:]
                + "`\n**Result: **\n`"
                + "No Result Returned/False"
                + "`"
            )
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                "Exec query " + e.text[5:] + " was executed successfully"
            )


@register(outgoing=True, pattern="^.term")
async def terminal_runner(event):
    split_text = event.text.split(None, 1)

    if len(split_text) == 1:
        await event.edit(terminal.__doc__)
        return

    cmd = split_text[1]


    start_time = time.time() + 10
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Query:**\n\n`{cmd}`\n\n**Result:**\n\n"

    if not SUBPROCESS_ANIM:
        stdout, stderr = await process.communicate()

        if len(stdout) > 4096:
            await event.reply(f"{OUTPUT}\n__Process killed:__ `Messasge too long`")
            return

        if stderr.decode():
            await event.edit(f"{OUTPUT}`{stderr.decode()}`")
            return

        await event.edit(f"{OUTPUT}`{stdout.decode()}`")
        return

    while process:
        if time.time() > start_time:
            if process:
                process.kill()
            await event.edit(event, f"{OUTPUT}\n__Process killed__: `Time limit reached`")
            break

        stdout = await process.stdout.readline()

        if not stdout:
            _, stderr = await process.communicate()
            if stderr.decode():
                OUTPUT += f"`{stderr.decode()}`"
                try:
                    await event.edit(OUTPUT)
                except Exception:
                    break
                break

        if stdout:
            OUTPUT += f"`{stdout.decode()}`"

        if len(OUTPUT) > 4096:
            if process:
                process.kill()
            await event.reply(f"{OUTPUT}\n__Process killed:__ `Messasge too long`")
            break
        try:
            await event.edit(OUTPUT)
        except FloodWaitError:
            stdout, stderr = await process.communicate()
            if stderr:
                await event.edit(f"{OUTPUT}`{stderr}`")
                break

            await event.edit(f"{OUTPUT}`{stdout}`")
            break


HELPER.update({
    "eval": "Evalute mini-expressions. Usage: \n .eval 2 + 3 "
})
HELPER.update({
    "exec": "Execute small python scripts. Usage: \n .exec print('hello')"
})
HELPER.update({
    "term": "Run bash commands and scripts on your server. Usage: \n .term ls"
})
