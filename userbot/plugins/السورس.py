import random
import re
import time
from platform import python_version

from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from userbot import StartTime, iqthon, catversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "utils"


@iqthon.iq_cmd(
    pattern="السورس$",
    command=("السورس", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI_TELETHON = gvarstatus("ALIVE_EMOJI") or " ٍَ 🖤"
    IQTHON_ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "❬ تـليثون العـرب - Telethon-Arabe ، 🕸  ❭"
    IQTHON_IMG = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/cd27beb82e7af1aff97d2.mp4"
    if IQTHON_IMG:
        CAT = [x for x in IQTHON_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        cat_caption = f"**{IQTHON_ALIVE_TEXT}**\n"
        cat_caption += f"**———×**\n"
        cat_caption += f"**{EMOJI_TELETHON} ❬ ٍَ أصدار النسخـة :  ِ5.0.0  ٍَ❭**\n"
        cat_caption += f"**{EMOJI_TELETHON}❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**\n"
        cat_caption += f"**{EMOJI_TELETHON} ❬ ِحسـابك  :   {mention}  ٍ**\n"
        cat_caption += f"**{EMOJI_TELETHON} ❬ ٰقنـاة تليـثون  :** @M4_STORY  ٍَ❭\n"
        cat_caption += f"**{EMOJI_TELETHON}** ❬ ٰمـطور السورس : ** @LLL5L ٍَ❭\n"
        cat_caption += f"**———×**\n"
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            event,
            f"**{IQTHON_ALIVE_TEXT}**\n\n"
            f"**———×**\n"
            f"**{EMOJI_TELETHON} ❬ ٍَ أصدار النسخـة :  ِ5.0.0  ٍَ❭**\n"
            f"**{EMOJI_TELETHON}❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**\n"
            f"**{EMOJI_TELETHON} ❬ ِحسـابك  :   {mention}  ٍَ❭**\n"
            f"**{EMOJI_TELETHON} ❬ ٰقنـاة تليـثون  :** @M4_STORY  ٍَ❭\n"
            f"**{EMOJI_TELETHON}** ❬ ٰمـطور السورس : ** @LLL5L ٍَ❭\n"
            f"**———×**\n"
        )


@iqthon.iq_cmd(
    pattern="ialive$",
    command=("سورس", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    cat_caption = f"**Catuserbot is Up and Running**\n"
    cat_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    cat_caption += f"**{EMOJI} Catuserbot Version :** `{catversion}`\n"
    cat_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    cat_caption += f"**{EMOJI} Master:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@iqthon.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
