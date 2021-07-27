from datetime import datetime

from telethon.utils import get_display_name

from userbot import iqthon
from userbot.core.logger import logging

from ..core.data import blacklist_chats_list
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper import global_collectionjson as sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

plugin_category = "tools"

LOGS = logging.getLogger(__name__)


@iqthon.iq_cmd(
    pattern="المنع (تشغيل|ايقاف)$",
    command=("المنع", plugin_category),
    info={
        "header": "To enable and disable chats blacklist.",
        "description": "If you turn this on, then your userbot won't work on the chats stored\
         in database by addblkchat cmd. If you turn it off even though you added chats to database\
         userbot won't stop working in that chat.",
        "usage": "{tr}chatblacklist <on/off>",
    },
)
async def chat_blacklist(event):
    "To enable and disable chats blacklist."
    input_str = event.pattern_match.group(1)
    blkchats = blacklist_chats_list()
    if input_str == "تشغيل":
        if gvarstatus("blacklist_chats") is not None:
            return await edit_delete(event, "**⌔︙ تـم تشـغـيلـه بالفعـل ✅ .**")
        addgvar("blacklist_chats", "true")
        text = "**⌔︙ من الآن فصاعدًا ، لا يعمل المنع  في الدردشات المخزنة .✅ .**"
        if len(blkchats) != 0:
            text += (
                "**⌔︙ يقوم البوت بإعادة التحميل لتطبيق التغييرات. من فضلك انتظر دقيقة 👁‍🗨 .**"
            )
            msg = await edit_or_reply(
                event,
                text,
            )
            return await event.client.reload(msg)
        else:
            text += "**⌔︙ لم تقم بإضافة أي دردشة إلى المنع ‼️ .**"
            return await edit_or_reply(
                event,
                text,
            )
    if gvarstatus("blacklist_chats") is not None:
        delgvar("blacklist_chats")
        text = "**⌔︙  إن المنع الخاص بك  يعمل في كل محادثة ⚜️**"
        if len(blkchats) != 0:
            text += (
                "**⌔︙ يقـوم البـوت بإعـادة التحـميـل لتطبيـق التغييـرات. مـن فـضـلك انتـظـر دقـيقـة 👁‍🗨 .**"
            )
            msg = await edit_or_reply(
                event,
                text,
            )
            return await event.client.reload(msg)
        else:
            text += "**⌔︙ لم تقم بإضـافـة أي دردشـة إلـى المـنـع ‼️ .**"
            return await edit_or_reply(
                event,
                text,
            )
    await edit_delete(event, "**⌔︙ تــم ايقـافـه بالـفعـل ✅ .**")


@iqthon.iq_cmd(
    pattern="منع(?:\s|$)([\s\S]*)",
    command=("منع", plugin_category),
    info={
        "header": "To add blacklist words to database",
        "description": "The given word or words will be added to blacklist in that specific chat if any user sends then the message gets deleted.",
        "note": "if you are adding more than one word at time via this, then remember that new word must be given in a new line that is not [hi hello]. It must be as\
            \n[hi \n hello]",
        "usage": "{tr}addblacklist <word(s)>",
        "examples": ["{tr}addblacklist fuck", "{tr}addblacklist fuck\nsex"],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To add blacklist words to database"
    text = event.pattern_match.group(1)
    to_blacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )

    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await edit_or_reply(
        event,
        "⌔︙ تـم اضـافـة {} الكلمـة فـي قائمـة المنـع بنجـاح".format(
            len(to_blacklist)
        ),
    )


@iqthon.iq_cmd(
    pattern="الغاء منع(?:\s|$)([\s\S]*)",
    command=("الغاء منع", plugin_category),
    info={
        "header": "To remove blacklist words from database",
        "description": "The given word or words will be removed from blacklist in that specific chat",
        "note": "if you are removing more than one word at time via this, then remember that new word must be given in a new line that is not [hi hello]. It must be as\
            \n[hi \n hello]",
        "usage": "{tr}rmblacklist <word(s)>",
        "examples": ["{tr}rmblacklist fuck", "{tr}rmblacklist fuck\nsex"],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To Remove Blacklist Words from Database."
    text = event.pattern_match.group(1)
    to_unblacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    successful = sum(
        bool(sql.rm_from_blacklist(event.chat_id, trigger.lower()))
        for trigger in to_unblacklist
    )
    await edit_or_reply(
        event, f"⌔︙ تـم ازالـة الـكلمـة {successful} / {len(to_unblacklist)} مـن قائمـة المنـع بنجـاح"
    )


@iqthon.iq_cmd(
    pattern="قائمة المنع$",
    command=("قائمة المنع", plugin_category),
    info={
        "header": "To show the black list words",
        "description": "Shows you the list of blacklist words in that specific chat",
        "usage": "{tr}listblacklist",
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To show the blacklist words in that specific chat"
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "⌔︙ قائمـة الـمنـع في الدردشـة الـحاليـة :\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👈 {trigger} \n"
    else:
        OUT_STR = " ⌔︙ لـم تـقـم باضـافـة كلمـات سـوداء ارسـل  `.منع` لمـنع كلمـة"
    await edit_or_reply(event, OUT_STR)
