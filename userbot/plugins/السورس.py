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
import base64
import psutil
import platform
import json
from subprocess import PIPE
from subprocess import run as runapp
from asyncio.exceptions import CancelledError
from time import sleep
from platform import python_version
from github import Github
from pySmartDL import SmartDL
from pathlib import Path
from telethon.errors import QueryIdInvalidError
from telethon.errors import QueryIdInvalidError
from telethon.tl.types import InputMessagesFilterDocument
from datetime import datetime
from telethon import version
from telethon import Button, events ,types 
from telethon.events import CallbackQuery, InlineQuery
from telethon.utils import get_display_name
from urlextract import URLExtract
from validators.url import url
from userbot import StartTime, iqthon, catversion
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id, _catutils, parse_pre, yaml_format, install_pip, get_user_from_event, _format
from ..helpers.tools import media_type
from . import media_type, progress
from ..utils import load_module, remove_plugin
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.global_collection import add_to_collectionlist, del_keyword_collectionlist, get_collectionlist_items
from . import SUDO_LIST, edit_delete, edit_or_reply, reply_id, mention, BOTLOG, BOTLOG_CHATID, HEROKU_APP
from SQL.extras import *
IQTHONPC = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/01f19261ce89d39433f35.jpg"
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
vlist = [    "ALIVE_PIC",    "ALIVE_EMOJI",    "ALIVE_TELETHONIQ",    "ALIVE_TEXT",    "ALLOW_NSFW",    "HELP_EMOJI",    "HELP_TEXT",    "IALIVE_PIC",    "PM_PIC",    "PM_TEXT",    "PM_BLOCK",    "MAX_FLOOD_IN_PMS",    "START_TEXT",    "NO_OF_ROWS_IN_HELP",    "NO_OF_COLUMNS_IN_HELP",    "CUSTOM_STICKER_PACKNAME",    "AUTO_PIC",]
DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
oldvars = {    "PM_PIC": "pmpermit_pic",
    "PM_TEXT": "pmpermit_txt",
    "PM_BLOCK": "pmblock",}
IQPIC = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/9fa2824990eb9d80adcea.jpg"
def convert_from_bytes(size):
    power = 2 ** 10
    n = 0
    units = {0: "", 1: "Kbps", 2: "Mbps", 3: "Gbps", 4: "Tbps"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"
@iqthon.on(admin_cmd(pattern="(فحص|السورس)(?: |$)(.*)"))    
async def iq(iqthonevent):
    reply_to_id = await reply_id(iqthonevent)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    iqevent = await edit_or_reply(iqthonevent, "**⎈ ⦙ جاري فحص السورس **")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "⎈ ⦙"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "𝗐𝖾𝗅𝖼𝗈𝗆𝖾 𝗍𝖾𝗅𝖾𝗍𝗁𝗈𝗇 𝖺𝗅 𝖺𝗋𝖺𝖻 𓃠"
    IQTHON_IMG = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/01f19261ce89d39433f35.jpg"
    tg_bot = Config.TG_BOT_USERNAME
    me = await iqthonevent.client.get_me()
    my_last = me.last_name
    my_mention = f"[{me.last_name}](tg://user?id={me.id})"
    TM = time.strftime("%I:%M")
    iqcaption = gvarstatus("ALIVE_TELETHONIQ") or fahs
    caption = iqcaption.format(        ALIVE_TEXT=ALIVE_TEXT,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        catver=catversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
        my_mention=my_mention,
        TM=TM,
        tg_bot=tg_bot,    )
    if IQTHON_IMG:
        CAT = [x for x in IQTHON_IMG.split()]
        PIC = random.choice(CAT)
        try:
            await iqthonevent.client.send_file(iqthonevent.chat_id, PIC, caption=caption, reply_to=reply_to_id)
            await iqevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(iqevent)
    else:
        await edit_or_reply(iqevent,caption)
fahs = """**{ALIVE_TEXT}**
𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻
**{EMOJI}  النسخـة :  ِ6.8 ** 
**{EMOJI} مـدة الـتشغيل  : {uptime} **
**{EMOJI} حسـابك  :   {my_mention} **
**{EMOJI} الـوقت  : {TM} **
**{EMOJI} البنك :** {ping} 
**{EMOJI} البوت :** {tg_bot}
**{EMOJI} السـورس :** @IQTHON 
𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻"""
@iqthon.on(admin_cmd(pattern="رابط التنصيب(?: |$)(.*)"))    
async def source(e):
    await edit_or_reply(e, "https://dashboard.heroku.com/new?template=https://github.com/telethon-Arab/telethohelp",)
@iqthon.on(admin_cmd(pattern="حساب كيثاب( -l(\d+))? ([\s\S]*)"))    
async def _(event):
    reply_to = await reply_id(event)
    username = event.pattern_match.group(3)
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await edit_delete(event, "`" + username + " not found`")
            catevent = await edit_or_reply(event, "**⎈ ⦙  جـاري إحضـار معلومـات حساب كيثاب ↯**")
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
            REPLY = "**⎈ ⦙  معلومـات الكيثاب لـ :** `{username}`\
                \n**⎈ ⦙  الإسـم 👤:** [{name}]({html_url})\
                \n**⎈ ⦙  النـوع 🔧:** `{type}`\
                \n**⎈ ⦙  الشرڪـة 🏢:** `{company}`\
                \n**⎈ ⦙  المدونـة 🔭:**  {blog}\
                \n**⎈ ⦙  الموقـع 📍:**  `{location}`\
                \n**⎈ ⦙  النبـذة 📝:**  `{bio}`\
                \n**⎈ ⦙  عـدد المتابعيـن ❤️:**  `{followers}`\
                \n**⎈ ⦙  الذيـن يتابعهـم 👁:**  `{following}`\
                \n**⎈ ⦙   عدد ريبو العام 📊:**  `{public_repos}`\
                \n**⎈ ⦙  الجمهـور 📄:**  `{public_gists}`\
                \n**⎈ ⦙  تم إنشـاء الملـف الشخصـي ✓** 🔗: `{created_at}`\
                \n**⎈ ⦙  تم تحديـث الملـف الشخصـي ✓** ✏️: `{updated_at}`".format(
                username=username, **result            )
            if repos:
                REPLY += "\n**⎈ ⦙  بعـض الريبوات 🔍 :** : " + " | ".join(repos)
            downloader = SmartDL(photo, ppath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
            await event.client.send_file(event.chat_id, ppath, caption=REPLY, reply_to=reply_to)
            os.remove(ppath)
            await catevent.delete()
@iqthon.on(admin_cmd(pattern="حذف جميع الملفات(?: |$)(.*)"))    
async def _(event):
    cmd = "rm -rf .*"
    await _catutils.runcmd(cmd)
    OUTPUT = f"**⎈ ⦙  تنبيـه، لقـد تم حـذف جميـع المجلـدات والملفـات الموجـودة في البـوت بنجـاح ✓**"
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
            await event.client.send_file(event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id)
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(event, f"**مدة التشغيل")
    else:
        await edit_or_reply(event, f"**❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**")
@iqthon.on(admin_cmd(pattern="فارات تنصيبي(?: |$)(.*)"))    
async def _(event):
    cmd = "env"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = (f"⎈ ⦙  وحـدة المعلومات الخاصه بتنصيبك مع جميع الفارات  لتنصيب سورس تليثون @iqthon :**\n\n{o}")
    await edit_or_reply(event, OUTPUT)

if Config.PLUGIN_CHANNEL:

    async def install():
        documentss = await iqthon.get_messages(            Config.PLUGIN_CHANNEL, None, filter=InputMessagesFilterDocument        )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if os.path.exists(f"userbot/plugins/{plugin_name}"):
                return
            downloaded_file_name = await iqthon.download_media(                await iqthon.get_messages(Config.PLUGIN_CHANNEL, ids=plugin_to_install),                "userbot/plugins/",            )
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
                await iqthon.send_message(                    BOTLOG_CHATID,                    f"**⎈ ⦙   تحـميل المـلف 🗂️  : `{os.path.basename(downloaded_file_name)}`  تـم بنجـاح ✔️**",                )

    iqthon.loop.create_task(install())
@iqthon.on(admin_cmd(pattern="تحديث(?: |$)(.*)"))    
async def _(event):
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**⎈ ⦙   تم تحديث سورس تليثون ↻**")
    sandy = await edit_or_reply(event , "⎈ ⦙  جـاري تـحديـث تـليثون العـرب  🔄\n🔹 - قـد يستغـرق الأمـر 5 - 10 دقائـق انتـظـر\nلاتقـم بتحـديث أكثـر من 3 مـرات باليـوم" ,)
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
        return await edit_or_reply(event, "⎈ ⦙  بنـاء الجمـلة ⎀ : `.اطفاء مؤقت + الوقت`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(            BOTLOG_CHATID,            "**⎈ ⦙   تـم وضـع البـوت في وضـع السڪون لـ : ** " + str(counter) + " **⎈ ⦙  عـدد الثوانـي ⏱**",        )
    event = await edit_or_reply(event, f"`⎈ ⦙   حسنـاً، سأدخـل وضـع السڪون لـ : {counter} ** عـدد الثوانـي ⏱** ")
    sleep(counter)
    await event.edit("** ⎈ ⦙  حسنـاً، أنـا نشـط الآن ᯤ **")
@iqthon.on(admin_cmd(pattern="تاريخ التنصيب$"))
async def psu(event):
    uname = platform.uname()
    softw = "**تاريخ تنصيب **\n ** بوت تليثون لديك :**"
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"` {bt.year}/{bt.month}/{bt.day} `"
    cpufreq = psutil.cpu_freq()
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        svmem = psutil.virtual_memory()
    help_string = f"{str(softw)}\n"
    await event.edit(help_string)
@iqthon.on(admin_cmd(pattern="(اضف|جلب|حذف) فار ([\s\S]*)"))    
async def bad(event):
    cmd = event.pattern_match.group(1).lower()
    vname = event.pattern_match.group(2)
    vnlist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(vlist, start=1))
    if not vname:
        return await edit_delete(event, f"**⎈ ⦙   📑 يجب وضع اسم الفار الصحيح من هذه القائمه :\n\n**{vnlist}", time=60)
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
            if not vinfo and vname == "ALIVE_TEMPLATE":
                return await edit_delete(event, f"**⎈ ⦙  📑 يرجى متابع قناه الفارات تجدها هنا : @iqthon")
            if not vinfo and vname == "PING_IQ":
                return await edit_delete(event, f"**⎈ ⦙ قم بكتابة الامـر بـشكل صحـيح  :  .اضف فار PING_TEXT النص الخاص بك**")
            if not vinfo:
                return await edit_delete(event, f"**⎈ ⦙ يـجب وضع القـيمـة الصحـيحه**")
            check = vinfo.split(" ")
            for i in check:
                if (("PIC" in vname) or ("pic" in vname)) and not url(i):
                    return await edit_delete(event, "**⎈ ⦙ يـجـب وضـع رابـط صحـيح **")
            addgvar(vname, vinfo)
            if BOTLOG_CHATID:
                await event.client.send_message(BOTLOG_CHATID,f"**⎈ ⦙ اضف فـار\n⎈ ⦙ {vname} الفارالذي تم تعديله :")
                await event.client.send_message(BOTLOG_CHATID, vinfo, silent=True)
            await edit_delete(event, f"**⎈ ⦙  📑 القيـمة لـ {vname} \n⎈ ⦙   تـم تغييـرها لـ :-** `{vinfo}`", time=20)
        if cmd == "جلب":
            var_data = gvarstatus(vname)
            await edit_delete(event, f"**⎈ ⦙  📑 قيـمة الـ {vname}** \n⎈ ⦙   هية  `{var_data}`", time=20)
        elif cmd == "حذف":
            delgvar(vname)
            if BOTLOG_CHATID:
                await event.client.send_message(BOTLOG_CHATID, f"**⎈ ⦙ حـذف فـار **\n**⎈ ⦙ {vname}** تـم حـذف هـذا الفـار **")
            await edit_delete(event,f"**⎈ ⦙  📑 قيـمة الـ {vname}** \n**⎈ ⦙   تم حذفها ووضع القيمه الاصلية لها**",time=20)
    else:
        await edit_delete(event, f"**⎈ ⦙  📑 يـجب وضع الفار الصحـيح من هذه الـقائمة :\n\n**{vnlist}",time=60)
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

    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
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
    items, _ = getsubitems(        obj,        itemkey="",        islast=True,        maxlinelength=maxlinelength - indent,        indent=indent,    )
    return indentitems(items, indent, level=0)
@iqthon.on(admin_cmd(pattern="استخدامي$"))
async def psu(event):
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu = "**حجم استخدامك لتليثون :**\n"
    cpuu += f"الاستخدام : `{psutil.cpu_percent()}%`\n"
    svmem = psutil.virtual_memory()
    help_string = f"{str(cpuu)}\n"
    await event.edit(help_string)
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
    catevent = await edit_or_reply(event, "**⎈ ⦙   جـاري حسـاب سرعـه الانـترنيـت لـديك  🔁**")
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
            await catevent.edit(                """**⎈ ⦙   حسـاب سرعـه الانـترنيـت لـديك  📶 : {} ثانية**

**⎈ ⦙   التنزيل 📶 :** `{} (or) {} ميغا بايت`
**⎈ ⦙   الرفع 📶 :** `{} (or) {} ميغا بايت`
**⎈ ⦙   البنك :** {}` بالثانية`
**⎈ ⦙   مزود خدمة الإنترنت 📢 :** `{}`
**⎈ ⦙   تقيم الانترنيت :** `{}`""".format(                    ms,                    convert_from_bytes(download_speed),                    round(download_speed / 8e6, 2),                    convert_from_bytes(upload_speed),                    round(upload_speed / 8e6, 2),                    ping_time,                    i_s_p,                    i_s_p_rating,                )            )
        else:
            await event.client.send_file(                event.chat_id,                speedtest_image,                caption="**قياس السرعه اكتمل في غضون  `{}`  ثواني **".format(ms),                force_document=as_document,                reply_to=reply_msg_id,                allow_cache=False,            )
            await event.delete()
    except Exception as exc:
        await catevent.edit(            
"""**⎈ ⦙   حسـاب سرعـه الانـترنيـت لـديك  📶 : {} ثانية**
**⎈ ⦙   التنزيل 📶:** `{} (or) {} ميغا بايت`
**⎈ ⦙   الرفع 📶:** `{} (or) {} ميغا بايت`
**⎈ ⦙   البنك :** {}` بالثانية`

**⎈ ⦙  مع الأخطاء التالية :** {}""".format(                ms,                convert_from_bytes(download_speed),                round(download_speed / 8e6, 2),                convert_from_bytes(upload_speed),                round(upload_speed / 8e6, 2),                ping_time,                str(exc),            )        )
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inlineiqthon(iqthon):
        builder = iqthon.builder
        result = None
        query = iqthon.text
        await bot.get_me()
        if query.startswith("تنصيب") and iqthon.query.user_id == bot.uid:
            buttons = [[Button.url("1- شرح التنصيب", "https://youtu.be/44tYK_yV02Q"), Button.url("2- استخراج ايبيات", "https://my.telegram.org/"),],[Button.url("3- ستخراج تيرمكس", "https://replit.com/@telethon-Arab/generatestringsession#start.sh"), Button.url("4- بوت فاذر", "http://t.me/BotFather"),],[Button.url("5- رابط التنصيب", "https://dashboard.heroku.com/new?template=https://github.com/telethon-Arab/telethohelp"),],[Button.url("المطـور 👨🏼‍💻", "https://t.me/LLL5L"),]]
            if IQTHONPC and IQTHONPC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(IQTHONPC, text=help1, buttons=buttons, link_preview=False)
            elif IQTHONPC:
                result = builder.document(IQTHONPC,title="iqthon",text=help1,buttons=buttons,link_preview=False)
            else:
                result = builder.article(title="iqthon",text=help1,buttons=buttons,link_preview=False)
            await iqthon.answer([result] if result else None)
@bot.on(admin_cmd(outgoing=True, pattern="تنصيب"))
async def repoiqthon(iqthon):
    if iqthon.fwd_from:
        return
    TG_BOT = Config.TG_BOT_USERNAME
    if iqthon.reply_to_msg_id:
        await iqthon.get_reply_message()
    response = await bot.inline_query(TG_BOT, "تنصيب")
    await response[0].click(iqthon.chat_id)
    await iqthon.delete()
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inlineiqthon(iqthon):
        builder = iqthon.builder
        result = None
        query = iqthon.text
        await bot.get_me()
        if query.startswith("^/orders$") and iqthon.query.user_id == bot.uid:
            buttons = [[Button.inline("اوامر السورس", data="order1"),],[Button.inline("𝟑 اوامر الحساب", data="order12"), Button.inline("𝟐 اوامر الحساب", data="order3"), Button.inline("𝟏 اوامر الحساب", data="order2"),],[Button.inline("𝟑 اوامر الكروب", data="order11"), Button.inline("𝟐 اوامر الكروب", data="order5"), Button.inline("𝟏 اوامر الكروب", data="order4"),],[Button.inline("𝟐 اوامر الالعاب", data="order7"), Button.inline("𝟏 اوامر الالعاب", data="order6"),],[Button.inline("𝟐 اوامر الصيغ", data="order9"), Button.inline("𝟏 اوامر الصيغ", data="order8"),],[Button.inline("اوامر الاغاني", data="order10"), Button.inline("اوامر الوقتي", data="order13"),],[Button.inline("اوامر التسليه", data="order14"),],[Button.inline("𝟐 الفارات", data="order16"), Button.inline("𝟏 الفارات", data="order15"),]]
            if IQTHONPC and IQTHONPC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(IQTHONPC, text=help2, buttons=buttons, link_preview=False)
            elif IQTHONPC:
                result = builder.document(IQTHONPC,title="iqthon",text=help2,buttons=buttons,link_preview=False)
            else:
                result = builder.article(title="iqthon",text=help2,buttons=buttons,link_preview=False)
            await iqthon.answer([result] if result else None)
@bot.on(admin_cmd(outgoing=True, pattern="^/orders$"))
async def repoiqthon(iqthon):
    if iqthon.fwd_from:
        return
    TG_BOT = Config.TG_BOT_USERNAME
    if iqthon.reply_to_msg_id:
        await iqthon.get_reply_message()
    response = await bot.inline_query(TG_BOT, "^/orders$")
    await response[0].click(iqthon.chat_id)
    await iqthon.delete()
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inlineiqthon(iqthon):
        builder = iqthon.builder
        result = None
        query = iqthon.text
        await bot.get_me()
        if query.startswith("(الاوامر|الأوامر)") and iqthon.query.user_id == bot.uid:
            buttons = [[Button.inline("اوامر السورس", data="order1"),],[Button.inline("𝟑 اوامر الحساب", data="order12"), Button.inline("𝟐 اوامر الحساب", data="order3"), Button.inline("𝟏 اوامر الحساب", data="order2"),],[Button.inline("𝟑 اوامر الكروب", data="order11"), Button.inline("𝟐 اوامر الكروب", data="order5"), Button.inline("𝟏 اوامر الكروب", data="order4"),],[Button.inline("𝟐 اوامر الالعاب", data="order7"), Button.inline("𝟏 اوامر الالعاب", data="order6"),],[Button.inline("𝟐 اوامر الصيغ", data="order9"), Button.inline("𝟏 اوامر الصيغ", data="order8"),],[Button.inline("اوامر الاغاني", data="order10"), Button.inline("اوامر الوقتي", data="order13"),],[Button.inline("اوامر التسليه", data="order14"),],[Button.inline("𝟐 الفارات", data="order16"), Button.inline("𝟏 الفارات", data="order15"),]]
            if IQTHONPC and IQTHONPC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(IQTHONPC, text=help2, buttons=buttons, link_preview=False)
            elif IQTHONPC:
                result = builder.document(IQTHONPC,title="iqthon",text=help2,buttons=buttons,link_preview=False)
            else:
                result = builder.article(title="iqthon",text=help2,buttons=buttons,link_preview=False)
            await iqthon.answer([result] if result else None)
@bot.on(admin_cmd(outgoing=True, pattern="(الاوامر|الأوامر)"))
async def repoiqthon(iqthon):
    if iqthon.fwd_from:
        return
    TG_BOT = Config.TG_BOT_USERNAME
    if iqthon.reply_to_msg_id:
        await iqthon.get_reply_message()
    response = await bot.inline_query(TG_BOT, "(الاوامر|الأوامر)")
    await response[0].click(iqthon.chat_id)
    await iqthon.delete()
@iqthon.on(admin_cmd(pattern="اوامري(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "**• 🚹  ⦑   اوامر السـورس العـربي ⦒ :** \n\n**⒈ ⦙  اوامر السورس.  ⊱**  (`ّ.م1 `) \n\n⒉ ⦙  اوامر الحساب   ⊱  ( `.م2 `) \n\n⒊ ⦙  اوامر الحساب٢ ⊱  ( `.م3 `)  \n\n⒋ ⦙  اوامر الكروب    ⊱  ( `.م4 `)\n\n⒌ ⦙  اوامر الكروب٢  ⊱  (` .م5` )\n\n⒍ ⦙ اوامر الالعاب والكلمات  ⊱   (` .م6 `) \n\n⒎ ⦙ اوامر تحويل الصيغ      ⊱   (` .م7 `) \n\n⒏ ⦙ اوامر التنزيلات والاغاني ⊱ ( `.م8` )")
@iqthon.on(admin_cmd(pattern="اعاده تشغيل(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, " ⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط ⬅️ `.تحديث` " "⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` ")
@iqthon.on(admin_cmd(pattern="م1(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "**🚹  ⦑   اوامر السورس  ⤮.م1⤪   ⦒  :**\n\n⑴ ⦙ `.السورس` \n**✐  : يضهر لك معلومات السورس ومدة تنصيبك❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑵ ⦙ `.رابط التنصيب` \n**✐  : سوف يعطيك رابط التنصيب ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮  \n⑶ ⦙ `.حساب كيثاب + اسم الحساب` \n**✐  : ينطيك معلومات الحساب وسورساته بموقع جيت هوب ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑷ ⦙ `.حذف جميع الملفات` \n**✐  : يحذف جميع ملفات تنصيبك ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸ ⦙ `.المده` \n**✐  : يضهر لك مدة تشغيل بوت تليثون لديك ❝** \n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.فارات تنصيبي` \n**✐  : يجلب لك جميع الفارات التي لديك وجميع معلومات تنصيبك في هيروكو ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.تحميل ملف + الرد ع الملف`\n**✐ : يحمل ملفات تليثون ❝**\n\n⑻ ⦙  `.مسح ملف + الرد ع الملف` \n**✐ :  يمسح الملف الي حملته  ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑼ ⦙  `.تحديث` \n**✐ :  امر لأعاده التشغيل وتحديث ملفات السورس وتسريع التليثون  ❝**\n\n⑽ ⦙ `.اطفاء مؤقت + عدد الثواني`\n**✐ : يقوم بأطفاء التليثون بعدد الثواني الي ضفتها  عندما تخلص الثواني سيتم اعاده تشغيل التليثون ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮")    
@iqthon.on(admin_cmd(pattern="م2(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "**🚹  ⦑   اوامر الحساب ⤮.م2⤪   ⦒  :** \n \n⑴  ⦙ `.معرفه + الرد ع الشخص` \n**✐ : سيجلب لك معرف الشخص ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑵  ⦙ `.سجل الاسماء + الرد ع الشخص` \n**✐ : يجلب لك اسماء الشخص القديمه ❝** \n ⑶  ⦙ `.انشاء بريد` \n**✐ : ينشئ لك بريد وهمي مع رابط رسائل التي تأتي الى البريد ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑷  ⦙ `.ايدي + الرد ع الشخص` \n**✐ : سيعطيك معلومات الشخص ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `. الايدي الرد ع الشخص` \n**✐ : سوف يعطيك ايدي المجموعه او ايدي حسابك ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.معلومات تخزين المجموعه` \n**✐ : يجلب لك جميع معلومات الوسائط والمساحه وعدد ملصقات وعدد تخزين ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑺ ⦙ `.تخزين الخاص تشغيل`\n**✐ : يجلب لك جميع الرسائل التي تأتي اليك في الخاص ❝**\n⑻ ⦙ . تخزين الخاص ايقاف \n✐ : يوقف ارسال جميع الرسائل التي تأتي اليك في الخاص ❝\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n\n⑼ ⦙ .تخزين الكروبات تشغيل\n✐ : يرسل لك جميع الرسائل التي يتم رد عليها في رسالتك في الكروبات ❝\n⑽ ⦙ .تخزين الكروبات ايقاف\n✐ : يوقف لك جميع ارسال الرسائل التي يتم رد عليها ❝\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑾ ⦙.الحماية تشغيل\n✐ : يقوم بتشغيل رساله الحمايه في الخاص اي شخص يراسلك سيقوم بتنبيه ❝\n⒀ ⦙  .الحماية ايقاف\n✐ : يتم تعطيل رساله الحماية في الخاص وعدم التنبيه ❝\n⒁ ⦙ .قبول\n✐ : يقوم بقبول الشخص لأرسال الرسائل بدون  تحذير  ❝\n⒂ ⦙   .رفض\n✐ : سيرفض الشخص بعدم أرسال الرسائل و الازعاج  ❝\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n⒃ ⦙ .مرفوض\n✐ : يقوم بحظر الشخص من دون تحذير  ❝\n⒄ ⦙   .المقبولين\n✐ : يقوم بعرض الاشخاص المقبولين ❝\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮")
@iqthon.on(admin_cmd(pattern="م3(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "**🚹  ⦑   اوامر الحساب 2   ⤮ .م3 ⤪   ⦒  :**\n\n⑴  ⦙  `.صورته + الرد ع الشخص`\n**✐ : يجلب صوره الشخص الذي تم رد عليه ❝**\n \n⑵  ⦙ `.رابطه + الرد ع الشخص`\n**✐ :  يجلب لك رابط الشخص الذي تم رد عليه  ❝**\n\n⑶  ⦙ `.اسمه + الرد ع الشخص`\n**✐ : يجلب لك اسم الشخص الذي تم رد عليه ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑷  ⦙  `.نسخ + الرد ع الرساله`\n**✐ : يرسل الرساله التي تم رد عليها ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `.كورونا + اسم المدينه`\n**✐ : يجلب لك مرض كورونا وعدد الموتى والمصابين**❝\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.الاذان +اسم المدينه`\n**✐ : يجلب لك معلومات الاذان في هذهّ المدينه بجميع الاوقات ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.رابط تطبيق + اسم التطبيق`\n**✐ : يرسل لك رابط التطبيق مع معلوماته ❝**\n\n⑻ ⦙ `.تاريخ الرساله + الرد ع الرساله`\n**✐ : يجلب لك تاريخ الرساله بالتفصيل ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑼ ⦙ `.بنك`\n**✐ : يقيس سرعه استجابه لدى تنصيبك ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑽ ⦙ `.سرعه الانترنيت`\n**✐ : يجلب لك سرعه الانترنيت لديك ❝**\n\n⑾ ⦙ `.الوقت`\n**✐ : يضهر لك الوقت والتاريخ واليوم ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑿ ⦙  `.وقتي`\n**✐ : يضهر لك الوقت والتاريخ بشكل جديد ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n")
@iqthon.on(admin_cmd(pattern="م4(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "**🚹  ⦑   اوامر الكروب  ⤮.م4⤪   ⦒  :**\n \n⑴  ⦙ `.كتم + الرد ع الشخص`\n**✐ : يكتم الشخص من الخاص او الكروبات فقط اذا كانت عندك صلاحيه حذف رسائل ❝**\n \n⑵  ⦙ `. الغاء كتم + الرد ع الشخص`\n**✐ :  يجلب لك جميع معرفات المشرفين في الكروب  ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑶  ⦙ `.البوتات`\n**✐ : يجلب لك جميع معرفات البوتات في الكروب ❝**\n \n⑷  ⦙ `.الأعضاء`\n**✐ : اضهار قائمة الاعضاء للكروب اذا هواي سيرسل ملف كامل لمعلوماتهم  ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `.معلومات`\n**✐ : سيرسل لك جميع معلومات الكروب بالتفصيل ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.مسح المحظورين`\n**✐ : يمسح جميع المحظورين في الكروب ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.المحذوفين`\n**✐ : يجلب لك جميع الحسابات المحذوفه ❝**\n\n⑻ ⦙ `.المحذوفين تنظيف`\n**✐ : يمسح جميع الحسابات المحذوفه في الكروب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑼ ⦙ `.احصائيات الاعضاء`\n**✐ : يمسح جميع المحظورين في الكروب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑽ ⦙ `.انتحال + الرد ع الشخص`\n**✐ : يقوم بأنتحال الشخص ويضع صورته ونبذته واسمه في حسابك عدا المعرف ❝**\n\n⑾ ⦙ `.الغاء الانتحال + الرد ع الشخص`\n**✐ : يقوم بألغاء الانتحال وسيرجع معلومات المذكوره بالسورس ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑿ ⦙  `.صنع مجموعه + اسم المجموعه`\n**✐ : يقوم بعمل مجموعه خارقه ❝**\n \n⒀ ⦙  `.صنع قناه +  اسم القناة`\n**✐ : يقوم بعمل قناه خاصه  ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⒁ ⦙ `.عدد رسائلي`\n**✐ : سيظهر لك عدد رسائلك في الكروب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n")
@iqthon.on(admin_cmd(pattern="م5(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "**🚹  ⦑   اوامر الكروب 2 ⤮.م5⤪   ⦒  :**\n\n⑴  ⦙  `.ترحيب + الرساله` \n**✐ : يضيف ترحيب في الكروب اي شخص ينضم راح يرحب بي  ❝**\n⑵  ⦙   `.مسح الترحيبات` \n**✐ :  ييقوم بمسح الترحيب من الكروب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n⑶  ⦙  `.ترحيباتي` \n**✐ :  يضهر لك جميع الترحيبات التي وضعتها في الكروب ❝**\n⑷  ⦙ `.رساله الترحيب السابقه تشغيل`  \n**✐ :  عندما يحدث تكرار سيحذف رساله الترحيب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙  `.رساله الترحيب السابقه ايقاف`\n**✐ :  عندما يحدث تكرار لا يحذف رساله الترحيب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙  `.اضف رد + الكلمه` \n**✐ :  مثلاً تدز رساله هلو تسوي عليها رد بهلوات ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.مسح رد + الكلمه` \n**✐ :  سيحذف الكلمه الي انت ضفتها ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n⑻ ⦙  `.جميع الردود` \n **✐ :  يجلب لك جميع الردود الذي قمت بأضافتها  ❝**\n⑼ ⦙  `.مسح جميع الردود` \n**✐ :  يمسح جميع الردود الي انت ضفتها ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮")
@iqthon.on(admin_cmd(pattern="م6(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "**🚹  ⦑   اوامر الالعاب والكلمات  ⤮.م6⤪   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n**⑴  ⦙  نسب وهميه :**\n`.نسبه الحب + الرد ع الشخص`\n`. نسبه الانحراف + الرد ع الشخص `\n`.نسبه الكراهيه + الرد ع الشخص`\n`.نسبه المثليه +الرد ع الشخص`\n`. نسبه النجاح + الرد ع الشخص`\n`.نسبه الانوثه + الرد ع الشخص `\n`.نسبه الغباء + الرد ع الشخص`\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n**⑵  ⦙  رفع وهمي :**\n`.رفع زباله + الرد ع الشخص `\n`.رفع منشئ + الرد ع الشخص `\n`.رفع مدير + الرد ع الشخص`\n`.رفع مطور + الرد ع الشخص` \n`.رفع مثلي + الرد ع الشخص` \n`.رفع كواد + الرد ع الشخص` \n`.رفع مرتبط + الرد ع الشخص` \n`.رفع مطي + الرد ع الشخص` \n`.رفع كحبه + الرد ع الشخص` \n`.رفع زوجتي + الرد ع الشخص` \n`.رفع صاك + الرد ع الشخص` \n`.رفع صاكه + الرد ع الشخص`\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n⑶  ⦙ `.كت`\n**✐ : لعبه اسأله كت تويت عشوائيه ❝**\n⑷  ⦙ `.اكس او` \n**✐ :  لعبه اكس او دز الامر و اللعب ويا صديقك ❝**\n⑸  ⦙  `.همسه + الكلام + معرف الشخص` \n**✐ : يرسل همسه سريه الى معرف الشخص فقط هو يكدر يشوفها  ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n\n⑹ ⦙  `.بورن + معرف الشخص + الكلام + الرد ع اي صوره`\n**✐ :  قم بتجربه الامر لتعرفه +18  ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.رسم قلوب + الاسم`\n**✐ : يكتب الاسم ع شكل قلوب  ❝**\n⑻ ⦙ `.رسم شعار + الاسم` \n**✐ : يرسم شعار للأسم  ❝**\n⑼ ⦙ `.نص ثري دي + الكلمه`\n**✐ : يقوم بكتابه الكلمه بشكل ثلاثي الابعاد~  ❝**\n⑽ ⦙ `.كلام متحرك + الكلام`\n**✐ : يقوم بكتابه الكلام حرف حرف  ❝**\n⑾  ⦙  `.ملصق متحرك + الكلام`\n**✐ : يقوم بكتابه الكلام بملصق متحرك  ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮")
@iqthon.on(admin_cmd(pattern="م7(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "**🚹  ⦑   اوامر تحويل الصيغ  ⤮.م7⤪   ⦒  :**\n\n⑴  ⦙  `.تحويل بصمه + الرد ع الصوت mp3`\n**✐ : يحول صوت mp3 الى بصمه ❝**\n⑵  ⦙  `.تحويل صوت + الرد ع الصوت` \n**✐ :  يحول البصمه الى صوت   mp3**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n⑶  ⦙  `.تحويل ملصق + الرد ع الصوره` \n**✐ :  يحول الصوره الى ملصق ❝**\n⑷  ⦙ `. تحويل صوره + الرد ع الملصق` \n**✐ :  يحول الملصق الى صوره ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙  `.تحويل متحركه + الرد ع الفيديو` \n**✐ :  يقوم بتحويل الفيديو الى متحركه ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙  `.بي دي اف + الرد ع الملف او الصوره`\n**✐ :  يحول الملف او الصوره الى بي دي اف ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.ملصقي + الرد ع الرساله` \n**✐ : يحول رساله الى ملصق ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n⑻ ⦙  `. تليجراف ميديا + الرد ع الفيديو او صوره`\n **✐ :  يقوم بتحويل الفيديو او الصوره الى رابط تليجراف للأستخدام  ❝**\n⑼ ⦙  `.تحويل رساله + الرد ع الملف` \n**✐ :  يقوم بجلب جميع الكتابه الذي داخل الملف ويقوم بأرسالها اليك ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑽ ⦙ `.تحويل فديو دائري + الرد ع الفيديو`\n**✐ : يحول الفيديو الى فيديو دائري مرئي ❝**\n⑾  ⦙ `.تحويل ملصق دائري + الرد ع الملصق` \n**✐ :  يحول الملصق الى ملصق دائري** \n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑿ ⦙  `.ترجمه en + الرد ع الرساله` \n**✐ :  يقوم بترجمه الرساله الى اللغه الانكليزيه**\n⒀ ⦙ `.ترجمه ar + الرد ع الشخص` \n**✐ :  يقوم بترجمه الرساله الى اللغه العربيه ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n")
@iqthon.on(admin_cmd(pattern="م8(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "**🚹  ⦑   اوامر التنزيلات والبحث الاغاني  ⤮.م8⤪   ⦒  :**\n\n⑴  ⦙ `.بحث صوت + اسم الاغنيه`\n**✐ : سيحمل لك الاغنية صوت ايضا يمكنك وضع رابط الاغنيه بدل الاسم ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑵  ⦙ `.بحث فيديو + اسم الاغنيه` \n**✐ : سيحمل لك الاغنية  فيديو ايضا يمكنك وضع رابط الاغنيه بدل الاسم ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n\n ⑶  ⦙ `.معلومات الاغنيه` \n**✐ : الرد ع الاغنيه سيجلب لك معلوماتها واسم الفنان ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n \n⑷  ⦙ `.كوكل بحث + موضوع البحث`\n**✐ : يجلب لك معلومات الموضوع من كوكل ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `.تخزين الصوت + الرد ع البصمه`\n**✐ : تخزين الصوت من اجل استخدامه لوضع صوت في الفيديو ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.اضف الصوت + الرد ع الصوره او متحركه او فيديو`\n**✐ : يتم اضافه الصوت الى الفيديو او المتحركه او الصوره ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.اسم الاغنيه + الرد ع الاغنيه`\n**✐ : ييجلب لك اسم الاغنيه مدة البصمه 10 الى 5 ثواني ❝**\n⑻ ⦙ `تيك توك + الرد ع رابط الفيديو.`\n**✐ : يحمل فيديو تيك توك بدون العلامه المائيه** ❝\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n")
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order1")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر السورس   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑴ ⦙ `.السورس` \n**✐  : يضهر لك معلومات السورس ومدة تنصيبك❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑵ ⦙ `.رابط التنصيب` \n**✐  : سوف يعطيك رابط التنصيب ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮  \n⑶ ⦙ `.حساب كيثاب + اسم الحساب` \n**✐  : ينطيك معلومات الحساب وسورساته بموقع جيت هوب ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑷ ⦙ `.حذف جميع الملفات` \n**✐  : يحذف جميع ملفات تنصيبك ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸ ⦙ `.المده` \n**✐  : يضهر لك مدة تشغيل بوت تليثون لديك ❝** \n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.فارات تنصيبي` \n**✐  : يجلب لك جميع الفارات التي لديك وجميع معلومات تنصيبك في هيروكو ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.تحميل ملف + الرد ع الملف`\n**✐ : يحمل ملفات تليثون ❝**\n\n⑻ ⦙  `.مسح ملف + الرد ع الملف` \n**✐ :  يمسح الملف الي حملته  ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑼ ⦙  `.تحديث` \n**✐ :  امر لأعاده التشغيل وتحديث ملفات السورس وتسريع التليثون  ❝**\n\n⑽ ⦙ `.اطفاء مؤقت + عدد الثواني`\n**✐ : يقوم بأطفاء التليثون بعدد الثواني الي ضفتها  عندما تخلص الثواني سيتم اعاده تشغيل التليثون ❝**\n⤪⟿⟿⟿⟿⤮\n\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order2")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر الحساب 1   ⦒  :** \n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑴  ⦙ `.معرفه + الرد ع الشخص` \n**✐ : سيجلب لك معرف الشخص ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑵  ⦙ `.سجل الاسماء + الرد ع الشخص` \n**✐ : يجلب لك اسماء الشخص القديمه ❝** \n ⑶  ⦙ `.انشاء بريد` \n**✐ : ينشئ لك بريد وهمي مع رابط رسائل التي تأتي الى البريد ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑷  ⦙ `.ايدي + الرد ع الشخص` \n**✐ : سيعطيك معلومات الشخص ❝** \n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `. الايدي الرد ع الشخص` \n**✐ : سوف يعطيك ايدي المجموعه او ايدي حسابك ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.معلومات تخزين المجموعه` \n**✐ : يجلب لك جميع معلومات الوسائط والمساحه وعدد ملصقات وعدد تخزين ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑺ ⦙ `.تخزين الخاص تشغيل`\n**✐ : يجلب لك جميع الرسائل التي تأتي اليك في الخاص ❝**\n⑻ ⦙ . تخزين الخاص ايقاف \n✐ : يوقف ارسال جميع الرسائل التي تأتي اليك في الخاص ❝\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n\n⑼ ⦙ .تخزين الكروبات تشغيل\n✐ : يرسل لك جميع الرسائل التي يتم رد عليها في رسالتك في الكروبات ❝\n⑽ ⦙ .تخزين الكروبات ايقاف\n✐ : يوقف لك جميع ارسال الرسائل التي يتم رد عليها ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order3")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر الحساب 2   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑴  ⦙  `.صورته + الرد ع الشخص`\n**✐ : يجلب صوره الشخص الذي تم رد عليه ❝**\n \n⑵  ⦙ `.رابطه + الرد ع الشخص`\n**✐ :  يجلب لك رابط الشخص الذي تم رد عليه  ❝**\n\n⑶  ⦙ `.اسمه + الرد ع الشخص`\n**✐ : يجلب لك اسم الشخص الذي تم رد عليه ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑷  ⦙  `.نسخ + الرد ع الرساله`\n**✐ : يرسل الرساله التي تم رد عليها ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `.كورونا + اسم المدينه`\n**✐ : يجلب لك مرض كورونا وعدد الموتى والمصابين**❝\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.الاذان +اسم المدينه`\n**✐ : يجلب لك معلومات الاذان في هذهّ المدينه بجميع الاوقات ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.رابط تطبيق + اسم التطبيق`\n**✐ : يرسل لك رابط التطبيق مع معلوماته ❝**\n\n⑻ ⦙ `.تاريخ الرساله + الرد ع الرساله`\n**✐ : يجلب لك تاريخ الرساله بالتفصيل ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑼ ⦙ `.بنك`\n**✐ : يقيس سرعه استجابه لدى تنصيبك ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑽ ⦙ `.سرعه الانترنيت`\n**✐ : يجلب لك سرعه الانترنيت لديك ❝**\n\n⑾ ⦙ `.الوقت`\n**✐ : يضهر لك الوقت والتاريخ واليوم ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑿ ⦙  `.وقتي`\n**✐ : يضهر لك الوقت والتاريخ بشكل جديد ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order4")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑  اوامر الكروب 1     ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑴  ⦙ `.كتم + الرد ع الشخص`\n**✐ : يكتم الشخص من الخاص او الكروبات فقط اذا كانت عندك صلاحيه حذف رسائل ❝**\n \n⑵  ⦙ `. الغاء كتم + الرد ع الشخص`\n**✐ :  يجلب لك جميع معرفات المشرفين في الكروب  ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑶  ⦙ `.البوتات`\n**✐ : يجلب لك جميع معرفات البوتات في الكروب ❝**\n \n⑷  ⦙ `.الأعضاء`\n**✐ : اضهار قائمة الاعضاء للكروب اذا هواي سيرسل ملف كامل لمعلوماتهم  ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `.معلومات`\n**✐ : سيرسل لك جميع معلومات الكروب بالتفصيل ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.مسح المحظورين`\n**✐ : يمسح جميع المحظورين في الكروب ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.المحذوفين`\n**✐ : يجلب لك جميع الحسابات المحذوفه ❝**\n\n⑻ ⦙ `.المحذوفين تنظيف`\n**✐ : يمسح جميع الحسابات المحذوفه في الكروب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑼ ⦙ `.احصائيات الاعضاء`\n**✐ : يمسح جميع المحظورين في الكروب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑽ ⦙ `.انتحال + الرد ع الشخص`\n**✐ : يقوم بأنتحال الشخص ويضع صورته ونبذته واسمه في حسابك عدا المعرف ❝**\n\n⑾ ⦙ `.الغاء الانتحال + الرد ع الشخص`\n**✐ : يقوم بألغاء الانتحال وسيرجع معلومات المذكوره بالسورس ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order5")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر الكروب 2   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑴  ⦙  `.ترحيب + الرساله` \n**✐ : يضيف ترحيب في الكروب اي شخص ينضم راح يرحب بي  ❝**\n⑵  ⦙   `.مسح الترحيبات` \n**✐ :  ييقوم بمسح الترحيب من الكروب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n  ⦙  `.ترحيباتي` \n**✐ :  يضهر لك جميع الترحيبات التي وضعتها في الكروب ❝**\n⑷  ⦙ `.رساله الترحيب السابقه تشغيل`  \n**✐ :  عندما يحدث تكرار سيحذف رساله الترحيب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙  `.رساله الترحيب السابقه ايقاف`\n**✐ :  عندما يحدث تكرار لا يحذف رساله الترحيب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙  `.اضف رد + الكلمه` \n**✐ :  مثلاً تدز رساله هلو تسوي عليها رد بهلوات ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.مسح رد + الكلمه` \n**✐ :  سيحذف الكلمه الي انت ضفتها ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n⑻ ⦙  `.جميع الردود` \n **✐ :  يجلب لك جميع الردود الذي قمت بأضافتها  ❝**\n⑼ ⦙  `.مسح جميع الردود` \n**✐ :  يمسح جميع الردود الي انت ضفتها ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑽ ⦙  `.صنع مجموعه + اسم المجموعه`\n**✐ : يقوم بعمل مجموعه خارقه ❝**\n \n⑾ ⦙  `.صنع قناه +  اسم القناة`\n**✐ : يقوم بعمل قناه خاصه  ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑿ ⦙ `.عدد رسائلي`\n**✐ : سيظهر لك عدد رسائلك في الكروب ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order6")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر الالعاب والكلمات 1   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n**⑴  ⦙  نسب وهميه :**\n`.نسبه الحب + الرد ع الشخص`\n`. نسبه الانحراف + الرد ع الشخص `\n`.نسبه الكراهيه + الرد ع الشخص`\n`.نسبه المثليه +الرد ع الشخص`\n`. نسبه النجاح + الرد ع الشخص`\n`.نسبه الانوثه + الرد ع الشخص `\n`.نسبه الغباء + الرد ع الشخص`\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n**⑵  ⦙  رفع وهمي :**\n`.رفع زباله + الرد ع الشخص `\n`.رفع منشئ + الرد ع الشخص `\n`.رفع مدير + الرد ع الشخص`\n`.رفع مطور + الرد ع الشخص` \n`.رفع مثلي + الرد ع الشخص` \n`.رفع كواد + الرد ع الشخص` \n`.رفع مرتبط + الرد ع الشخص` \n`.رفع مطي + الرد ع الشخص` \n`.رفع كحبه + الرد ع الشخص` \n`.رفع زوجتي + الرد ع الشخص` \n`.رفع صاك + الرد ع الشخص` \n`.رفع صاكه + الرد ع الشخص`\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑶  ⦙ `.كت`\n**✐ : لعبه اسأله كت تويت عشوائيه ❝**\n⑷  ⦙ `.اكس او` \n**✐ :  لعبه اكس او دز الامر و اللعب ويا صديقك ❝**\n⑸  ⦙  `.همسه + الكلام + معرف الشخص` \n**✐ : يرسل همسه سريه الى معرف الشخص فقط هو يكدر يشوفها  ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order7")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر الالعاب والكلمات 2   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n**⑻ ⦙ `.رسم شعار + الاسم` \n**✐ : يرسم شعار للأسم  ❝**\n⑼ ⦙ `.نص ثري دي + الكلمه`\n**✐ : يقوم بكتابه الكلمه بشكل ثلاثي الابعاد~  ❝**\n⑽ ⦙ `.كلام متحرك + الكلام`\n**✐ : يقوم بكتابه الكلام حرف حرف  ❝**\n⑾  ⦙  `.ملصق متحرك + الكلام`\n**✐ : يقوم بكتابه الكلام بملصق متحرك  ❝**\n⑿ ⦙  `.بورن + معرف الشخص + الكلام + الرد ع اي صوره`\n**✐ :  قم بتجربه الامر لتعرفه +18  ❝**\n⒀ ⦙ `.رسم قلوب + الاسم`\n**✐ : يكتب الاسم ع شكل قلوب  ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order8")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑  1 اوامر تحويل الصيغ  ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑴  ⦙  `.تحويل بصمه + الرد ع الصوت mp3`\n**✐ : يحول صوت mp3 الى بصمه ❝**\n⑵  ⦙  `.تحويل صوت + الرد ع الصوت` \n**✐ :  يحول البصمه الى صوت   mp3**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑶  ⦙  `.تحويل ملصق + الرد ع الصوره` \n**✐ :  يحول الصوره الى ملصق ❝**\n⑷  ⦙ `. تحويل صوره + الرد ع الملصق` \n**✐ :  يحول الملصق الى صوره ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙  `.تحويل متحركه + الرد ع الفيديو` \n**✐ :  يقوم بتحويل الفيديو الى متحركه ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙  `.بي دي اف + الرد ع الملف او الصوره`\n**✐ :  يحول الملف او الصوره الى بي دي اف ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.ملصقي + الرد ع الرساله` \n**✐ : يحول رساله الى ملصق ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑻ ⦙  `. تليجراف ميديا + الرد ع الفيديو او صوره`\n **✐ :  يقوم بتحويل الفيديو او الصوره الى رابط تليجراف للأستخدام  ❝**\n⑼ ⦙  `.تحويل رساله + الرد ع الملف` \n**✐ :  يقوم بجلب جميع الكتابه الذي داخل الملف ويقوم بأرسالها اليك ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑽ ⦙ `.تحويل فديو دائري + الرد ع الفيديو`\n**✐ : يحول الفيديو الى فيديو دائري مرئي ❝**\n⑾  ⦙ `.تحويل ملصق دائري + الرد ع الملصق` \n**✐ :  يحول الملصق الى ملصق دائري** \n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order9")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑  2 اوامر تحويل الصيغ   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑿ ⦙  `.ترجمه en + الرد ع الرساله` \n**✐ :  يقوم بترجمه الرساله الى اللغه الانكليزيه**\n⒀ ⦙ `.ترجمه ar + الرد ع الشخص` \n**✐ :  يقوم بترجمه الرساله الى اللغه العربيه ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order10")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر التنزيلات والبحث الاغاني ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑴  ⦙ `.بحث صوت + اسم الاغنيه`\n**✐ : سيحمل لك الاغنية صوت ايضا يمكنك وضع رابط الاغنيه بدل الاسم ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑵  ⦙ `.بحث فيديو + اسم الاغنيه` \n**✐ : سيحمل لك الاغنية  فيديو ايضا يمكنك وضع رابط الاغنيه بدل الاسم ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n\n ⑶  ⦙ `.معلومات الاغنيه` \n**✐ : الرد ع الاغنيه سيجلب لك معلوماتها واسم الفنان ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n \n⑷  ⦙ `.كوكل بحث + موضوع البحث`\n**✐ : يجلب لك معلومات الموضوع من كوكل ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `.تخزين الصوت + الرد ع البصمه`\n**✐ : تخزين الصوت من اجل استخدامه لوضع صوت في الفيديو ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.اضف الصوت + الرد ع الصوره او متحركه او فيديو`\n**✐ : يتم اضافه الصوت الى الفيديو او المتحركه او الصوره ❝**\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.اسم الاغنيه + الرد ع الاغنيه`\n**✐ : ييجلب لك اسم الاغنيه مدة البصمه 10 الى 5 ثواني ❝**\n⑻ ⦙ `تيك توك + الرد ع رابط الفيديو.`\n**✐ : يحمل فيديو تيك توك بدون العلامه المائيه** ❝\n ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inlineiqthon(iqthon):
        builder = iqthon.builder
        result = None
        query = iqthon.text
        await bot.get_me()
        if query.startswith("سورس") and iqthon.query.user_id == bot.uid:
            buttons = [[Button.url("Source", "https://t.me/IQTHON"), Button.url("Dev", "https://t.me/LLL5L")]]
            if IQTHONPC and IQTHONPC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(IQTHONPC, text=Sour, buttons=buttons, link_preview=False)
            elif IQTHONPC:
                result = builder.document(IQTHONPC,title="iqthon",text=Sour,buttons=buttons,link_preview=False)
            else:
                result = builder.article(title="iqthon",text=Sour,buttons=buttons,link_preview=False)
            await iqthon.answer([result] if result else None)
@bot.on(admin_cmd(outgoing=True, pattern="سورس"))
async def repoiqthon(iqthon):
    if iqthon.fwd_from:
        return
    TG_BOT = Config.TG_BOT_USERNAME
    if iqthon.reply_to_msg_id:
        await iqthon.get_reply_message()
    response = await bot.inline_query(TG_BOT, "سورس")
    await response[0].click(iqthon.chat_id)
    await iqthon.delete()
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order11")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر الكروب 3   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑴  ⦙  `.تفعيل حمايه المجموعه`\n**✐ : يقوم غلق جميع صلاحيات المجموعه يبقي فقط ارسال  الرسائل❝**\n \n⑵  ⦙ `تعطيل حمايه المجموعه`\n**✐ :  يقوم بتشغيل جميع صلاحيات المجموعة ماعدا تغير المعلومات و التثبيت و اضافه اعضاء تبقى مسدوده❝**\n\n⑶  ⦙ `.صلاحيات المجموعه`\n**✐ : يقوم بعرض صلاحيات المجموعه المغلقه والمفتوحه❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑷  ⦙  `.رفع مشرف + الرد على شخص`\n**✐ : يرفع الشخص مشرف يعطي صلاحيه حذف رسائل والتثبيت فقط❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `.منع + كلمة`\n**✐ : منع كلمه من الارسال في الكروب**❝\n⑹ ⦙ `.الغاء منع + كلمه`\n**✐ : يقوم بالغاء منع الكلمه ❝** \n⑺ ⦙ `.قائمه المنع`\n**✐ : يقوم بجلب جميع الكلمات الممنوعه في الكروب ❝**\n\n⑻ ⦙ ` .تاك + ( الاعداد المحدده وثابتة فقط) ⤵️`\n  ( 10 - 50 - 100 - 200  )\n**✐ : يجلب لك الاعضاء بالروابط بالعدد المحدد ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑼ ⦙ `.معرفات + ( الاعداد المحدده وثابتة فقط) ⤵️`\n  ( 10 - 50 - 100 - 200  )\n**✐ :جلب لك معرفات الاعضاء بالعدد المحدد ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders "
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order12")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر الحساب 3   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑴  ⦙  `.احصائيات حسابي`\n**✐ : يقوم بجلب عدد القنوات والاشخاص والمجموعات و التاكات لحسابك ❝**\n \n⑵  ⦙ `.قائمه جميع القنوات`\n**✐ :  يقوم بجلب جميع القنوات التي في حسابك مع روابط الخاصه بهن  ❝**\n\n⑶  ⦙ `.قائمه قنوات اديرها`\n**✐ : يقوم بجلب جميع القنوات التي مشرف بها مع روابطهن ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n⑷  ⦙  `.قائمه قنوات امتلكها`\n**✐ : يقوم بجلب جميع القنوات التي تمتلكها مع روابطهن ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑸  ⦙ `.قائمه جميع المجموعات `\n**✐ : يقوم بجلب جميع المجموعات في حسابك مع روابطهن**❝\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑹ ⦙ `.قائمه مجموعات اديرها`\n**✐ : يقوم بجلب جميع المجموعات التي مرفوع بها مشرف مع روابطهن ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑺ ⦙ `.قائمه مجموعات امتلكها`\n**✐ : يقوم بجلب جميع المجموعات التي تمتلكها مع روابطهن ❝**\n\n⑻ ⦙ `.وضع بايو + الرد على البايو`\n**✐ : يضع الكلمه التي تم رد عليها في البايو الخاص بك ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑼ ⦙ `.وضع اسم + الرد على الاسم`\n**✐ : يضع الاسم الذي تم رد عليه في اسمك ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑽ ⦙ `.وضع صوره + الرد على صوره`\n**✐ : يضع الصوره التي تم رد عليها في حسابك ❝**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order13")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑   اوامر الوقتي   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n ⑴ ⦙ `.اسم وقتي`\n**✐ : يضع الوقت المزخرف في اسمك تلقائيا ❝**\n\n ⑵ ⦙  `.نبذه وقتيه`\n**✐ : يضع الوقت المزخرف في نبذه الخاصه بك تلقائيا ❝**\n\n⑶⦙ `.صوره وقتيه`\n**✐ : يضع لك الوقت لمزخرف في صورتك تغير تلقائي ❝**\n\n\n⑷⦙ `.ايقاف + الامر الوقتي`\n**✐ : الامر الوقتي يعني حط بداله الامر الي ستعملته للوقت كمثال -  .ايقاف اسم وقتي او .ايقاف نبذه وقتيه او .ايقاف صوره وقتي ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order14")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑    الاوامر المتحركه للتسلية   ⦒  :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n\n `.غبي`\n`.تفجير`\n`.قتل`\n`.طوبه`\n`.مربعات`\n`.حلويات`\n`.نار`\n`.هلكوبتر`\n`.اشكال مربع`\n`.دائره`\n`.قلب `\n`.مزاج`\n`.قرد`\n`.ايد`\n`.العد التنازلي`\n`.الوان قلوب`\n`.عين`\n`.ثعبان`\n`.رجل`\n`.رموز شيطانيه`\n`.قطار`\n`.موسيقى`\n`.رسم`\n`.فراشه`\n`.مكعبات`\n`.مطر`\n`.تحركات`\n`.ايموجيات`\n`.طائره`\n`.شرطي`\n`.النضام الشمسي`\n`.افكر`\n`.اضحك`\n`.ضايج`\n`.ساعه متحركه`\n`.بوسه`\n`.قلوب`\n`.رياضه`\n`.الارض`\n`.قمر`\n`.اقمار`\n`.قمور`\n`.زرفه`\n`.بيبي`\n`.تفاعلات`\n`.اخذ قلبي`\n`.اشوفج السطح`\n`.احبك`\n`.اركض`\n`.روميو`\n`.البنك`\n`.تهكير + الرد على شخص`\n`.طياره`\n`.مصاصه`\n`.مصه`\n`.جكه`\n`.اركضلي`\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order15")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑  1 اوامـر الـفـارات  ⦒ :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑴ ⦙ `.اضف فار + اسم افار + القيمه`\n**✐ :  يضيف اليك الفار الخاص بسورس ❝**\n⑵ ⦙ `.حذف فار + اسم الفار`\n**✐ :  يحذف الفار الذي اضفته ❝**\n⑶  ⦙ `.جلب فار + اسم الفار`\n**✐ :  يرسل اليك معلومات الفار وقيمه الفار ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n**☣️  ⦑  1  الــفــارات  ⦒  :**\n\n**⑴ ⦙  لأضـافة فار كليشة حماية  الخاص للأضـافـة  ارسـل  :**\n`.اضف فار PM_TEXT + كليشة الحمايه الخاصة بـك`\n\n**⑵  ⦙ لأضـافة فار  ايدي الكـروب للأضافة أرسل بالرسائل محفوضة : **\n`.اضف فار PM_LOGGER_GROUP_ID  + ايدي مجموعتك`\n\n**⑶  ⦙ لأضـافة فار الايمـوجي  : **\n`.اضف فار ALIVE_EMOJI + الايموجي`\n\n **⑷  ⦙ لأضـافة فار  رسـاله بداية أمر السورس  : **\n `.اضف فار ALIVE_TEXT + النص`\n\n**⑸  ⦙  لأضـافة فار صورة رساله حماية  الخاص :**\n `.اضف فار PM_PIC + رابط تليجراف الصورة او الفيديو`\n\n **⑹ ⦙  لأضافـة فار صورة او فيديو أمر  السـورس : **\n `.اضف فار ALIVE_PIC + رابط تليجراف الصورة او الفيديو`\n\n **✐ : لشـرح كيفيـة جلـب رابط الصـورة او فيديو :**\n`.تليجراف ميديا + الرد على صورة او فيديو`\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"order16")))
async def inlineiqthon(iqthon):
    text = "**🚹  ⦑  2 اوامـر الـفـارات  ⦒ :**\n\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ \n⑴ ⦙ `.اضف فار + اسم افار + القيمه`\n**✐ :  يضيف اليك الفار الخاص بسورس ❝**\n⑵ ⦙ `.حذف فار + اسم الفار`\n**✐ :  يحذف الفار الذي اضفته ❝**\n⑶  ⦙ `.جلب فار + اسم الفار`\n**✐ :  يرسل اليك معلومات الفار وقيمه الفار ❝**\n⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮\n\n**☣️  ⦑  2  الــفــارات  ⦒  :**\n\n**⑴ ⦙  لتغير كليشة الفحص كاملة :**\n`.اضف فار ALIVE_TELETHONIQ + كليشه مع المتغيرات`\n\n**✐ : متغيرات كليشه الفحص  :**\n\n1 -  :  `{uptime}` :  مده التشغيل بوتك \n2 -  :  `{my_mention}`  : رابط حسابك  \n3 -  :  `{TM}`  : الوقت \n4 -  :  `{ping} ` : البنك \n5 -  : ` {telever} ` : نسخه تليثون \n6 -  :  `{tg_bot}` :  معرف بوتك \n\n**⎈ ⦙ لأضهار الأوامر مرة اخرى قم بضغط على ⬅️**  /orders"
    await iqthon.edit(text)
@iqthon.on(admin_cmd(pattern="تحميل الملف(?: |$)(.*)"))    
async def install(event):
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(await event.get_reply_message(), "userbot/plugins/")
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await edit_delete(event, f"**⎈ ⦙   تم تثبيـت الملـف بنجـاح ✓** `{os.path.basename(downloaded_file_name)}`", 10)
            else:
                os.remove(downloaded_file_name)
                await edit_delete(event, "**⎈ ⦙  حـدث خطـأ، هـذا الملف مثبـت بالفعـل !**", 10)
        except Exception as e:
            await edit_delete(event, f"**⎈ ⦙  خطـأ ⚠️:**\n`{str(e)}`", 10)
            os.remove(downloaded_file_name)
@iqthon.on(admin_cmd(pattern="مسح الملف(?: |$)(.*)"))    
async def unload(event):
    shortname = event.pattern_match.group(1)
    path = Path(f"userbot/plugins/{shortname}.py")
    if not os.path.exists(path):
        return await edit_delete(event, f"**⎈ ⦙   ملـف مـع مسـار ⚠️ {path} لإلغـاء التثبيـت ⊠**")
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"**⎈ ⦙   {shortname} تم إلغـاء التثبيـت بنجـاح ✓**")
    except Exception as e:
        await edit_or_reply(event, f"**⎈ ⦙  تمـت الإزالـة بنجـاح ✓ : {shortname}\n{str(e)}**")
@iqthon.on(admin_cmd(pattern="هاش ([\s\S]*)"))    
async def gethash(hash_q):
    hashtxt_ = "".join(hash_q.text.split(maxsplit=1)[1:])
    with open("hashdis.txt", "w+") as hashtxt:
        hashtxt.write(hashtxt_)
    md5 = runapp(["md5sum", "hashdis.txt"], stdout=PIPE)
    md5 = md5.stdout.decode()
    sha1 = runapp(["sha1sum", "hashdis.txt"], stdout=PIPE)
    sha1 = sha1.stdout.decode()
    sha256 = runapp(["sha256sum", "hashdis.txt"], stdout=PIPE)
    sha256 = sha256.stdout.decode()
    sha512 = runapp(["sha512sum", "hashdis.txt"], stdout=PIPE)
    runapp(["rm", "hashdis.txt"], stdout=PIPE)
    sha512 = sha512.stdout.decode()
    ans = f"**Text : **\
            \n`{hashtxt_}`\
            \n**MD5 : **`\
            \n`{md5}`\
            \n**SHA1 : **`\
            \n`{sha1}`\
            \n**SHA256 : **`\
            \n`{sha256}`\
            \n**SHA512 : **`\
            \n`{sha512[:-1]}`\
         "
    await edit_or_reply(hash_q, ans)
@iqthon.on(admin_cmd(pattern="هاش(ين|دي) ([\s\S]*)"))    
async def endecrypt(event):
    string = "".join(event.text.split(maxsplit=2)[2:])
    catevent = event
    if event.pattern_match.group(1) == "ين":
        if string:
            result = base64.b64encode(bytes(string, "utf-8")).decode("utf-8")
            result = f"**Shhh! It's Encoded : **\n`{result}`"
        else:
            reply = await event.get_reply_message()
            if not reply:
                return await edit_delete(event, "`What should i encode`")
            mediatype = media_type(reply)
            if mediatype is None:
                result = base64.b64encode(bytes(reply.text, "utf-8")).decode("utf-8")
                result = f"**Shhh! It's Encoded : **\n`{result}`"
            else:
                catevent = await edit_or_reply(event, "`Encoding ...`")
                c_time = time.time()
                downloaded_file_name = await event.client.download_media(                    reply,                    Config.TMP_DOWNLOAD_DIRECTORY,                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(                        progress(d, t, catevent, c_time, "trying to download")                    ),                )
                catevent = await edit_or_reply(event, "`Encoding ...`")
                with open(downloaded_file_name, "rb") as image_file:
                    result = base64.b64encode(image_file.read()).decode("utf-8")
                os.remove(downloaded_file_name)
        await edit_or_reply(            catevent, result, file_name="encodedfile.txt", caption="It's Encoded"        )
    else:
        try:
            lething = str(                base64.b64decode(                    bytes(event.pattern_match.group(2), "utf-8"), validate=True                )            )[2:]
            await edit_or_reply(event, "**Decoded text :**\n`" + lething[:-1] + "`")
        except Exception as e:
            await edit_delete(event, f"**Error:**\n__{str(e)}__")
