
import asyncio , subprocess
from userbot.events import register
from telethon import events
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.channels import LeaveChannelRequest, CreateChannelRequest, DeleteMessagesRequest

@register(outgoing=True, pattern="^.timer")
async def timer_blankx(e):
	txt=e.text[7:] + '\nJeepeo , I am Deleting the message in T-minus '
	j=15
	k=j
	for j in range(j):
		await e.edit(txt + str(k))
		k=k-1
		await asyncio.sleep(1)
	await e.delete()

@register(outgoing=True, pattern="^.stimer")
async def stimer_blankx(e):
	await e.edit(e.text[7:])
	await asyncio.sleep(10)
	await e.delete()

@register(outgoing=True, pattern="^.time$")
async def time_blankx(e):
	if e.reply_to_msg_id != None:
		thed='Jeepeo , I am Deleting replied to message in '
		j=10
		k=j
		for j in range(j):
			await e.edit(thed + str(k))
			k=k-1
			await asyncio.sleep(1)
		await bot.delete_messages(e.input_chat, [e.reply_to_msg_id, e.id])

@register(outgoing=True, pattern="^.stime$")
async def stime_blankx(e):
	await e.delete()
	if e.reply_to_msg_id != None:
		await asyncio.sleep(10)
		await bot.delete_messages(e.input_chat, [e.reply_to_msg_id])


@register(outgoing=True, pattern="^.leave$")
async def leave(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if '-' in str(e.chat_id):
            await bot(LeaveChannelRequest(e.chat_id))
        else:
            await e.edit('`This is dead group!`')


@register(outgoing=True, pattern="^.fg (.*)")
async def figlety(e):
	l=['figlet']
	l+=e.pattern_match.group(1).split(' ')
	p='```'
	p+=subprocess.run(l, stdout=subprocess.PIPE).stdout.decode()
	p+='```'
	await e.edit(p)


@register(outgoing=True, pattern="^.cs (.*)")
async def cowsay(e):
        l=['cowsay']
        l+=e.pattern_match.group(1).split(' ')
        p='```'
        p+=subprocess.run(l, stdout=subprocess.PIPE).stdout.decode()
        p+='```'
        await e.edit(p)  


@register(outgoing=True, pattern="^.fs (.*)")
async def figlety(e):
    l=['figlet -f small']
    l+=e.pattern_match.group(1).split(' ')
    p='```'
    p+=subprocess.run(l, stdout=subprocess.PIPE).stdout.decode()
    p+='```'
    await e.edit(p)

