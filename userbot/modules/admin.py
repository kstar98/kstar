
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.

from time import sleep

from telethon.errors import (BadRequestError, ImageProcessFailedError,
                             PhotoCropSizeSmallError)
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.types import (ChatAdminRights, ChatBannedRights,
                               MessageMediaDocument, MessageMediaPhoto)

from telethon.tl.types import ChatAdminRights, ChatBannedRights
from telethon.tl.functions.users import GetFullUserRequest

from userbot import (BRAIN_CHECKER, LOGGER, LOGGER_GROUP, HELPER, bot)
from userbot.events import register

#=================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing image`"
NO_ADMIN = "`You aren't an admin!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = "`Some issue with updating the pic,`" \
                "`maybe you aren't an admin,`" \
                "`or don't have the desired rights.`"
INVALID_MEDIA = "`Invalid Extension`"
#================================================


@register(outgoing=True, pattern="^.setgrouppic$")
async def set_group_photo(gpic):
    if not gpic.text[0].isalpha() and gpic.text[0] not in ("/", "#", "@", "!"):
        replymsg = await gpic.get_reply_message()
        chat = await gpic.get_chat()
        photo = None

        if not chat.admin_rights or chat.creator:
            await gpic.edit(NO_ADMIN)
            return

        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await bot.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split('/'):
                photo = await bot.download_file(replymsg.media.document)
            else:
                await gpic.edit(INVALID_MEDIA)

        if photo:
            try:
                await EditPhotoRequest(
                    gpic.chat_id,
                    await bot.upload_file(photo)
                    )
                await gpic.edit(CHAT_PP_CHANGED)

            except PhotoCropSizeSmallError:
                await gpic.edit(PP_TOO_SMOL)
            except ImageProcessFailedError:
                await gpic.edit(PP_ERROR)


@register(outgoing=True, pattern="^.promote$")
async def promote(promt):
    """ For .promote command, do promote targeted person """
    if not promt.text[0].isalpha() \
            and promt.text[0] not in ("/", "#", "@", "!"):
        new_rights = ChatAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True
        )

        # Self explanatory
        if not await promt.get_reply_message():
            await promt.edit("`Jeepeo Gib a reply message`")
        elif not admin and creator:
            rights = new_rights

        # Try to promote if current user is admin or creator
        try:
            await promt.client(
                EditAdminRequest(promt.chat_id,
                                 (await promt.get_reply_message()).sender_id,
                                 new_rights)
            )
            await promt.edit("`Promoted Successfully!`")

        # If Telethon spit BadRequestError, assume
        # we don't have Promote permission
        except BadRequestError:
            await promt.edit(
                "`Ooof ! Jeepeo😎 ,You are not admin in this **CANCEROUS** group `"
                )
            return


@register(outgoing=True, pattern="^.demote$")
async def demote(dmod):
    """ For .demote command, do demote targeted person """
    if not dmod.text[0].isalpha() and dmod.text[0] not in ("/", "#", "@", "!"):
        # Get targeted chat
        chat = await dmod.get_chat()
        # Grab admin status or creator in a chat
        admin = chat.admin_rights
        creator = chat.creator

        # If there's no reply, return
        if not await dmod.get_reply_message():
            await dmod.edit("`Give a reply message`")
            return
        # If not admin and not creator, also return
        if not admin and not creator:
            await dmod.edit("`Ooof ! Jeepeo😎 ,You are not admin in this **CANCEROUS** group `")
            return

        # If passing, declare that we're going to demote
        await dmod.edit("`The Bitch is being Demoted...`")

        # New rights after demotion
        newrights = ChatAdminRights(
            add_admins=None,
            invite_users=None,
            change_info=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None
        )
        # Edit Admin Permission
        try:
            await dmod.client(
                EditAdminRequest(dmod.chat_id,
                                 (await dmod.get_reply_message()).sender_id,
                                 newrights)
            )

        # If we catch BadRequestError from Telethon
        # Assume we don't have permission to demote
        except BadRequestError:
            await dmod.edit(
                "`Ooof ! You dont Have permission to demote!`"
                )
            return
        await dmod.edit("`Demoted The bitch Successfully!`")


@register(outgoing=True, pattern="^.ban$")
async def thanos(bon):
    """ For .ban command, do "thanos" at targeted person """
    if not bon.text[0].isalpha() and bon.text[0] not in ("/", "#", "@", "!"):
        banned_rights = ChatBannedRights(
            until_date=None,
            view_messages=True,
            send_messages=True,
            send_media=True,
            send_stickers=True,
            send_gifs=True,
            send_games=True,
            send_inline=True,
            embed_links=True,
        )

        # Here laying the sanity check
        chat = await bon.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # For dealing with reply-at-ban
        sender = await bon.get_reply_message()

        # Well
        if not admin and not creator:
            await bon.edit("`Ooof ! Jeepeo😎 ,You are not admin in this **CANCEROUS** group `")
            return

        # If the user is a sudo
        try:
            if sender.sender_id in BRAIN_CHECKER:
                await bon.edit(
                    "`Ban Error! I am not supposed to ban this user`"
                    )
                return

        # This exception handled if the user doesn't
        # Specifying any target (reply in this case)
        except AttributeError:
            return

        # Announce that we're going to whacking the pest
        await bon.edit("`Whacking the pest!`")
        try:
            await bon.client(
            EditBannedRequest(
                bon.chat_id,
                sender.sender_id,
                banned_rights
            )
        )
        except Exception as e:
            await bon.edit("`I couldn't ban this user! Possible reasons: \
                             Maybe the admin status was appointed by someone else.`")
            return
        # Helps ban group join spammers more easily
        try:
            await sender.delete() 
        except Exception as e:
            await bon.edit("`I dont have message nuking rights! But still he was banned!`")
            return
        # Delete message and then tell that the command
        # is done gracefully
        # Shout out the ID, so that fedadmins can fban later

        await bon.edit("`{}` was banned!".format(str(sender.sender_id)))

        # Announce to the logging group if we done a banning
        if LOGGER:
            await bon.client.send_message(
                LOGGER_GROUP,
                "#BAN\n"
                "ID: `"+ str((await bon.get_reply_message()).sender_id)
                + "`",
            )


@register(outgoing=True, pattern="^.unban$")
async def nothanos(unbon):
    if not unbon.text[0].isalpha() and unbon.text[0] \
            not in ("/", "#", "@", "!"):
        rights = ChatBannedRights(
            until_date=None,
            send_messages=None,
            send_media=None,
            send_stickers=None,
            send_gifs=None,
            send_games=None,
            send_inline=None,
            embed_links=None,
            )
        replymsg = await unbon.get_reply_message()
        try:
            await unbon.client(EditBannedRequest(
                unbon.chat_id,
                replymsg.sender_id,
                rights
                ))
            await unbon.edit("```Unbanned the bitch Successfully```")

            if LOGGER:
                await unbon.client.send_message(
                    LOGGER_GROUP,
                    "#UNBAN\n"
                    +"ID: `"+ str((await unbon.get_reply_message()).sender_id)
                    + "`",
                )
        except UserIdInvalidError:
            await unbon.edit("`Cant use Magic Wand Jeepeo😎`")


@register(outgoing=True, pattern="^.mute$")
async def spider(spdr):
    """
    This function basically muting peeps
    """
    if not spdr.text[0].isalpha() and spdr.text[0] not in ("/", "#", "@", "!"):

        # If the targeted user is a Sudo
        if (await spdr.get_reply_message()).sender_id in BRAIN_CHECKER:
            await spdr.edit(
                "`Mute Error! I am not supposed to mute this user`"
                )
            return

        # Check if the function running under SQL mode
        try:
            from userbot import MONGO
        except Exception:
            await spdr.edit("`Running on Non-SQL mode!`")
            return

        # Get the targeted chat
        chat = await spdr.get_chat()
        # Check if current user is admin
        admin = chat.admin_rights
        # Check if current user is creator
        creator = chat.creator

        # If not admin and not creator, return
        if not admin and not creator:
            await spdr.edit("`Ooof ! Jeepeo😎 ,You are not admin in this **CANCEROUS** group `")
            return

        target = await spdr.get_reply_message()
        # Else, do announce and do the mute
        MONGO.mutes.insert_one(
            {"chat_id":spdr.chat_id, "sender":target.sender_id}
            )
        await spdr.edit("`Here is your glue`")

        # Announce that the function is done
        await spdr.edit("`You have been sucessfully used the glue`")

        # Announce to logging group
        if LOGGER:
            await spdr.send_message(
                LOGGER_GROUP,
                "#MUTE\n"
                +"ID: `"+ str(target.sender_id)
                + "`",
            )


@register(outgoing=True, pattern="^.unmute$")
async def unmoot(unmot):
    if not unmot.text[0].isalpha() and unmot.text[0] \
            not in ("/", "#", "@", "!"):
        rights = ChatBannedRights(
            until_date=None,
            send_messages=None,
            send_media=None,
            send_stickers=None,
            send_gifs=None,
            send_games=None,
            send_inline=None,
            embed_links=None,
            )
        try:
            from userbot import MONGO
        except Exception:
            await unmot.edit("`Running on non-SQL mode`")
        replymsg = await unmot.get_reply_message()
        MONGO.mutes.delete_one(
            {"chat_id":unmot.chat_id, "sender":replymsg.sender_id}
            )
        try:
            await unmot.client(EditBannedRequest(
                unmot.chat_id,
                replymsg.sender_id,
                rights
                ))
            MONGO.mutes.delete_one(
                {"sender":replymsg.sender_id}
                )
            await unmot.edit("```Unmuted Successfully```")
        except UserIdInvalidError:
            await unmot.edit("`Uh oh my unmute logic broke!`")
        if LOGGER:
            await unmot.send_message(
                LOGGER_GROUP,
                "#MUTE\n"
                +"ID: `"+ str((await unmot.get_reply_message()).sender_id)
                + "`",
            )       

@register(incoming=True)
async def muter(moot):
    try:
        from userbot import MONGO
    except:
        return
    muted = MONGO.mutes.find_one(
            {"chat_id":moot.chat_id, "sender":moot.sender_id}
            )
    gmuted = MONGO.gmutes.find_one(
            {"sender":moot.sender_id}
            )
    rights = ChatBannedRights(
                until_date=None,
                send_messages=True,
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_games=True,
                send_inline=True,
                embed_links=True,
                )
    if muted:
                await moot.delete()
                await moot.client(EditBannedRequest(
                    moot.chat_id,
                    moot.sender_id,
                    rights
                    ))
    if gmuted:
                await moot.delete()


@register(outgoing=True, pattern="^.ungmute$")
async def ungmoot(ungmoot):
    if not ungmoot.text[0].isalpha() and ungmoot.text[0] \
            not in ("/", "#", "@", "!"):
        reply = await ungmoot.get_reply_message()
        replied_user = await ungmoot.client(GetFullUserRequest(reply.from_id))
        aname = replied_user.user.id
        try:
            from userbot import MONGO
        except:
            await ungmoot.edit('`Running on Non-SQL Mode!`')
        MONGO.gmutes.delete_one(
            {"sender":replied_user.user.id}
            )
        await ungmoot.edit("```Ungmuted Successfully```")


@register(outgoing=True, pattern="^.gmute$")
async def gspider(gspdr):
    if not gspdr.text[0].isalpha() and gspdr.text[0] not in ("/", "#", "@", "!"):
        if (await gspdr.get_reply_message()).sender_id in BRAIN_CHECKER:
            await gspdr.edit("`Mute Error! Couldn't mute this user`")
            return
        reply = await gspdr.get_reply_message()
        replied_user = await gspdr.client(GetFullUserRequest(reply.from_id))
        aname = replied_user.user.id
        try:
            from userbot import MONGO
        except Exception as err:
            print(err)
            await gspdr.edit("`Running on Non-SQL mode!`")
            return

        MONGO.gmutes.insert_one(
            {"sender":replied_user.user.id}
            )
        await gspdr.edit("`Ooof ! Here's your strong tape , apply it in ur mouth`")
        sleep(5)
        await gspdr.delete()
        await gspdr.respond("`Taped!`")

        if LOGGER:
            await gspdr.send_message(
                LOGGER_GROUP,
                str((await gspdr.get_reply_message()).sender_id)
                + " was muted.",
            )

HELPER.update({
    "promote": "Usage: \nReply someone's message with .promote to promote them."
})
HELPER.update({
    "ban": "Usage: \nReply someone's message with .ban to ban them."
})
HELPER.update({
    "demote": "Usage: \nReply someone's message with .demote to revoke their admin permissions."
})
HELPER.update({
    "unban": "Usage: \nReply someone's message with .unban to unban them in this chat."
})
HELPER.update({
    "mute": "Usage: \nReply someone's message with .mute to mute them, works on admins too"
})
HELPER.update({
    "unmute": "Usage: \nReply someone's message with .unmute to remove them from muted list."
})
HELPER.update({
    "gmute": "Usage: \nReply someone's message with .gmute to mute them in all groups you have in common with them."
})
HELPER.update({
    "ungmute": "Usage: \nReply someone's message with .ungmute to remove them from the gmuted list."
})
