import re
import asyncio
import calendar
import json
import os
from telethon import events
from asyncio.exceptions import TimeoutError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ExportChatInviteRequest
from userbot import iqthon
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import get_user_from_event, sanga_seperator
from bs4 import BeautifulSoup
from ..helpers.utils import _format
from datetime import datetime
from urllib.parse import quote
import barcode
import qrcode
import requests
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from PIL import Image, ImageColor
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import iqthon
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import AioHttp
from ..helpers.utils import _catutils, _format, reply_id
LOGS = logging.getLogger(__name__)
IQMOG = re.compile(
    "[" #Telethon IQ
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental aliosamg
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+")
def iqtfy(inputString: str) -> str:
    return re.sub(IQMOG, "", inputString)
@iqthon.on(admin_cmd(pattern="اكس او(?: |$)(.*)"))
async def iq(iqthon):
    kn = iqthon.pattern_match.group(1)
    if not kn:
        if iqthon.is_reply:
            (await iqthon.get_reply_message()).message

            return
    LLL5L = await bot.inline_query("xobot", f"{(iqtfy(kn))}")
    await LLL5L[0].click(
        iqthon.chat_id,
        reply_to=iqthon.reply_to_msg_id,
        silent=True if iqthon.is_reply else False,
        hide_via=True)
@iqthon.on(admin_cmd(pattern="همسه ?(.*)"))
async def iq(iqthon):
    if iqthon.fwd_from:
        return
    kkno = iqthon.pattern_match.group(1)
    donttag = "@whisperBot"
    if iqthon.reply_to_msg_id:
        await iqthon.get_reply_message()
    l5 = await bot.inline_query(donttag, kkno)
    await l5[0].click(iqthon.chat_id)
    await iqthon.delete()
@iqthon.on(admin_cmd(pattern="حالتي ?(.*)"))
async def iq(iqthon):
    await iqthon.edit("جاري الفحص")
    async with bot.conversation("@SpamBot") as l5:
        try:
            dontTag = l5.wait_event(
                events.NewMessage(incoming=True, from_users=178220800))
            await l5.send_message("/start")
            dontTag = await dontTag
            await bot.send_read_acknowledge(l5.chat_id)
        except YouBlockedUserError:
            await iqthon.edit("**قم بفك حظر @SpamBot للاكمال**")
            return
        await iqthon.edit(f"~ {dontTag.message.message}")    
@iqthon.on(admin_cmd(pattern="بي دي اف ?(.*)"))
async def _(iqthon):
    if not iqthon.reply_to_msg_id:
        return await iqthon.edit("**الرجاء الرد على أي نص**")
    reply_message = await iqthon.get_reply_message()
    chat = "@office2pdf_bot"
    await iqthon.edit("**جاري تحويل إلى PDF...**")
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                msg = await conv.send_message(reply_message)
                convert = await conv.send_message("/ready2conv")
                cnfrm = await conv.get_response()
                editfilename = await conv.send_message("نعم")
                enterfilename = await conv.get_response()
                filename = await conv.send_message("IQTHON")
                started = await conv.get_response()
                pdf = await conv.get_response()
                """iq"""
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await iqthon.edit("**قم بفك الحظر من البوت : @office2pdf_bot **")
                return
            await iqthon.client.send_message(event.chat_id, pdf)
            await iqthon.client.delete_messages(
                conv.chat_id,
                [
                    msg_start.id,
                    response.id,
                    msg.id,
                    started.id,
                    filename.id,
                    editfilename.id,
                    enterfilename.id,
                    cnfrm.id,
                    pdf.id,
                    convert.id,
                ],)
            await iqthon.delete()
    except TimeoutError:
        return await iqthon.edit("**هناك خطا نعتذر**") 
@iqthon.on(admin_cmd(pattern="ملصقي ?(.*)"))
async def iq(iqthon):
    if iqthon.fwd_from:
        return
    if not iqthon.reply_to_msg_id:
        await edit_delete(iqthon, "**الرجاء الرد على الرسالة**")
        return
    reply_message = await iqthon.get_reply_message()
    warna = iqthon.pattern_match.group(1)
    chat = "@QuotLyBot"
    await edit_or_reply(iqthon, "**جاري...**")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(incoming=True, from_users=1031952739))
            first = await conv.send_message(f"/start")
            ok = await conv.get_response()
            await asyncio.sleep(2)
            second = await bot.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await iqthon.reply("**قم بفك الحظر من البوت : @QuotLyBot **")
            return
        if response.text.startswith("Hi!"):
            await edit_or_reply(
                iqthon, "**الرجاء تعطيل إعادة توجيه إعدادات الخصوصية الخاصة بك**")
        else:
            await iqthon.delete()
            await bot.forward_messages(iqthon.chat_id, response.message)
    await bot.delete_messages(conv.chat_id, [first.id, ok.id, second.id, response.id])
@iqthon.on(admin_cmd(pattern="اسم الاغنيه ?(.*)"))
async def iq(iqthon):
    if not iqthon.reply_to_msg_id:
        return await iqthon.edit("**الرجاء الرد على الرسالة**")
    reply_message = await iqthon.get_reply_message()
    chat = "@auddbot"
    try:
        async with iqthon.client.conversation(chat) as conv:
            try:
                await iqthon.edit("**التعرف على الأغاني...**")
                start_msg = await conv.send_message("/start")
                await conv.get_response()
                send_audio = await conv.send_message(reply_message)
                check = await conv.get_response()
                if not check.text.startswith("Audio received"):
                    return await iqthon.edit(
                        "**حدث خطأ أثناء تحديد الأغنية. حاول استخدام رسالة صوتية تتراوح مدتها من 5 إلى 10 ثوانٍ.**")
                await iqthon.edit("**انتظر لحظة...**")
                result = await conv.get_response()
                await iqthon.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await iqthon.edit("**قم بفك الحظر من البوت : @auddbot dan coba lagi:")
                return
            namem = f"**إسم الأغنية : {result.text.splitlines()[0]}**\
        \n\n**تفاصيل : {result.text.splitlines()[2]}**"
            await iqthon.edit(namem)
            await iqthon.client.delete_messages(                conv.chat_id, [start_msg.id, send_audio.id, check.id, result.id]            )
    except TimeoutError:
        return await iqthon.edit(            "**هناك خطا نعتذر**")
@iqthon.on(admin_cmd(pattern="انشاء بريد(?: |$)(.*)"))
async def _(iqthon):
    chat = "@TempMailBot"
    geez = await iqthon.edit("**جاري انشاء بريد ...**")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(                incoming=True,                from_users=220112646            )            )            
            await conv.send_message("/start")
            await asyncio.sleep(1)
            await conv.send_message("/create")
            response = await response
            iqthonbot = ((response).reply_markup.rows[2].buttons[0].url)
            await iqthon.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await geez.edit("**قم بفتح الحظر عن : @TempMailBot للأستمرار بانشاء البريدات**")
            return
        await iqthon.edit(f"بريدك الخاص هوه : ~ `{response.message.message}`\n[انقر هنا للتحقق من رسائل بريدك]({iqthonbot})")
@iqthon.on(admin_cmd(pattern="سجل الاسماء(ألف)?(?:\s|$)([\s\S]*)"))
async def _(iqthon):  # sourcery no-metrics
    input_str = "".join(iqthon.text.split(maxsplit=1)[1:])
    reply_message = await iqthon.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete(iqthon, "**⎈ ⦙ قم بالـرد على رسالـة لمستخـدم للحصـول على إسمـه/سجل يوزراتـه أو قم بإعطـاء آيـدي المستخـدم/يـوزر المستخـدم ✦**")
    user, rank = await get_user_from_event(iqthon, secondgroup=True)
    if not user:
        return
    uid = user.id
    chat = "@SangMataInfo_bot"
    iqevent = await edit_or_reply(iqthon, "**⎈ ⦙ جـاري المعالجـة ↯**")
    async with iqthon.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/search_id {uid}")
        except YouBlockedUserError:
            await edit_delete(iqthon, "**⎈ ⦙ قم بإلغـاء حظـر @Sangmatainfo_bot ثم حـاول !!**")
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await iqthon.client.send_read_acknowledge(conv.chat_id)
    if not responses:
        await edit_delete(iqthon, "**⎈ ⦙ لا يستطيـع البـوت جلـب النتائـج ⚠️**")
    if "No records found" in responses:
        await edit_delete(iqthon, "**⎈ ⦙ المستخـدم ليـس لديـه أيّ سجـل ✕**")
    names, usernames = await sanga_seperator(responses)
    cmd = iqthon.pattern_match.group(1)
    sandy = None
    check = usernames if cmd == "u" else names
    for i in check:
        if sandy:
            await iqthon.reply(i, parse_mode=_format.parse_pre)
        else:
            sandy = True
            await iqevent.edit(i, parse_mode=_format.parse_pre)
@iqthon.on(admin_cmd(pattern="تيك توك(?: |$)(.*)"))
async def _(iqthon):
    reply_message = await iqthon.get_reply_message()
    if not reply_message:
        await edit_or_reply(iqthon, "**⎈ ⦙  الرد على الرابط.**")
        return
    if not reply_message.text:
        await edit_or_reply(iqthon, "**⎈ ⦙  الرد على الرابط.**")
        return
    chat = "@fs0bot"
    iqevent = await edit_or_reply(iqthon, "**⎈ ⦙  جاري تحميل الرابط**")
    async with iqthon.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(incoming=True, from_users=1354606430))
            await iqthon.client.forward_messages(chat, reply_message)
            response = await response
            await iqthon.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await iqevent.edit("**⎈ ⦙  فك الحظر من البوت : @fs0bot**")
            return
        if response.text.startswith("؟"):
            await iqevent.edit("?")
        else:
            await iqevent.delete()
            await iqthon.client.send_message(iqthon.chat_id, response.message)
@iqthon.on(admin_cmd(pattern="زخرفه ?(.*)"))
async def _IQ(iqthon):
    if event.fwd_from:
        return 
    if not iqthon.reply_to_msg_id:
       await iqthon.edit("**⎈ ⦙ الرجاء الرد على الرسالة**")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await iqthon.edit("**⎈ ⦙ الرجاء الرد على الرسالة**")
       return
    chat = '@zagtelethonbot'
    sender = reply_message.sender
    if reply_message.sender.bot:
       await iqthon.edit("**⎈ ⦙ الرجاء الرد على الرسالة**")
       return
    await iqthon.edit("**⎈ ⦙ جاري الزخرفه الانكليزيه ...**")
    async with iqthon.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1943073737))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await iqthon.reply("**⎈ ⦙ قم بفك الحظر من البوت : @zagtelethonbot **")
              return
          if response.text.startswith("Hi!"):
             await iqthon.edit("**⎈ ⦙ قم بفك الحظر من البوت : @zagtelethonbot **")
          else: 
             await iqthon.delete()
             await iqthon.client.send_message(iqthon.chat_id, response.message)
@iqthon.on(admin_cmd(pattern="كشف الفايروسات( -i)?$"))    
async def _IQ(iqthon):
    input_str = iqthon.pattern_match.group(1)
    if not iqthon.reply_to_msg_id:
        return await edit_or_reply(iqthon, "الرد على أي رسالة مستخدم.")
    reply_message = await iqthon.get_reply_message()
    if not reply_message.media:
        return await edit_or_reply(iqthon, "الرد على الملف")
    chat = "@VS_Robot"
    IQevent = await edit_or_reply(iqthon, " انتضر قليلا")
    async with iqthon.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await iqthon.client.forward_messages(chat, reply_message)
            response1 = await conv.get_response()
            if response1.text:
                await iqthon.client.send_read_acknowledge(conv.chat_id)
                return await IQevent.edit(response1.text, parse_mode=_format.parse_pre)
            await conv.get_response()
            await iqthon.client.send_read_acknowledge(conv.chat_id)
            response3 = await conv.get_response()
            response4 = await conv.get_response()
            await iqthon.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await IQevent.edit("قم بفتح الحظر من : @VS_Robot")
        if not input_str:
            return await edit_or_reply(IQevent, response4.text)
        await IQevent.delete()
        await iqthon.client.send_file(iqthon.chat_id, response3.media, reply_to=(await reply_id(iqthon)))
@iqthon.on(admin_cmd(pattern="تقويم ([\s\S]*)"))    
async def _iq(iqthon):
    input_str = iqthon.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) != 2:
        return await edit_delete(iqthon, "**تصحيح قم بكتابه الأمر هكذا : **`.تقويم السنه الشهر `", 5)

    yyyy = input_sgra[0]
    mm = input_sgra[1]
    try:
        output_result = calendar.month(int(yyyy.strip()), int(mm.strip()))
        await edit_or_reply(iqthon, f"```{output_result}```")
    except Exception as e:
        await edit_delete(iqthon, f"                                              **خطأ :**\n`{str(e)}`                       ", 5)
