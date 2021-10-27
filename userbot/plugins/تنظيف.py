import re
from asyncio import sleep

from telethon.errors import rpcbaseerrors
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterEmpty,
    InputMessagesFilterGeo,
    InputMessagesFilterGif,
    InputMessagesFilterMusic,
    InputMessagesFilterPhotos,
    InputMessagesFilterRoundVideo,
    InputMessagesFilterUrl,
    InputMessagesFilterVideo,
    InputMessagesFilterVoice,
)

from userbot import iqthon

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID



purgelist = {}

purgetype = {
    "a": InputMessagesFilterVoice,
    "f": InputMessagesFilterDocument,
    "g": InputMessagesFilterGif,
    "i": InputMessagesFilterPhotos,
    "l": InputMessagesFilterGeo,
    "m": InputMessagesFilterMusic,
    "r": InputMessagesFilterRoundVideo,
    "t": InputMessagesFilterEmpty,
    "u": InputMessagesFilterUrl,
    "v": InputMessagesFilterVideo,
    
}


@iqthon.on(admin_cmd(pattern="مسح(\s*| \d+)$"))
async def iq(event):
    input_str = event.pattern_match.group(1).strip()
    msg_src = await event.get_reply_message()
    if msg_src:
        if input_str and input_str.isnumeric():
            await event.delete()
            await sleep(int(input_str))
            try:
                await msg_src.delete()
                if BOTLOG:
                    await event.client.send_message(BOTLOG_CHATID, "**⌔︙ حـذف الـرسائل 🗳️  \n ⌔︙ تـم حـذف الـرسالة بـنجاح ✅**")
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await event.client.send_message(BOTLOG_CHATID, "**⌔︙عـذرا لايـمكن الـحذف بـدون  صلاحيـات ألاشـراف ⚜️**")
        elif input_str:
            if not input_str.startswith("var"):
                await edit_or_reply(event, "**⌔︙ عـذرا الـرسالة غيـر موجـودة ❌**")
        else:
            try:
                await msg_src.delete()
                await event.delete()
                if BOTLOG:
                    await event.client.send_message(BOTLOG_CHATID, "**⌔︙ حـذف الـرسائل 🗳️  \n ⌔︙ تـم حـذف الـرسالة بـنجاح ✅**")
            except rpcbaseerrors.BadRequestError:
                await edit_or_reply(event, "**⌔︙ عـذرا  لا استـطيع حـذف الرسـالة. ⁉️**")
    elif not input_str:
        await event.delete()


@iqthon.on(admin_cmd(pattern="حذف رسائلي(?: |$)(.*)"))
async def purgeme(event):
    message = event.text
    count = int(message[9:])
    i = 1
    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await event.client.send_message(event.chat_id, "**⌔︙ تـم الأنتـهاء من التـنظيف ✅**  \n ⌔︙ لقـد  تـم حـذف \n  ⌔︙ عـدد  **" + str(count) + "** من الـرسائـل 🗑️**")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**⌔︙ تـم الأنتـهاء من التـنظيف ✅**  \n ⌔︙ لقـد  تـم حـذف \n  ⌔︙ عـدد  **" + str(count) + "** من الـرسائـل 🗑️**")
    await sleep(5)
    await smsg.delete()

@iqthon.on(admin_cmd(pattern="تنظيف(?:\s|$)([\s\S]*)"))
async def fastpurger(event):  # sourcery no-metrics
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    input_str = event.pattern_match.group(1)
    ptype = re.findall(r"-\w+", input_str)
    try:
        p_type = ptype[0].replace("-", "")
        input_str = input_str.replace(ptype[0], "").strip()
    except IndexError:
        p_type = None
    error = ""
    result = ""
    await event.delete()
    reply = await event.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            if p_type is not None:
                for ty in p_type:
                    if ty in purgetype:
                        async for msg in event.client.iter_messages(
                            event.chat_id,
                            limit=int(input_str),
                            offset_id=reply.id - 1,
                            reverse=True,
                            filter=purgetype[ty],
                        ):
                            count += 1
                            msgs.append(msg)
                            if len(msgs) == 50:
                                await event.client.delete_messages(chat, msgs)
                                msgs = []
                        if msgs:
                            await event.client.delete_messages(chat, msgs)
                    elif ty == "s":
                        error += f"\n**⌔︙ هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
                    else:
                        error += f"\n\n⌔︙ `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
            else:
                count += 1
                async for msg in event.client.iter_messages(
                    event.chat_id,
                    limit=(int(input_str) - 1),
                    offset_id=reply.id,
                    reverse=True,
                ):
                    msgs.append(msg)
                    count += 1
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
        elif input_str and p_type is not None:
            if p_type == "s":
                try:
                    cont, inputstr = input_str.split(" ")
                except ValueError:
                    cont = "error"
                    inputstr = input_str
                cont = cont.strip()
                inputstr = inputstr.strip()
                if cont.isnumeric():
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        limit=int(cont),
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=inputstr,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                else:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=input_str,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            else:
                error += f"\n⌔︙ `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :** "
        elif input_str:
            error += f"\n⌔︙ **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
        elif p_type is not None:
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        min_id=event.reply_to_msg_id - 1,
                        filter=purgetype[ty],
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                else:
                    error += f"\n⌔︙ `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
        else:
            async for msg in event.client.iter_messages(
                chat, min_id=event.reply_to_msg_id - 1
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
    elif p_type is not None and input_str:
        if p_type != "s" and input_str.isnumeric():
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id, limit=int(input_str), filter=purgetype[ty]
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                elif ty == "s":
                    error += f"\n**⌔︙ لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه 🔎**"
                else:
                    error += f"\n⌔︙ `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
        elif p_type == "s":
            try:
                cont, inputstr = input_str.split(" ")
            except ValueError:
                cont = "error"
                inputstr = input_str
            cont = cont.strip()
            inputstr = inputstr.strip()
            if cont.isnumeric():
                async for msg in event.client.iter_messages(
                    event.chat_id, limit=int(cont), search=inputstr
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            else:
                async for msg in event.client.iter_messages(
                    event.chat_id, search=input_str
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
        else:
            error += f"\n⌔︙ `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
    elif p_type is not None:
        for ty in p_type:
            if ty in purgetype:
                async for msg in event.client.iter_messages(
                    event.chat_id, filter=purgetype[ty]
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            elif ty == "s":
                error += f"\n**⌔︙ لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه 🔎**"
            else:
                error += f"\n⌔︙ `{ty}`  **هنـاك خطـا فـي تركـيب الجمـلة 🔩 :**"
    elif input_str.isnumeric():
        async for msg in event.client.iter_messages(chat, limit=int(input_str) + 1):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
        if msgs:
            await event.client.delete_messages(chat, msgs)
    else:
        error += "\n**⌔︙ لم يتـم تحـديد الرسـالة أرسل  (.قائمة الاوامر ) و رؤية اوامر التنظيف  📌**"
    if msgs:
        await event.client.delete_messages(chat, msgs)
    if count > 0:
        result += "⌔︙ تـم الأنتـهاء من التـنظيف السـريع  ✅  \n ⌔︙ لقـد  تـم حـذف \n  ⌔︙ عـدد  " + str(count) + " من الـرسائـل 🗑️"
    if error != "":
        result += f"\n\n**⌔︙عـذرا هنـاك خطـأ ❌:**{error}"
    if result == "":
        result += "**⌔︙ لا تـوجد رسـائل لـتنظيفها ♻️**"
    hi = await event.client.send_message(event.chat_id, result)
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, f"**⌔︙ حـذف الـرسائل 🗳️** \n{result}")
    await sleep(5)
    await hi.delete()

@iqthon.on(admin_cmd(pattern="upurge( -a)?(?:\s|$)([\s\S]*)"))
async def fast_purger(event):  # sourcery no-metrics
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    ptype = re.findall(r"-\w+", input_str)
    try:
        p_type = ptype[0].replace("-", "")
        input_str = input_str.replace(ptype[0], "").strip()
    except IndexError:
        p_type = None
    error = ""
    result = ""
    await event.delete()
    reply = await event.get_reply_message()
    if not reply or reply.sender_id is None:
        return await edit_delete(event, "**Error**\n__This cmd Works only if you reply to user message.__")
    if not flag:
        if input_str and p_type == "s":
            async for msg in event.client.iter_messages(
                event.chat_id,
                search=input_str,
                from_user=reply.sender_id,
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str and input_str.isnumeric():
            async for msg in event.client.iter_messages(
                event.chat_id,
                limit=int(input_str),
                offset_id=reply.id - 1,
                reverse=True,
                from_user=reply.sender_id,
            ):
                msgs.append(msg)
                count += 1
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
        elif input_str:
            error += f"\n• `.upurge {input_str}` تركيب جملة غير صالح ، حاول مرة أخرى"
        else:
            async for msg in event.client.iter_messages(
                chat,
                min_id=event.reply_to_msg_id - 1,
                from_user=reply.sender_id,
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
    elif input_str.isnumeric():
        async for msg in event.client.iter_messages(chat, limit=int(input_str),
            from_user=reply.sender_id,
        ):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
    else:
        async for msg in event.client.iter_messages(chat,
            from_user=reply.sender_id,
        ):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
    if msgs:
        await event.client.delete_messages(chat, msgs)
    if count > 0:
        result += "اكتمل المسح السريع! \n تم الإزالة" + str(count) + "رسائل"
    if error != "":
        result += f"\n\n**خطأ :**{error}"
    if result == "":
        result += "**لا توجد رسائل لحذفها**."
    hi = await event.client.send_message(event.chat_id, result)
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, f"#UPURGE \n{result}")
    await sleep(5)
    await hi.delete()
