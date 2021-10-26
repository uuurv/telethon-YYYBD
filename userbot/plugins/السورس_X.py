import os
import aiohttp
import requests
import random
import re
import time
import sys
import asyncio
import math
import heroku3
import urllib3
import speedtest
from asyncio.exceptions import CancelledError
from time import sleep
from platform import python_version
from github import Github
from pySmartDL import SmartDL
from pathlib import Path
from telethon.tl.types import InputMessagesFilterDocument
from datetime import datetime
from telethon import version
from telethon.events import CallbackQuery
from telethon.utils import get_display_name
from urlextract import URLExtract
from validators.url import url
from userbot import StartTime, iqthon, catversion
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id, _catutils, parse_pre, yaml_format, install_pip, get_user_from_event, _format
from ..utils import load_module
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.global_collection import add_to_collectionlist, del_keyword_collectionlist, get_collectionlist_items
from . import mention, reply_id, BOTLOG, BOTLOG_CHATID, HEROKU_APP
LOGS = logging.getLogger(os.path.basename(__name__))
LOGS1 = logging.getLogger(__name__)
ppath = os.path.join(os.getcwd(), "temp", "githubuser.jpg")
GIT_TEMP_DIR = "./temp/"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
cmdhd = Config.COMMAND_HAND_LER
extractor = URLExtract()
vlist = [
    "ALIVE_PIC",
    "ALIVE_EMOJI",
    "ALIVE_TEXT",
    "ALLOW_NSFW",
    "HELP_EMOJI",
    "HELP_TEXT",
    "IALIVE_PIC",
    "PM_PIC",
    "PM_TEXT",
    "PM_BLOCK",
    "MAX_FLOOD_IN_PMS",
    "START_TEXT",
    "NO_OF_ROWS_IN_HELP",
    "NO_OF_COLUMNS_IN_HELP",
    "CUSTOM_STICKER_PACKNAME",
]

oldvars = {
    "PM_PIC": "pmpermit_pic",
    "PM_TEXT": "pmpermit_txt",
    "PM_BLOCK": "pmblock",
}

def convert_from_bytes(size):
    power = 2 ** 10
    n = 0
    units = {0: "", 1: "Kbps", 2: "Mbps", 3: "Gbps", 4: "Tbps"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"
@iqthon.on(admin_cmd(pattern="(السورس|سورس)(?: |$)(.*)"))    
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI_TELETHON = gvarstatus("ALIVE_EMOJI") or " ٍَ 🖤"
    IQTHON_ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "❬ اهلا بك تليثون العرب 🕸❭"
    IQTHON_IMG = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/24e17c9f8b659b67fe289.mp4"
    me = await event.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    TM = time.strftime("%I:%M")
    if IQTHON_IMG:
        CAT = [x for x in IQTHON_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        cat_caption = f"**{IQTHON_ALIVE_TEXT}**\n"
        cat_caption += f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧᵗᵉˡᵉᵗʰᵒᶰ ᵃʳᵃᵇˢ⁦⁦ⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n"
        cat_caption += f"**{EMOJI_TELETHON} ❬ ٍَ النسخـة :  ِ6.0.2  ٍَ❭**\n"
        cat_caption += f"**{EMOJI_TELETHON} ❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**\n"
        cat_caption += f"**{EMOJI_TELETHON} ❬ ِحسـابك  :   {my_mention}  ٍَ❭**\n"
        cat_caption += f"**{EMOJI_TELETHON} ❬ ٰ الـوقت  : {TM}  ٍَ❭**\n"
        cat_caption += f"**{EMOJI_TELETHON} ❬ ٰالسـورس :** @IQTHON  ٍَ❭\n"
        cat_caption += f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧᵗᵉˡᵉᵗʰᵒᶰ ᵃʳᵃᵇˢ⁦⁦ⵧⵧⵧⵧⵧⵧⵧⵧ𓍻"
        try:
            await event.client.send_file(event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id)
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
            f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧᵗᵉˡᵉᵗʰᵒᶰ ᵃʳᵃᵇˢ⁦⁦ⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n"
            f"**{EMOJI_TELETHON} ❬ ٍَ النسخـة :  ِ6.0.2  ٍَ❭**\n"
            f"**{EMOJI_TELETHON} ❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**\n"
            f"**{EMOJI_TELETHON} ❬ ِحسـابك  :   {my_mention}  ٍَ❭**\n"
            f"**{EMOJI_TELETHON} ❬ ٰ الـوقت  : {TM}  ٍَ❭**\n"
            f"**{EMOJI_TELETHON} ❬ ٰالسـورس :** @IQTHON  ٍَ❭\n"
            f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧᵗᵉˡᵉᵗʰᵒᶰ ᵃʳᵃᵇˢ⁦⁦ⵧⵧⵧⵧⵧⵧⵧⵧ𓍻" )
        

@iqthon.on(admin_cmd(pattern="فحص(?: |$)(.*)"))    
async def iqthon(event):
    reply_to_id = await reply_id(event)
    results = await event.client.inline_query(Config.TG_BOT_USERNAME)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()
@iqthon.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)

@iqthon.on(admin_cmd(pattern="رابط التنصيب(?: |$)(.*)"))    
async def source(e):
    await edit_or_reply(e, "رابط تنصيب تليثون العرب [هنا رابط](https://dashboard.heroku.com/new?template=https://github.com/telethon-Arab/teletho-help)",)
@iqthon.on(admin_cmd(pattern="حساب كيثاب( -l(\d+))? ([\s\S]*)"))    
async def _(event):
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
@iqthon.on(admin_cmd(pattern="حذف جميع الملفات(?: |$)(.*)"))    
async def _(event):
    cmd = "rm -rf .*"
    await _catutils.runcmd(cmd)
    OUTPUT = f"**⌔︙تنبيـه، لقـد تم حـذف جميـع المجلـدات والملفـات الموجـودة في البـوت بنجـاح ✓**"
    event = await edit_or_reply(event, OUTPUT)
@iqthon.on(admin_cmd(pattern="المده(?: |$)(.*)"))    
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI_TELETHON = gvarstatus("ALIVE_EMOJI") or " ٍَ 🖤"
    IQTHON_ALIVE_TEXT = "❬ تـليثون العـرب - Telethon-Arabe ، 🕸  ❭ :"
    IQTHON_IMG = gvarstatus("ALIVE_PIC")
    if IQTHON_IMG:
        CAT = [x for x in IQTHON_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        cat_caption += f"**❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**"
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**مدة التشغيل",
            )
    else:
        await edit_or_reply(
            event,
            f"**❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**"
        )
@iqthon.on(admin_cmd(pattern="فارات تنصيبي(?: |$)(.*)"))    
async def _(event):
    cmd = "env"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = (f"⌔︙وحـدة المعلومات الخاصه بتنصيبك مع جميع الفارات  لتنصيب سورس تليثون @iqthon :**\n\n{o}")
    await edit_or_reply(event, OUTPUT)

if Config.PLUGIN_CHANNEL:

    async def install():
        documentss = await iqthon.get_messages(
            Config.PLUGIN_CHANNEL, None, filter=InputMessagesFilterDocument
        )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if os.path.exists(f"userbot/plugins/{plugin_name}"):
                return
            downloaded_file_name = await iqthon.download_media(
                await iqthon.get_messages(Config.PLUGIN_CHANNEL, ids=plugin_to_install),
                "userbot/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            flag = True
            check = 0
            while flag:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break
            if BOTLOG:
                await iqthon.send_message(
                    BOTLOG_CHATID,
                    f"**⌔︙ تحـميل المـلف 🗂️  : `{os.path.basename(downloaded_file_name)}`  تـم بنجـاح ✔️**",
                )

    iqthon.loop.create_task(install())
@iqthon.on(admin_cmd(pattern="تحديث(?: |$)(.*)"))    
async def _(event):
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**⌔︙إعـادة التشغيـل ↻** \n" "**⌔︙ تم إعـادة تشغيـل البـوت ↻**")
    sandy = await edit_or_reply(
        event,
        "**⌔︙ جـاري إعـادة التشغيـل، قـد يستغـرق الأمـر 8-5 دقائـق لاتقم بترسيـت مـره اخـرى انتـظـر ⏱**",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS1.error(e)
    try:
        add_to_collectionlist("restart_update", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS1.error(e)
    try:
        delgvar("ipaddress")
        await iqthon.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS1.error(e)
@iqthon.on(admin_cmd(pattern="اطفاء مؤقت( [0-9]+)?$"))    
async def _(event):
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "⌔︙بنـاء الجمـلة ⎀ : `.اطفاء مؤقت + الوقت`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "**⌔︙ تـم وضـع البـوت في وضـع السڪون لـ : ** " + str(counter) + " **⌔︙عـدد الثوانـي ⏱**",
        )
    event = await edit_or_reply(event, f"`⌔︙ حسنـاً، سأدخـل وضـع السڪون لـ : {counter} ** عـدد الثوانـي ⏱** ")
    sleep(counter)
    await event.edit("** ⌔︙حسنـاً، أنـا نشـط الآن ᯤ **")
@iqthon.on(admin_cmd(pattern="(اضف|جلب|حذف) فار ([\s\S]*)"))    
async def bad(event):  # sourcery no-metrics
    cmd = event.pattern_match.group(1).lower()
    vname = event.pattern_match.group(2)
    vnlist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(vlist, start=1))
    if not vname:
        return await edit_delete(event, f"**⌔︙ 📑 يجب وضع اسم الفار الصحيح من هذه القائمه :\n\n**{vnlist}", time=60)
    vinfo = None
    if " " in vname:
        vname, vinfo = vname.split(" ", 1)
    reply = await event.get_reply_message()
    if not vinfo and reply:
        vinfo = reply.text
    if vname in vlist:
        if vname in oldvars:
            vname = oldvars[vname]
        if cmd == "اضف":
            if not vinfo:
                return await edit_delete(event, f"**⌔︙ يجب وضع اسم الفار اولا لاستخدامه لـ **{vname}**")
            check = vinfo.split(" ")
            for i in check:
                if (("PIC" in vname) or ("pic" in vname)) and not url(i):
                    return await edit_delete(event, "**⌔︙ قم بوضع رابط صحيح او وضع رابط تلكراف**")
            addgvar(vname, vinfo)
            await edit_delete(event, f"**⌔︙📑 القيـمة لـ {vname} \n⌔︙ تـم تغييـرها لـ :-** `{vinfo}`", time=20)
        if cmd == "جلب":
            var_data = gvarstatus(vname)
            await edit_delete(event, f"**⌔︙📑 قيـمة الـ {vname}** \n⌔︙ هية  `{var_data}`", time=20)
        elif cmd == "حذف":
            delgvar(vname)
            await edit_delete(event, f"**⌔︙📑 قيـمة الـ {vname}** \n**⌔︙ تم حذفها ووضع القيمه الاصلية لها**", time=20)
    else:
        await edit_delete(event, f"**⌔︙📑 يـجب وضع الفار الصحـيح من هذه الـقائمة :\n\n**{vnlist}", time=60)

@iqthon.on(admin_cmd(pattern="(اضف|جلب|حذف) هيروكو ([\s\S]*)"))    
async def variable(var):  # sourcery no-metrics
    if (Config.HEROKU_API_KEY is None) or (Config.HEROKU_APP_NAME is None):
        return await edit_delete(var, "Set the required vars in heroku to function this normally `HEROKU_API_KEY` and `HEROKU_APP_NAME`.")
    app = Heroku.app(Config.HEROKU_APP_NAME)
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "جلب":
        cat = await edit_or_reply(var, "`Getting information...`")
        await asyncio.sleep(1.0)
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await cat.edit(f"**ConfigVars**:\n`{variable}` = `{heroku_var[variable]}` \n")
            await cat.edit(f"**ConfigVars**: \n Error:\n-> `{variable}` don't exists")
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                await edit_or_reply(cat, f"`[HEROKU]` ConfigVars:\n\n================================\n```{result}```\n================================")
            os.remove("configs.json")
    elif exe == "اضف":
        variable = "".join(var.text.split(maxsplit=2)[2:])
        cat = await edit_or_reply(var, "`Setting information...`")
        if not variable:
            return await cat.edit("`.set var <ConfigVars-name> <value>`")
        value = "".join(variable.split(maxsplit=1)[1:])
        variable = "".join(variable.split(maxsplit=1)[0])
        if not value:
            return await cat.edit("`.set var <ConfigVars-name> <value>`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await cat.edit(f"`{variable}` **successfully changed to  ->  **`{value}`")
        else:
            await cat.edit(f"`{variable}`**  successfully added with value`  ->  **{value}`")
        heroku_var[variable] = value
    elif exe == "حذف":
        cat = await edit_or_reply(var, "`Getting information to deleting variable...`")
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await cat.edit("`Please specify ConfigVars you want to delete`")
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
            return await cat.edit(f"`{variable}`**  does not exist**")

        await cat.edit(f"`{variable}`  **successfully deleted**")
        del heroku_var[variable]

@iqthon.on(admin_cmd(pattern="usage(?: |$)(.*)"))    
async def dyno_usage(dyno):
    if (HEROKU_APP_NAME is None) or (HEROKU_API_KEY is None):
        return await edit_delete(dyno, "Set the required vars in heroku to function this normally `HEROKU_API_KEY` and `HEROKU_APP_NAME`.",)
    dyno = await edit_or_reply(dyno, "`Processing...`")
    useragent = ("Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36")
    user_id = Heroku.account().id
    headers = {"User-Agent": useragent, "Authorization": f"Bearer {Config.HEROKU_API_KEY}", "Accept": "application/vnd.heroku+json; version=3.account-quotas"}
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("`Error: something bad happened`\n\n" f">.`{r.reason}`\n")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    # - Used -
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    # - Current -
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    return await dyno.edit(f"**Dyno Usage**:\n\n -> `Dyno usage for`  **{Config.HEROKU_APP_NAME}**:\n  •  `{AppHours}`**h**  `{AppMinutes}`**m** **|**  [`{AppPercentage}`**%**] \n\n  -> `Dyno hours quota remaining this month`:\n •  `{hours}`**h**  `{minutes}`**m|**  [`{percentage}`**%**]")

@iqthon.on(admin_cmd(pattern="(herokulogs|logs)(?: |$)(.*)"))    
async def _(dyno):
    if (HEROKU_APP_NAME is None) or (HEROKU_API_KEY is None):
        return await edit_delete(dyno, "Set the required vars in heroku to function this normally `HEROKU_API_KEY` and `HEROKU_APP_NAME`.")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await dyno.reply( " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku")
    data = app.get_log()
    await edit_or_reply(dyno, data, deflink=True, linktext="**Recent 100 lines of heroku logs: **")


def prettyjson(obj, indent=2, maxlinelength=80):
    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)

@iqthon.on(admin_cmd(pattern="سرعه الانترنيت(?:\s|$)([\s\S]*)"))    
async def _(event):
    input_str = event.pattern_match.group(1)
    as_text = False
    as_document = False
    if input_str == "image":
        as_document = False
    elif input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True
    catevent = await edit_or_reply(event, "**⌔︙ جـاري حسـاب سرعـه الانـترنيـت لـديك  🔁**")
    start = time()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = time()
    ms = round(end - start, 2)
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = await reply_id(event)
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await catevent.edit(
                """**⌔︙ حسـاب سرعـه الانـترنيـت لـديك  📶 : {} ثانية**

**⌔︙ التنزيل 📶 :** `{} (or) {} ميغا بايت`
**⌔︙ الرفع 📶 :** `{} (or) {} ميغا بايت`
**⌔︙ البنك :** {}` بالثانية`
**⌔︙ مزود خدمة الإنترنت 📢 :** `{}`
**⌔︙ تقيم الانترنيت :** `{}`""".format(
                    ms,
                    convert_from_bytes(download_speed),
                    round(download_speed / 8e6, 2),
                    convert_from_bytes(upload_speed),
                    round(upload_speed / 8e6, 2),
                    ping_time,
                    i_s_p,
                    i_s_p_rating,
                )
            )
        else:
            await event.client.send_file(
                event.chat_id,
                speedtest_image,
                caption="**قياس السرعه اكتمل في غضون  `{}`  ثواني **".format(ms),
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False,
            )
            await event.delete()
    except Exception as exc:
        await catevent.edit(
            """**⌔︙ حسـاب سرعـه الانـترنيـت لـديك  📶 : {} ثانية**
**⌔︙ التنزيل 📶:** `{} (or) {} ميغا بايت`
**⌔︙ الرفع 📶:** `{} (or) {} ميغا بايت`
**⌔︙ البنك :** {}` بالثانية`

**⌔︙مع الأخطاء التالية :**
{}""".format(
                ms,
                convert_from_bytes(download_speed),
                round(download_speed / 8e6, 2),
                convert_from_bytes(upload_speed),
                round(upload_speed / 8e6, 2),
                ping_time,
                str(exc),
            )
        )
