import random
import re
import time
from platform import python_version

from telethon import version, Button
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
    pattern="سورس$",
    command=("سورس", plugin_category),
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
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    CUSTOM_ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**• ⚜️ ~  تـليـثون العـرب ~ ⚜️ •  :**"
    CAT_IMG = gvarstatus("ALIVE_PIC")
    if CAT_IMG:
        CAT = [x for x in CAT_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        cat_caption += f"**• ⚜️ ~  تـليـثون العـرب ~ ⚜️ •  :**\n\n"
        cat_caption += f"**⌔︙ اصـدار النسـخة 📄  :**  ` 1.0.0 `\n"
        cat_caption += f"**⌔︙ مـدة التشـغيـل 🕛 : ** ` {uptime}`\n"
        cat_caption += f"**⌔︙ اسـم الـمنصـب 🚹  :**  `{mention}`\n"
        cat_caption += f"**⌔︙ قنـاة تـليثـون الـرسميـة ⚛️ :** @M4_STORY\n"
        cat_caption += f"**⌔︙ مـطـور الـسورس 🛃 :** @KLANR\n"
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**⌔︙ خطأ في قيمة الوسائط **",
            )
    else:
        await edit_or_reply(
            event,
        cat_caption += f"**• ⚜️ ~  تـليـثون العـرب ~ ⚜️ •  :**\n\n"
        cat_caption += f"**⌔︙ اصـدار النسـخة 📄  :**  ` 1.0.0 `\n"
        cat_caption += f"**⌔︙ مـدة التشـغيـل 🕛 : ** ` {uptime}`\n"
        cat_caption += f"**⌔︙ اسـم الـمنصـب 🚹  :**  `{mention}`\n"
        cat_caption += f"**⌔︙ قنـاة تـليثـون الـرسميـة ⚛️ :** @M4_STORY\n"
        cat_caption += f"**⌔︙ مـطـور الـسورس 🛃 :** @KLANR\n"
        )



@iqthon.iq_cmd(
    pattern="السورس$",
    command=("السورس", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}السورس",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, 'السورس')
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@iqthon.iq_cmd(
    pattern="السورس$",
    command=("السورس", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}السورس",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
        cat_caption += f"**• ⚜️ ~  تـليـثون العـرب ~ ⚜️ •  :**\n\n"
        cat_caption += f"**⌔︙ اصـدار النسـخة 📄  :**  ` 1.0.0 `\n"
        cat_caption += f"**⌔︙ مـدة التشـغيـل 🕛 : ** ` {uptime}`\n"
        cat_caption += f"**⌔︙ اسـم الـمنصـب 🚹  :**  `{mention}`\n"
        cat_caption += f"**⌔︙ قنـاة تـليثـون الـرسميـة ⚛️ :** @M4_STORY\n"
        cat_caption += f"**⌔︙ مـطـور الـسورس 🛃 :** @KLANR\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@iqthon.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
