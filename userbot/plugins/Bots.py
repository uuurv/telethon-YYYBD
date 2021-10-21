import re
import asyncio
from telethon import events
from asyncio.exceptions import TimeoutError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ExportChatInviteRequest
from userbot import iqthon
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import get_user_from_event, sanga_seperator
from ..helpers.utils import _format
IQMOG = re.compile(
    "["
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
    """قم بإزالة الرموز التعبيرية """
    return re.sub(IQMOG, "", inputString)
@iqthon.on(admin_cmd(pattern="اكس او(?: |$)(.*)"))
async def iq(SLQ):
    kn = SLQ.pattern_match.group(1)
    if not kn:
        if SLQ.is_reply:
            (await SLQ.get_reply_message()).message

            return
    LLL5L = await bot.inline_query("xobot", f"{(iqtfy(kn))}")
    await LLL5L[0].click(
        SLQ.chat_id,
        reply_to=SLQ.reply_to_msg_id,
        silent=True if SLQ.is_reply else False,
        hide_via=True,
    )
@iqthon.on(admin_cmd(pattern="همسه ?(.*)"))
async def iq(SLQ):
    if SLQ.fwd_from:
        return
    kkno = SLQ.pattern_match.group(1)
    donttag = "@whisperBot"
    if SLQ.reply_to_msg_id:
        await SLQ.get_reply_message()
    l5 = await bot.inline_query(donttag, kkno)
    await l5[0].click(SLQ.chat_id)
    await SLQ.delete()
@iqthon.on(admin_cmd(pattern="فحص الحظر ?(.*)"))
async def iq(SLQ):
    await SLQ.edit("جاري الفحص")
    async with bot.conversation("@SpamBot") as l5:
        try:
            dontTag = l5.wait_event(
                events.NewMessage(incoming=True, from_users=178220800)
            )
            await l5.send_message("/start")
            dontTag = await dontTag
            await bot.send_read_acknowledge(l5.chat_id)
        except YouBlockedUserError:
            await SLQ.edit("**قم بفك حظر @SpamBot للاكمال**")
            return
        await SLQ.edit(f"~ {dontTag.message.message}")    
@iqthon.on(admin_cmd(pattern="بي دي اف ?(.*)"))
async def _(event):
    if not event.reply_to_msg_id:
        return await event.edit("**الرجاء الرد على أي نص**")
    reply_message = await event.get_reply_message()
    chat = "@office2pdf_bot"
    await event.edit("**جاري تحويل إلى PDF...**")
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
                await event.edit("**قم بفك الحظر من البوت : @office2pdf_bot **")
                return
            await event.client.send_message(event.chat_id, pdf)
            await event.client.delete_messages(
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
                ],
            )
            await event.delete()
    except TimeoutError:
        return await event.edit("**هناك خطا نعتذر**") 
@iqthon.on(admin_cmd(pattern="ملصقي ?(.*)"))
async def iq(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_delete(event, "**الرجاء الرد على الرسالة**")
        return
    reply_message = await event.get_reply_message()
    warna = event.pattern_match.group(1)
    chat = "@QuotLyBot"
    await edit_or_reply(event, "**جاري...**")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            first = await conv.send_message(f"/start")
            ok = await conv.get_response()
            await asyncio.sleep(2)
            second = await bot.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("**قم بفك الحظر من البوت : @QuotLyBot **")
            return
        if response.text.startswith("Hi!"):
            await edit_or_reply(
                event, "**الرجاء تعطيل إعادة توجيه إعدادات الخصوصية الخاصة بك**"
            )
        else:
            await event.delete()
            await bot.forward_messages(event.chat_id, response.message)
    await bot.delete_messages(conv.chat_id, [first.id, ok.id, second.id, response.id])
@iqthon.on(admin_cmd(pattern="اسم الاغنيه ?(.*)"))
async def iq(event):
    if not event.reply_to_msg_id:
        return await event.edit("**الرجاء الرد على الرسالة**")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    try:
        async with event.client.conversation(chat) as conv:
            try:
                await event.edit("**التعرف على الأغاني...**")
                start_msg = await conv.send_message("/start")
                await conv.get_response()
                send_audio = await conv.send_message(reply_message)
                check = await conv.get_response()
                if not check.text.startswith("Audio received"):
                    return await event.edit(
                        "**حدث خطأ أثناء تحديد الأغنية. حاول استخدام رسالة صوتية تتراوح مدتها من 5 إلى 10 ثوانٍ.**")
                await event.edit("**انتظر لحظة...**")
                result = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("**قم بفك الحظر من البوت : @auddbot dan coba lagi:")
                return
            namem = f"**إسم الأغنية : {result.text.splitlines()[0]}**\
        \n\n**تفاصيل : {result.text.splitlines()[2]}**"
            await event.edit(namem)
            await event.client.delete_messages(
                conv.chat_id, [start_msg.id, send_audio.id, check.id, result.id]
            )
    except TimeoutError:
        return await event.edit(
            "**هناك خطا نعتذر**")
@iqthon.on(admin_cmd(pattern="انشاء بريد(?: |$)(.*)"))
async def _(event):
    chat = "@TempMailBot"
    geez = await event.edit("**جاري انشاء بريد ...**")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(
                incoming=True,
                from_users=220112646
            )
            )
            await conv.send_message("/start")
            await asyncio.sleep(1)
            await conv.send_message("/create")
            response = await response
            iqthonbot = ((response).reply_markup.rows[2].buttons[0].url)
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await geez.edit("**قم بفتح الحظر عن : @TempMailBot للأستمرار بانشاء البريدات**")
            return
        await event.edit(f"بريدك الخاص هوه : ~ `{response.message.message}`\n[انقر هنا للتحقق من رسائل بريدك]({iqthonbot})")
@iqthon.on(admin_cmd(pattern="سجل الاسماء(ألف)?(?:\s|$)([\s\S]*)"))
async def _(event):  # sourcery no-metrics
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete(
            event,
            "**⌔︙قم بالـرد على رسالـة لمستخـدم للحصـول على إسمـه/سجل يوزراتـه أو قم بإعطـاء آيـدي المستخـدم/يـوزر المستخـدم ✦**",
        )
    user, rank = await get_user_from_event(event, secondgroup=True)
    if not user:
        return
    uid = user.id
    chat = "@SangMataInfo_bot"
    catevent = await edit_or_reply(event, "**⌔︙جـاري المعالجـة ↯**")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/search_id {uid}")
        except YouBlockedUserError:
            await edit_delete(catevent, "**⌔︙قم بإلغـاء حظـر @Sangmatainfo_bot ثم حـاول !!**")
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await event.client.send_read_acknowledge(conv.chat_id)
    if not responses:
        await edit_delete(catevent, "**⌔︙لا يستطيـع البـوت جلـب النتائـج ⚠️**")
    if "No records found" in responses:
        await edit_delete(catevent, "**⌔︙المستخـدم ليـس لديـه أيّ سجـل ✕**")
    names, usernames = await sanga_seperator(responses)
    cmd = event.pattern_match.group(1)
    sandy = None
    check = usernames if cmd == "u" else names
    for i in check:
        if sandy:
            await event.reply(i, parse_mode=_format.parse_pre)
        else:
            sandy = True
            await catevent.edit(i, parse_mode=_format.parse_pre)
