import string

from telethon.tl.types import Channel, MessageMediaWebPage

from userbot import iqthon
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_or_reply

plugin_category = "extra"

LOGS = logging.getLogger(__name__)


class FPOST:
    def __init__(self) -> None:
        self.GROUPSID = []
        self.MSG_CACHE = {}


FPOST_ = FPOST()


async def all_groups_id(cat):
    catgroups = []
    async for dialog in cat.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.megagroup:
            catgroups.append(entity.id)
    return catgroups


@iqthon.iq_cmd(
    pattern="اعاده ارسال$",
    command=("اعاده ارسال", plugin_category),
    info={
        "header": "To get view counter for the message. that is will delete old message and send new message where you can see how any people saw your message",
        "usage": "{tr}اعاده ارسال",
    },
)
async def _(event):
    "To get view counter for the message"
    if Config.PRIVATE_CHANNEL_BOT_API_ID == 0:
        return await edit_or_reply(
            event,
            "**⌔︙ يرجـىٰ تعييـن الڤـار المطلـوب** `PRIVATE_CHANNEL_BOT_API_ID` لڪي يعمـل هـذا الأمـر ⚠️",
        )
    try:
        e = await event.client.get_entity(Config.PRIVATE_CHANNEL_BOT_API_ID)
    except Exception as e:
        await edit_or_reply(event, str(e))
    else:
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await event.client.forward_messages(e, re_message, silent=True)
        await event.client.forward_messages(event.chat_id, fwd_message)
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@iqthon.iq_cmd(
    pattern="ازاله التوجيه$",
    command=("ازاله التوجيه", plugin_category),
    info={
        "header": "To resend the message again. Useful to remove forword tag",
        "usage": "{tr}ازاله التوجيه",
    },
)
async def _(event):
    "To resend the message again"
    try:
        await event.delete()
    except Exception as e:
        LOGS.info(str(e))
    m = await event.get_reply_message()
    if not m:
        return
    if m.media and not isinstance(m.media, MessageMediaWebPage):
        return await event.client.send_file(event.chat_id, m.media, caption=m.text)
    await event.client.send_message(event.chat_id, m.text)


