import os
import re

import pygments
import requests
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.utils import get_extension
from urlextract import URLExtract

from userbot import iqthon

from ..Config import Config
from ..core.events import MessageEdited
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..helpers.utils import pastetext, reply_id

plugin_category = "utils"

extractor = URLExtract()

LOGS = logging.getLogger(__name__)

pastebins = {
    "Pasty": "p",
    "Neko": "n",
    "Spacebin": "s",
    "Dog": "d",
}


def get_key(val):
    for key, value in pastebins.items():
        if val == value:
            return key





@iqthon.iq_cmd(
    pattern="(d|p|s|n)?(paste|كود بالرابط)(?:\s|$)([\S\s]*)",
    command=("paste", plugin_category),
    info={
        "header": "To paste text to a paste bin.",
        "description": "Uploads the given text to website so that you can share text/code with others easily. If no flag is used then it will use p as default",
        "flags": {
            "d": "Will paste text to dog.bin",
            "p": "Will paste text to pasty.lus.pm",
            "s": "Will paste text to spaceb.in (language extension not there at present.)",
        },
        "usage": [
            "{tr}{flags}paste <reply/text>",
            "{tr}{flags}paste {extension} <reply/text>",
        ],
        "examples": [
            "{tr}spaste <reply/text>",
            "{tr}ppaste -py await event.client.send_message(chat,'Hello! testing123 123')",
        ],
    },
)
async def paste_bin(event):
    "To paste text to a paste bin."
    catevent = await edit_or_reply(event, "**⌔︙قم بلصـق النـص للصـق إلى سلـة المحذوفـات ✦**")
    input_str = event.pattern_match.group(3)
    reply = await event.get_reply_message()
    ext = re.findall(r"-\w+", input_str)
    try:
        extension = ext[0].replace("-", "")
        input_str = input_str.replace(ext[0], "").strip()
    except IndexError:
        extension = None
    if event.pattern_match.group(2) == "neko":
        pastetype = "n"
    else:
        pastetype = event.pattern_match.group(1) or "p"
    text_to_print = ""
    if input_str:
        text_to_print = input_str
    if text_to_print == "" and reply.media:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
            if extension is None:
                extension = get_extension(reply.document)
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if text_to_print == "":
        if reply.text:
            text_to_print = reply.raw_text
        else:
            return await edit_delete(
                catevent,
                "**⌔︙إما الـرد على نـص أو على رسالـة أو إعطـاء نـص مع الأمـر ⚠️**",
            )
    if extension and extension.startswith("."):
        extension = extension[1:]
    try:
        response = await pastetext(text_to_print, pastetype, extension)
        if "error" in response:
            return await edit_delete(
                catevent,
                f"**⌔︙حـدث خطـأ أثنـاء لصـق النـص، قد تڪون غيـر قـادر على معالجـة طلبـك لأن عناصـر لصـق النـص معطلـة ⚠️**",
            )
        result = ""
        if pastebins[response["bin"]] != pastetype:
            result += f"<b>{get_key(pastetype)} is down, So </b>"
        result += f"<b>⌔︙ تم اللصـق في ⎙ : <a href={response['url']}>{response['bin']}</a></b>"
        if response["raw"] != "":
            result += f"\n<b>⌔︙رابط الكتابه  🝰: <a href={response['raw']}>اضغط هنا</a></b>"
        await catevent.edit(result, link_preview=False, parse_mode="html")
    except Exception as e:
        await edit_delete(catevent, f"**⌔︙حـدث خطـأ أثنـاء لصـق النـص ⚠️:**\n`{str(e)}`")


@iqthon.iq_cmd(
    command=("كود بالرابط", plugin_category),
    info={
        "header": "To paste text to a neko bin.",
        "description": "Uploads the given text to nekobin so that you can share text/code with others easily.",
        "usage": ["{tr}neko <reply/text>", "{tr}neko {extension} <reply/text>"],
        "examples": [
            "{tr}neko <reply/text>",
            "{tr}neko -py await event.client.send_message(chat,'Hello! testing123 123')",
        ],
    },
)
async def _(event):
    "To paste text to a neko bin."
    # just to show in help menu as seperate



