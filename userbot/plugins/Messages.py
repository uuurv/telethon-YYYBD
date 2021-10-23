import re
import asyncio
import base64
import string
import os
import subprocess
from datetime import datetime
from asyncio import sleep
from geopy.geocoders import Nominatim
from gtts import gTTS
from telethon import events
from telethon.tl import types, functions, types
from telethon.tl.types import Channel, MessageMediaWebPage, ChatBannedRights
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.functions.channels import EditBannedRequest
from telethon.utils import get_display_name
from googletrans import LANGUAGES, Translator
from userbot.core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..helpers.utils import _catutils, parse_pre, yaml_format
from ..helpers import reply_id
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.welcome_sql import add_welcome_setting, get_current_welcome_settings, rm_welcome_setting, update_previous_welcome
from ..sql_helper.echo_sql import addecho, get_all_echos, get_echos, is_echo, remove_all_echos, remove_echo, remove_echos
from ..sql_helper.filter_sql import add_filter, get_filters, remove_all_filters, remove_filter
from ..sql_helper import antiflood_sql as sql
from ..utils import is_admin
from . import BOTLOG, BOTLOG_CHATID, get_user_from_event, deEmojify, reply_id
from userbot import iqthon
LOGS = logging.getLogger(__name__)
CHAT_FLOOD = sql.__load_flood_settings()
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
until_date=None, view_messages=None, send_messages=True)


@iqthon.on(admin_cmd(pattern="وقتيه (\d*) ([\s\S]*)"))    
async def _(event):
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    ttl = int(cat[0])
    await event.delete()
    await sleep(ttl)
    await event.respond(message)

    
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
@iqthon.on(admin_cmd(pattern="ازاله التوجيه(?: |$)(.*)"))    
async def _(event):
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
@iqthon.on(admin_cmd(pattern="ارسال للكروبات ?(.*)$"))    
async def gcast(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "هـذا الامـر مقـيد ")
    xx = event.pattern_match.group(1)
    if not xx:
        return edit_or_reply(event, "**⌔︙ يجـب وضـع نـص مع الامـر للتوجيـه**")
    tt = event.text
    msg = tt[6:]
    event = await edit_or_reply(event, "** ⌔︙ يتـم الـتوجيـة للـمجموعـات انتـظر قليلا**")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await event.edit(f"⌔︙ تـم بنـجـاح فـي {done} من الـدردشـات , خطـأ فـي {er} من الـدردشـات")
async def getTranslate(text, **kwargs):
    translator = Translator()
    result = None
    for _ in range(10):
        try:
            result = translator.translate(text, **kwargs)
        except Exception:
            translator = Translator()
            await sleep(0.1)
    return result
@iqthon.iq_cmd(incoming=True, groups_only=True)
async def _(event):
    if not CHAT_FLOOD:
        return
    catadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not catadmin:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message=f"""**⌔︙ تحذير تكرار فـي المجموعة : لـ**
@تاك للادمنيه  : [User](tg://user?id={event.message.sender_id}) لقد قام بتكرار الرسائل .
`{str(e)}`""",
            reply_to=event.message.id,
        )
        await asyncio.sleep(4)
        await no_admin_privilege_message.edit(
            "**⌔︙ هذا الشخص الذي قام بتكرار الرسائل والازعاج **"
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message=f"""**⌔︙ تحذير تكرار فـي المجموعة : لـ**
[User](tg://user?id={event.message.sender_id}) تم تقيد الشخص بسبب عمل تكرار للرسائل والازعاج.""",
            reply_to=event.message.id,
        )
@iqthon.on(admin_cmd(pattern="ارسال للخاص ?(.*)$"))    
async def gucast(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await edit_or_reply(event, "هـذا الامـر مقـيد ")
    xx = event.pattern_match.group(1)
    if not xx:
        return edit_or_reply(event, "** ⌔︙ يجـب وضـع نـص مع الامـر للتوجيـه**")
    tt = event.text
    msg = tt[7:]
    await edit_or_reply(event, "** ⌔︙ يتـم الـتوجيـة للخـاص انتـظر قليلا**")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await event.edit(f"⌔︙ تـم بنـجـاح فـي {done} من الـدردشـات , خطـأ فـي {er} من الـدردشـات")

async def spam_function(event, sandy, cat, sleeptimem, sleeptimet, DelaySpam=False):
  
    counter = int(cat[0])
    if len(cat) == 2:
        spam_message = str(cat[1])
        for _ in range(counter):
            if event.reply_to_msg_id:
                await sandy.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and sandy.media:
        for _ in range(counter):
            sandy = await event.client.send_file(
                event.chat_id, sandy, caption=sandy.text
            )
            await _catutils.unsavegif(event, sandy)
            await asyncio.sleep(sleeptimem)
        if BOTLOG:
            if DelaySpam is not True:
                if event.is_private:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "**⌔︙ التڪـرار  ♽**\n"
                        + f"**⌔︙ تم تنفيذ التكرار بنجاح في ▷** [User](tg://user?id={event.chat_id}) **الدردشـة مـع** {counter} **عدد المرات مع الرسالة أدناه**",
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "**⌔︙ التڪـرار  ♽**\n"
                        + f"**⌔︙ تم تنفيذ التكرار بنجاح في ▷** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **مـع** {counter} **عدد المرات مع الرسالة أدناه**",
                    )
            elif event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔︙ التكرار الوقتي 💢**\n"
                    + f"**⌔︙ تم تنفيذ التكرار الوقتي  بنجاح في ▷** [User](tg://user?id={event.chat_id}) **الدردشـة مـع** {counter} **عدد المرات مع الرسالة أدناه مع التأخير** {sleeptimet} ** الثوانـي ⏱**",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔︙ التكرار الوقتي 💢**\n"
                    + f"**⌔︙ تم تنفيذ التكرار الوقتي  بنجاح في ▷** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **مـع** {counter} **عدد المرات مع الرسالة أدناه مع التأخير** {sleeptimet} ** الثوانـي ⏱**",
                )

            sandy = await event.client.send_file(BOTLOG_CHATID, sandy)
            await _catutils.unsavegif(event, sandy)
        return
    elif event.reply_to_msg_id and sandy.text:
        spam_message = sandy.text
        for _ in range(counter):
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    else:
        return
    if DelaySpam is not True:
        if BOTLOG:
            if event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔︙ التڪـرار  ♽**\n"
                    + f"**⌔︙ تم تنفيذ التكرار بنجاح في ▷** [User](tg://user?id={event.chat_id}) **الدردشـة مـع** {counter} **رسائـل الـ  ✉️ :** \n"
                    + f"⌔︙ `{spam_message}`",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔︙ التڪـرار  ♽**\n"
                    + f"**⌔︙ تم تنفيذ التكرار بنجاح في ▷** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **الدردشـة مـع** {counter} **رسائـل الـ  ✉️ :** \n"
                    + f"⌔︙ `{spam_message}`",
                )
    elif BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔︙ التكرار الوقتي 💢**\n"
                + f"**⌔︙ تم تنفيذ التكرار الوقتي  بنجاح في ▷** [User](tg://user?id={event.chat_id}) **الدردشـة مـع** {sleeptimet} seconds and with {counter} **رسائـل الـ  ✉️ :** \n"
                + f"⌔︙ `{spam_message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔︙ التكرار الوقتي 💢**\n"
                + f"**⌔︙ تم تنفيذ التكرار الوقتي  بنجاح في ▷** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **الدردشـة مـع** {sleeptimet} **الثوانـي و مـع** {counter} **رسائـل الـ  ✉️ :** \n"
                + f"⌔︙ `{spam_message}`",
            )

@iqthon.on(admin_cmd(pattern="تكرار (.*)"))    
async def spammer(event):
    "⌔︙ملـئ النـص في الدردشـة 🔖"
    sandy = await event.get_reply_message()
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    try:
        counter = int(cat[0])
    except Exception:
        return await edit_delete(
            event, "⌔︙إستخـدم بناء الجملة المناسب للإزعاج، صيغة Foe تشير إلىٰ قائمة التعليمات 💡"
        )
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    await event.delete()
    await spam_function(event, sandy, cat, sleeptimem, sleeptimet)

@iqthon.on(admin_cmd(pattern="مؤقت ([\s\S]*)"))    
async def spammer(event):
    "**⌔︙ لإرسال التكرار مع تخصيص وقت إيقـاف بين كل رسالة ❗️**"
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    try:
        sleeptimet = sleeptimem = float(input_str[0])
    except Exception:
        return await edit_delete(
            event, "**⌔︙خطأ إستخـدم بناء جملة مناسبة لتوقيت ❗️**"
        )
    cat = input_str[1:]
    await event.delete()
    await spam_function(event, reply, cat, sleeptimem, sleeptimet, DelaySpam=True)
        
@iqthon.on(admin_cmd(pattern="مؤقته (\d*) ([\s\S]*)"))    
async def selfdestruct(destroy):
    "To self destruct the sent message"
    cat = ("".join(destroy.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    ttl = int(cat[0])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, message)
    await sleep(ttl)
    await smsg.delete()

@iqthon.on(events.ChatAction)
async def _(event):  # sourcery no-metrics
    cws = get_current_welcome_settings(event.chat_id)
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        if gvarstatus("clean_welcome") is None:
            try:
                await event.client.delete_messages(event.chat_id, cws.previous_welcome)
            except Exception as e:
                LOGS.warn(str(e))
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = chat.title or "this chat"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "<a href='tg://user?id={}'>{}</a>".format(
            a_user.id, a_user.first_name
        )
        my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
            elif cws.reply:
                current_saved_welcome_message = cws.reply
        current_message = await event.reply(
            current_saved_welcome_message.format(
                mention=mention,
                title=title,
                count=count,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            ),
            file=file_media,
            parse_mode="html",
        )
        update_previous_welcome(event.chat_id, current_message.id)

@iqthon.on(admin_cmd(pattern="ترحيب(?:\s|$)([\s\S]*)"))    
async def save_welcome(event):
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙رسالة الترحيب 🔖 :\
                \n⌔︙ايدي الدردشة 🆔 : {event.chat_id}\
                \n⌔︙يتم حفظ الرسالة التالية كملاحظة ترحيبية لـ 🔖 : {event.chat.title}, ",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            return await edit_or_reply(
                event,
                "⌔︙ حفظ الصورة كرسالة ترحيبية يتطلب وضع الفار لـ  BOTLOG_CHATID ",
            )
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "**⌔︙تم حفظ الترحيب  \n {} بهذه الدردشة بنجاح ✅**"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("saved"))
    rm_welcome_setting(event.chat_id)
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("updated"))
    await edit_or_reply("⌔︙حدث خطأ أثناء وضع ترحيب في هذه المجموعة ⚠️")


@iqthon.on(admin_cmd(pattern="مسح الترحيبات(?: |$)(.*)"))    
async def del_welcome(event):
    "⌔︙لمسح الرسائل الترحيبية 🗑"
    if rm_welcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "**⌔︙تم مسح جميع الرسائل الترحيبية لهذه الدردشة بنجاح ✅**")
    else:
        await edit_or_reply(event, "**⌔︙لم يتم حفظ أي رسائل ترحيبية هنا ⚠️**")

@iqthon.on(admin_cmd(pattern="ترحيباتي(?: |$)(.*)"))    
async def show_welcome(event):
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        return await edit_or_reply(event, "**⌔︙لم يتم حفظ أي رسائل ترحيبية هنا ⚠️**")
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "**⌔︙أنا الآن أقوم بالترحيب بالمستخدمين الجدد مع هذه الرسالة ✅**"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "**⌔︙أنا الآن أقوم بالترحيب بالمستخدمين الجدد مع هذه الرسالة ✅**"
        )
        await event.reply(cws.reply, link_preview=False)

@iqthon.on(admin_cmd(pattern="رساله الترحيب السابقه (تشغيل|ايقاف)$"))    
async def del_welcome(event):
    input_str = event.pattern_match.group(1)
    if input_str == "تشغيل":
        if gvarstatus("clean_welcome") is None:
            return await edit_delete(event, "**⌔︙تم تشغيلها بالفعل ✅**")
        delgvar("clean_welcome")
        return await edit_delete(
            event,
            "**⌔︙ من الآن رسالة الترحيب السابقة سيتم حذفها وسيتم إرسال رسالة الترحيب الجديدة ⚠️**",
        )
    if gvarstatus("clean_welcome") is None:
        addgvar("clean_welcome", "false")
        return await edit_delete(
            event, "**⌔︙من الآن لن يتم حذف رسالة الترحيب السابقة ⚠️**"
        )
    await edit_delete(event, "**⌔︙تم إيقافها بالفعل ✅**")

@iqthon.on(admin_cmd(pattern="موقع(?: |$)(.*)"))    
async def gps(event):
    "⌔︙لإرسـال خارطـة الموقـع المعطـىٰ 🗺"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "** ⌔︙ جاري العثـور على الموقع  … **")
    geolocator = Nominatim(user_agent="catuserbot")
    geoloc = geolocator.geocode(input_str)
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await event.client.send_file(
            event.chat_id,
            file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),
            caption=f"**⌔︙ الموقـع 𖠕  : **`{input_str}`",
            reply_to=reply_to_id,
        )
        await catevent.delete()
    else:
        await catevent.edit("⌔︙ عـذراً، لـم أستطـع إيجـاده  ⚠️")

@iqthon.on(admin_cmd(pattern="ازعاج(?: |$)(.*)"))    
async def echo(event):
    "To echo the user messages"
    if event.reply_to_msg_id is None:
        return await edit_or_reply(
            event, "**⌔︙ يرجى الرد على الشخص الذي تـريد ازعاجه ❕**"
        )
    catevent = await edit_or_reply(event, "**⌔︙ يتم تفعيل هذا الامر انتظر قليلا ❕**")
    user, rank = await get_user_from_event(event, catevent, nogroup=True)
    if not user:
        return
    reply_msg = await event.get_reply_message()
    chat_id = event.chat_id
    user_id = reply_msg.sender_id
    if event.is_private:
        chat_name = user.first_name
        chat_type = "Personal"
    else:
        chat_name = event.chat.title
        chat_type = "Group"
    user_name = user.first_name
    user_username = user.username
    if is_echo(chat_id, user_id):
        return await edit_or_reply(event, "**⌔︙ تـم تفـعيل وضـع الازعاج على الشخص بنجاح ✅ **")
    try:
        addecho(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await edit_delete(catevent, f"⌔︙ Error:\n`{str(e)}`")
    else:
        await edit_or_reply(catevent, "**⌔︙ تـم تفعـيل امـر التقليد علـى هذا الشـخص**\n **⌔︙ سـيتم تقليـد جميع رسائلـه هـنا**")

@iqthon.on(admin_cmd(pattern="الغاء الازعاج( -a)?"))    
async def echo(event):
    "To delete echo in this chat."
    input_str = event.pattern_match.group(1)
    if input_str:
        lecho = get_all_echos()
        if len(lecho) == 0:
            return await edit_delete(
                event, "**⌔︙ لم يتم تفعيل الازعاج بالاصل لاي شخص ⚠️**"
            )
        try:
            remove_all_echos()
        except Exception as e:
            await edit_delete(event, f"**⌔︙ هناك خطا ‼️ :**\n`{str(e)}`", 10)
        else:
            await edit_or_reply(
                event, "**⌔︙ تـم ايقاف وضـع الازعاج على الجميع بنجاح ✅ .**"
            )
    else:
        lecho = get_echos(event.chat_id)
        if len(lecho) == 0:
            return await edit_delete(
                event, "**⌔︙ لم يتم تفعيل الازعاج بالاصل لاي شخص ⚠️**"
            )
        try:
            remove_echos(event.chat_id)
        except Exception as e:
            await edit_delete(event, f"**⌔︙ هناك خطا ‼️ :**\n`{str(e)}`", 10)
        else:
            await edit_or_reply(
                event, "**⌔︙ تـم ايقاف وضـع الازعاج على الجميع بنجاح ✅**"
            )

@iqthon.on(admin_cmd(pattern="المزعجهم( -a)?$"))    
async def echo(event):  # sourcery no-metrics
    "To list all users on who you enabled echoing."
    input_str = event.pattern_match.group(1)
    private_chats = ""
    output_str = "**⌔︙ قائمه الاشخاص الذين تم ازعاجهم :**\n\n"
    if input_str:
        lsts = get_all_echos()
        group_chats = ""
        if len(lsts) > 0:
            for echos in lsts:
                if echos.chat_type == "Personal":
                    if echos.user_username:
                        private_chats += f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                    else:
                        private_chats += (
                            f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                        )
                else:
                    if echos.user_username:
                        group_chats += f"☞ [{echos.user_name}](https://t.me/{echos.user_username}) in chat {echos.chat_name} of chat id `{echos.chat_id}`\n"
                    else:
                        group_chats += f"☞ [{echos.user_name}](tg://user?id={echos.user_id}) in chat {echos.chat_name} of chat id `{echos.chat_id}`\n"

        else:
            return await edit_or_reply(event, "**⌔︙ لم يتم تفعيل ازعاج  اي شخص  ⚠️**")
        if private_chats != "":
            output_str += "**⌔︙ الـدردشـات الـخاصة **\n" + private_chats + "\n\n"
        if group_chats != "":
            output_str += "**⌔︙ دردشـات الـمجموعات **\n" + group_chats
    else:
        lsts = get_echos(event.chat_id)
        if len(lsts) <= 0:
            return await edit_or_reply(
                event, "**لم يتم تفعيل الازعاج بالاصل في هذه الدردشه ⚠️**"
            )

        for echos in lsts:
            if echos.user_username:
                private_chats += (
                    f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                )
            else:
                private_chats += (
                    f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                )
        output_str = f"**⌔︙ الاشخاص الذي تم تقليدهم في هذه الدردشه :**\n" + private_chats

    await edit_or_reply(event, output_str)


@iqthon.iq_cmd(incoming=True, edited=False)
async def samereply(event):
    if is_echo(event.chat_id, event.sender_id) and (
        event.message.text or event.message.sticker
    ):
        await event.reply(event.message)

@iqthon.iq_cmd(incoming=True)
async def filter_incoming_handler(handler):  # sourcery no-metrics
    if handler.sender_id == handler.client.uid:
        return
    name = handler.raw_text
    filters = get_filters(handler.chat_id)
    if not filters:
        return
    a_user = await handler.get_sender()
    chat = await handler.get_chat()
    me = await handler.client.get_me()
    title = chat.title or "this chat"
    participants = await handler.client.get_participants(chat)
    count = len(participants)
    mention = f"[{a_user.first_name}](tg://user?id={a_user.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = a_user.first_name
    last = a_user.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{a_user.username}" if a_user.username else mention
    userid = a_user.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    for trigger in filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger.keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            if trigger.f_mesg_id:
                msg_o = await handler.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                )
                await handler.reply(
                    msg_o.message.format(
                        mention=mention,
                        title=title,
                        count=count,
                        first=first,
                        last=last,
                        fullname=fullname,
                        username=username,
                        userid=userid,
                        my_first=my_first,
                        my_last=my_last,
                        my_fullname=my_fullname,
                        my_username=my_username,
                        my_mention=my_mention,
                    ),
                    file=msg_o.media,
                )
            elif trigger.reply:
                await handler.reply(
                    trigger.reply.format(
                        mention=mention,
                        title=title,
                        count=count,
                        first=first,
                        last=last,
                        fullname=fullname,
                        username=username,
                        userid=userid,
                        my_first=my_first,
                        my_last=my_last,
                        my_fullname=my_fullname,
                        my_username=my_username,
                        my_mention=my_mention,
                    ),
                )

   

@iqthon.on(admin_cmd(pattern="اضف رد ([\s\S]*)")) 
async def add_new_filter(new_handler):
    keyword = new_handler.pattern_match.group(1)
    string = new_handler.text.partition(keyword)[2]
    msg = await new_handler.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG:
            await new_handler.client.send_message(
                BOTLOG_CHATID,
                f"**⌔︙ اضـافه ردّ ⎗ :**\
            \n**⌔︙آيـدي الدردشـة 🆔 :** {new_handler.chat_id}\
            \n**⌔︙آثـار ⌬ :** {keyword}\
            \n\n**⌔︙تـم حفظ الرسـالة التاليـة ڪردّ على الكلمـة في الدردشـة، يرجـى عـدم حذفهـا ✻**",
            )
            msg_o = await new_handler.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=new_handler.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                new_handler,
                "**⌔︙ لحفـظ الوسائـط ڪرد يتوجـب تعييـن - PRIVATE_GROUP_BOT_API_ID. 💡**",
            )
            return
    elif new_handler.reply_to_msg_id and not string:
        rep_msg = await new_handler.get_reply_message()
        string = rep_msg.text
    success = "**⌔︙تـم حفـظ الـرد {} بنجـاح ✓**"
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "added"))
    remove_filter(str(new_handler.chat_id), keyword)
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "Updated"))
    await edit_or_reply(new_handler, f"**⌔︙ حـدث خطـأ عنـد تعييـن الـردّ ✕ :** {keyword}")


@iqthon.on(admin_cmd(pattern="جميع الردود(?: |$)(.*)"))    
async def on_snip_list(event):
    "⌔︙لإظهـار جميع الـردود لهـذه الدردشـة ⎙"
    OUT_STR = "**⌔︙لايوجـد أيّ رد في هـذه الدردشـة  ✕**"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "**⌔︙ لايوجـد أيّ رد في هـذه الدردشـة  ✕**":
            OUT_STR = "**⌔︙الـردود المتوفـرة في هـذه الدردشـة ⎙ :** \n"
        OUT_STR += "▷  `{}`\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="**⌔︙الـردود المتاحـة في الدردشـة الحاليـة ⎙ **",
        file_name="filters.text",
    )

@iqthon.on(admin_cmd(pattern="مسح رد ([\s\S]*)")) 
async def remove_a_filter(r_handler):
    "⌔︙مسح رد الڪلمـة المحـددة ✕"
    filt = r_handler.pattern_match.group(1)
    if not remove_filter(r_handler.chat_id, filt):
        await r_handler.edit("**⌔︙ الـرد  {}  غيـر موجـود ❗️**".format(filt))
    else:
        await r_handler.edit("**⌔︙تـم حـذف الـردّ  {}  بنجـاح ✓**".format(filt))

@iqthon.on(admin_cmd(pattern="مسح جميع الردود(?: |$)(.*)"))    
async def on_all_snip_delete(event):
    "⌔︙ لحـذف جميـع ردود المجموعـة 💡"
    filters = get_filters(event.chat_id)
    if filters:
        remove_all_filters(event.chat_id)
        await edit_or_reply(event, f"**⌔︙تـم حـذف ردود الدردشـة الحاليـة بنجـاح ✓**")
    else:
        await edit_or_reply(event, f"**⌔︙لايوجـد أيّ رد في هـذه المجموعـة ✕**")

@iqthon.on(admin_cmd(pattern="تكلم(?:\s|$)([\s\S]*)"))    
async def _(event):
    "text to speech command"
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    reply_to_id = await reply_id(event)
    if ";" in input_str:
        lan, text = input_str.split(";")
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    else:
        if not input_str:
            return await edit_or_reply(event, "**⌔︙  عـذرا هـذا النص خـطأ **")
        text = input_str
        lan = "en"
    catevent = await edit_or_reply(event, "**⌔︙ يـتم الـتسجيل أنتـظر **")
    text = deEmojify(text.strip())
    lan = lan.strip()
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    required_file_name = "./temp/" + "voice.ogg"
    try:
        
        tts = gTTS(text, lang=lan)
        tts.save(required_file_name)
        command_to_execute = [
            "ffmpeg",
            "-i",
            required_file_name,
            "-map",
            "0:a",
            "-codec:a",
            "libopus",
            "-b:a",
            "100k",
            "-vbr",
            "on",
            required_file_name + ".opus",
        ]
        try:
            t_response = subprocess.check_output(
                command_to_execute, stderr=subprocess.STDOUT
            )
        except (subprocess.CalledProcessError, NameError, FileNotFoundError) as exc:
            await catevent.edit(str(exc))
            # continue sending required_file_name
        else:
            os.remove(required_file_name)
            required_file_name = required_file_name + ".opus"
        end = datetime.now()
        ms = (end - start).seconds
        await event.client.send_file(
            event.chat_id,
            required_file_name,
            reply_to=reply_to_id,
            allow_cache=False,
            voice_note=True,
        )
        os.remove(required_file_name)
        await edit_delete(
            catevent,
            "**⌔︙ النـص الـذي اخـترتـة  {} في هـذا البـصمة  خـلال 🔎 {} ثـانيـة 🔩".format(text[0:20], ms),
        )
    except Exception as e:
        await edit_or_reply(catevent, f"**⌔︙ عـذرا هنـاك خطـأ هـوة 🚫 :**\n`{str(e)}`")
@iqthon.on(admin_cmd(pattern="تحذير تكرار(?:\s|$)([\s\S]*)"))
async def _(event):
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "⌔︙جـاري تحديـث إعـدادات الـ كملها ↯")
    await asyncio.sleep(2)
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit(f"⌔︙تم تحديـث تحذير تكرار إلى : {input_str} في الدردشـة الحاليـة ⌂")
    except Exception as e:
        await event.edit(str(e))
@iqthon.on(admin_cmd(pattern="ترجمه ([\s\S]*)"))
async def _(event):
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        return await edit_delete(
            event, "**⌔︙ للترجمه يجـب الـرد على الرساله واكتب .ترجمه ar**", time=5
        )
    text = deEmojify(text.strip())
    lan = lan.strip()
    Translator()
    try:
        translated = await getTranslate(text, dest=lan)
        after_tr_text = translated.text
        output_str = f"**⌔︙ تمت الترجمه مـن  :** {LANGUAGES[translated.src].title()}\n **⌔︙ الـى ** {LANGUAGES[lan].title()} \
                \n\n{after_tr_text}"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, f"**خـطأ:**\n`{str(exc)}`", time=5)
@iqthon.on(admin_cmd(pattern="تاريخ الرساله(?: |$)(.*)"))    
async def _(event):
    "To get date and time of message when it posted."
    reply = await event.get_reply_message()
    if reply:
        try:
            result = reply.fwd_from.date
        except Exception:
            result = reply.date
    else:
        result = event.date
    await edit_or_reply(
        event, f"**هذا تاريخ الرساله والوقت  👁‍🗨 :** `{yaml_format(result)}`"
    )
