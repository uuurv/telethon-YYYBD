from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.types import ChannelParticipantAdmin as admin
from telethon.tl.types import ChannelParticipantCreator as owner
from telethon.tl.types import UserStatusOffline as off
from telethon.tl.types import UserStatusOnline as onn
from telethon.tl.types import UserStatusRecently as rec
from telethon.utils import get_display_name
from userbot import iqthon

from ..helpers.utils import get_user_from_event, reply_id

plugin_category = "extra"

@iqthon.on(admin_cmd(pattern="تاك (تشغيل|ايقاف|للكل|للبوتات|للنشط|للادمنيه|للمالك)?(.*)"
                   ))
async def iq(e):
    okk = e.text
    lll = e.pattern_match.group(2)
    users = 0
    o = 0
    nn = 0
    rece = 0
    if lll:
        xx = f"{lll}"
    else:
        xx = ""
    async for bb in e.client.iter_participants(e.chat_id, 500):
        users = users + 1
        x = bb.status
        y = bb.participant
        if isinstance(x, onn):
            o = o + 1
            if "تشغيل" in okk:
                xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if isinstance(x, off):
            nn = nn + 1
            if "ايقاف" in okk:
                if not (bb.bot or bb.deleted):
                    xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if isinstance(x, rec):
            rece = rece + 1
            if "للنشط" in okk:
                if not (bb.bot or bb.deleted):
                    xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if isinstance(y, owner):
            if "للادمنيه" or "للمالك" in okk:
                xx += f"\n👑 [{get_display_name(bb)}](tg://user?id={bb.id}) 👑"
        if isinstance(y, admin):
            if "للادمنيه" in okk:
                if not bb.deleted:
                    xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if "للكل" in okk:
            if not (bb.bot or bb.deleted):
                xx += f"\n⚜️ [{get_display_name(bb)}](tg://user?id={bb.id})"
        if "للبوتات" in okk:
            if bb.bot:
                xx += f"\n🤖 [{get_display_name(bb)}](tg://user?id={bb.id})"
    await e.client.send_message(e.chat_id, xx)
    await e.delete()



@iqthon.iq_cmd(
    pattern="ابلاغ الادمنيه$",
    command=("ابلاغ الادمنيه", plugin_category),
    info={
        "header": "To tags admins in group.",
        "usage": "{tr}report",
    },
)
async def _(event):
    "To tags admins in group."
    mentions = "@تاك للادمنيه : **⌔︙تم رصـد إزعـاج ⚠️**"
    chat = await event.get_input_chat()
    reply_to_id = await reply_id(event)
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        if not x.bot:
            mentions += f"[\u2063](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()


@iqthon.iq_cmd(
    pattern="تاك بالكلام ([\s\S]*)",
    command=("تاك بالكلام", plugin_category),
    info={
        "header": "Tags that person with the given custom text.",
        "usage": [
            "{tr}men username/userid text",
            "text (username/mention)[custom text] text",
        ],
        "examples": ["{tr}men @mrconfused hi", "Hi @mrconfused[How are you?]"],
    },
)
async def _(event):
    "Tags that person with the given custom text."
    user, input_str = await get_user_from_event(event)
    if not user:
        return
    reply_to_id = await reply_id(event)
    await event.delete()
    await event.client.send_message(
        event.chat_id,
        f"<a href='tg://user?id={user.id}'>{input_str}</a>",
        parse_mode="HTML",
        reply_to=reply_to_id,
    )
