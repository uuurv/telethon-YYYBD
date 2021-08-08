import os
from datetime import datetime

import aiohttp
import requests
from github import Github
from pySmartDL import SmartDL

from userbot import iqthon

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import reply_id

LOGS = logging.getLogger(os.path.basename(__name__))
ppath = os.path.join(os.getcwd(), "temp", "githubuser.jpg")
plugin_category = "misc"

GIT_TEMP_DIR = "./temp/"


@iqthon.iq_cmd(
    pattern="رابط تنصيب$",
    command=("رابط تنصيب", plugin_category),
    info={
        "header": "رابط تنصيب",
        "usage": [
            "{tr}رابط تنصيب",
        ],
    },
)
async def source(e):
    "رابط تنصيب"
    await edit_or_reply(
        e,
        "رابط تنصيب تليثون العرب [هنا رابط](https://heroku.com/deploy?template=https://github.com/klanrali/Telethon-Arab-helper)",
    )


@iqthon.iq_cmd(
    pattern="حساب كيثاب( -l(\d+))? ([\s\S]*)",
    command=("حساب كيثاب", plugin_category),
    info={
        "header": "Shows the information about an user on GitHub of given username",
        "flags": {"-l": "repo limit : default to 5"},
        "usage": ".github [flag] [username]",
        "examples": [".github sandy1709", ".github -l5 sandy1709"],
    },
)
async def _(event):
    "Get info about an GitHub User"
    reply_to = await reply_id(event)
    username = event.pattern_match.group(3)
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await edit_delete(event, "`" + username + " not found`")
            catevent = await edit_or_reply(event, "**⌔︙جـاري إحضـار معلومـات حساب كيثاب ↯**")
            result = await request.json()
            photo = result["avatar_url"]
            if result["bio"]:
                result["bio"] = result["bio"].strip()
            repos = []
            sec_res = requests.get(result["repos_url"])
            if sec_res.status_code == 200:
                limit = event.pattern_match.group(2)
                limit = 5 if not limit else int(limit)
                for repo in sec_res.json():
                    repos.append(f"[{repo['name']}]({repo['html_url']})")
                    limit -= 1
                    if limit == 0:
                        break
            REPLY = "**⌔︙معلومـات الكيثاب لـ :** `{username}`\
                \n**⌔︙الإسـم 👤:** [{name}]({html_url})\
                \n**⌔︙النـوع 🔧:** `{type}`\
                \n**⌔︙الشرڪـة 🏢:** `{company}`\
                \n**⌔︙المدونـة 🔭:**  {blog}\
                \n**⌔︙الموقـع 📍:**  `{location}`\
                \n**⌔︙النبـذة 📝:**  `{bio}`\
                \n**⌔︙عـدد المتابعيـن ❤️:**  `{followers}`\
                \n**⌔︙الذيـن يتابعهـم 👁:**  `{following}`\
                \n**⌔︙ عدد ريبو العام 📊:**  `{public_repos}`\
                \n**⌔︙الجمهـور 📄:**  `{public_gists}`\
                \n**⌔︙تم إنشـاء الملـف الشخصـي ✓** 🔗: `{created_at}`\
                \n**⌔︙تم تحديـث الملـف الشخصـي ✓** ✏️: `{updated_at}`".format(
                username=username, **result
            )

            if repos:
                REPLY += "\n**⌔︙بعـض الريبوات 🔍 :** : " + " | ".join(repos)
            downloader = SmartDL(photo, ppath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
            await event.client.send_file(
                event.chat_id,
                ppath,
                caption=REPLY,
                reply_to=reply_to,
            )
            os.remove(ppath)
            await catevent.delete()



