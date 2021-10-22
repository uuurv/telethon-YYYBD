from telethon import events
from userbot import iqthon
from ..sql_helper.autopost_sql import add_post, get_all_post, is_post, remove_post
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from . import *


@iqthon.on(admin_cmd(pattern="autopost ?(.*)"))
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "AutoPost Can Only Be Used For Channels.")
    hel_ = event.pattern_match.group(1)
    if str(hel_).startswith("-100"):
        iq = str(hel_).replace("-100", "")
    else:
        iq = hel_
    if not iq.isdigit():
        return await edit_or_reply(event, "**Please Give Channel ID !!**")
    if is_post(iq , event.chat_id):
        return await edit_or_reply(event, "This Channel Is Already In AutoPost Database.")
    add_post(iq, event.chat_id)
    await edit_or_reply(event, f"**📍 Started AutoPosting from** `{hel_}`")


@iqthon.on(admin_cmd(pattern="rmautopost ?(.*)"))
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "AutoPost Can Only Be Used For Channels.")
    hel_ = event.pattern_match.group(1)
    if str(hel_).startswith("-100"):
        iq = str(hel_).replace("-100", "")
    else:
        iq = hel_
    if not iq.isdigit():
        return await edit_or_reply(event, "**Please Give Channel ID !!**")
    if not is_post(iq, event.chat_id):
        return await edit_or_reply(event, "I don't think this channel is in AutoPost Database.")
    remove_post(iq, event.chat_id)
    await edit_or_reply(event, f"**📍 Stopped AutoPosting From** `{hel_}`")

@iqthon.iq_cmd(incoming=True)
async def _(event):
    if event.is_private:
        return
    chat_id = str(event.chat_id).replace("-100", "")
    channels_set  = get_all_post(chat_id)
    if channels_set == []:
        return
    for chat in channels_set:
        if event.media:
            await event.client.send_file(int(chat), event.media, caption=event.text)
        elif not event.media:
            await bot.send_message(int(chat), event.message)
