from userbot import iqthon

from ..core.managers import edit_or_reply
from ..helpers import fonts as emojify

plugin_category = "fun"


@iqthon.iq_cmd(
    pattern="رسم قلوب(?:\s|$)([\s\S]*)",
    command=("رسم قلوب", plugin_category),
    info={
        "header": "Converts your text to big emoji text, with some default emojis.",
        "usage": "{tr}emoji <text>",
        "examples": ["{tr}emoji catuserbot"],
    },
)
async def itachi(event):
    "To get emoji art text."
    args = event.pattern_match.group(1)
    get = await event.get_reply_message()
    if not args and get:
        args = get.text
    if not args:
        await edit_or_reply(
            event, "**⌔︙ قم بكتابه الكلمه بجانب الامر **"
        )
        return
    result = ""
    for a in args:
        a = a.lower()
        if a in emojify.kakashitext:
            char = emojify.kakashiemoji[emojify.kakashitext.index(a)]
            result += char
        else:
            result += a
    await edit_or_reply(event, result)


@iqthon.iq_cmd(
    pattern="رسم شعار(?:\s|$)([\s\S]*)",
    command=("cmoji", plugin_category),
    info={
        "header": "Converts your text to big emoji text, with your custom emoji.",
        "usage": "{tr}cmoji <emoji> <text>",
        "examples": ["{tr}cmoji 8 telethon"],
    },
)
async def itachi(event):
    "To get custom emoji art text."
    args = event.pattern_match.group(1)
    get = await event.get_reply_message()
    if not args and get:
        args = get.text
    if not args:
        return await edit_or_reply(
            event, "**⌔︙ قم بكتابه الكلمه بجانب الامر **"
        )
    try:
        emoji, arg = args.split(" ", 1)
    except Exception:
        arg = args
        emoji = "8"
    result = ""
    for a in arg:
        a = a.lower()
        if a in emojify.kakashitext:
            char = emojify.itachiemoji[emojify.kakashitext.index(a)].format(cj=emoji)
            result += char
        else:
            result += a
    await edit_or_reply(event, result)
