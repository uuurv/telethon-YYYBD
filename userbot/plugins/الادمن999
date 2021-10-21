from asyncio import sleep
from telethon import functions
from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)

from userbot import iqthon

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID

PP_TOO_SMOL = "**⌔︙الصورة صغيرة جدًا  📸** ."
PP_ERROR = "**⌔︙فشل أثناء معالجة الصورة  📵** ."
NO_ADMIN = "**⌔︙أنا لست مشرف هنا ** ."
NO_PERM = "**⌔︙ليس لدي أذونات كافية  🚮** ."
CHAT_PP_CHANGED = "**⌔︙تغيّرت صورة الدردشة  🌅** ."
INVALID_MEDIA = "**⌔ ︙ ملحق غير صالح  📳** ."
IMOGE_IQTHON = "⌔︙"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

plugin_category = "admin"
# ================================================


@iqthon.on(admin_cmd(pattern="حذف( صورة| -d)$"))
async def set_group_photo(event):  # sourcery no-metrics
    "⌔︙لتغيير المجموعة  ♌️"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "-s":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edit_delete(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edit_delete(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edit_delete(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edit_delete(event, PP_ERROR)
            except Exception as e:
                return await edit_delete(event, f"**⌔︙خطأ  ❌ : **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**♕︙ خطأ : **`{str(e)}`")
        process = "deleted"
        await edit_delete(event, "**⌔︙تـم حذف الـصورة بنـجاح  ✔️**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "⌔︙ صوره_المجموعة\n"
            f"⌔︙ صورة المجموعه {process} بنجاح "
            f"⌔︙ المحادثة  📜 : {event.chat.title}(`{event.chat_id}`)",
        )

async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("**⌔︙ لم يتم العثور على المجموعة او القناة**")
            return None
        except ChannelPrivateError:
            await event.reply(
                "**⌔︙ لا يمكنني استخدام الامر من الكروبات او القنوات الخاصة**"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**⌔︙ لم يتم العثور على المجموعة او القناة**")
            return None
        except (TypeError, ValueError):
            await event.reply("**⌔︙ رابط الكروب غير صحيح**")
            return None
    return chat_info


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name




@iqthon.on(admin_cmd(pattern="رفع مشرف(?: |$)(.*)"))
async def promote(event):
    "لرفع مشرف بالمجموعه"
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Admin"
    if not user:
        return
    catevent = await edit_or_reply(event, "**⌔︙يـتم الرفـع  ↗️ **")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**⌔︙تم رفعه مشرف بالمجموعه بنجاح  📤**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"⌔︙ترقية  🆙\
            \n⌔︙المستخدم  🚹 : [{user.first_name}](tg://user?id={user.id})\
            \n⌔︙المحادثة  📜 : {event.chat.title} (`{event.chat_id}`)",
        )


@iqthon.on(admin_cmd(pattern="تنزيل مشرف(?: |$)(.*)"))
async def demote(event):
    "لتنزيل من رتبة الادمن"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**⌔︙يـتم التنزيل من الاشراف  ↙️**")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "مشرف"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**⌔︙تـم تنزيله من قائمه الادمنيه بنجاح  ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"⌔︙ تنزيل_مشرف\
            \n⌔︙المستخدم  🚹 : [{user.first_name}](tg://user?id={user.id})\
            \n⌔︙المحادثة  📜 : {event.chat.title}(`{event.chat_id}`)",
        )



@iqthon.on(admin_cmd(pattern="طرد(?: |$)(.*)"))
async def endmute(event):
    "⌔︙إستخدم هذا لطرد مستخدم من المحادثة  🚷"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == 1226408155:
        return await edit_delete(event, "**⌔︙ عـذرا أنـة مبـرمج السـورس  ⚜️**")
    catevent = await edit_or_reply(event, "**⌔︙ تـم حـظره بـنجاح ✅**")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await catevent.edit(NO_PERM + f"\n{str(e)}")
    if reason:
        await catevent.edit(
            f"**⌔︙المستخدم  🚹 : [{user.first_name}](tg://user?id={user.id}) \n تم طـرده بنجاح  ✅ ** n\⌔︙ السـبب: {reason}"
        )
    else:
        await catevent.edit(f"**⌔︙المستخدم  🚹 : [{user.first_name}](tg://user?id={user.id}) \n تم طـرده بنجاح  ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "⌔︙ المطرودين\n"
            f"⌔︙ المستخدمين: [{user.first_name}](tg://user?id={user.id})\n"
            f"⌔︙المحادثة  📜 : {event.chat.title}(`{event.chat_id}`)\n",
        )


@iqthon.on(admin_cmd(pattern="تثبيت(?: |$)(.*)"))
async def pin(event):
    "⌔︙ تثبيت  📌"
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edit_delete(event, "**⌔︙يرجى الرد على الرسالة التي تريد تثبيتها 📨 **", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{str(e)}`", 5)
    await edit_delete(event, "**⌔︙تم تثبيت الرسالة بنجاح في هذه الدردشة  📌**", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"⌔︙ تثبيت  📌\
                \n⌔︙ تم تثبيت الرسالة بنجاح في الدردشة  📌\
                \n⌔︙المستخدم  🚹 : {event.chat.title}(`{event.chat_id}`)\
                \n⌔︙المحادثة  📜 : {is_silent}",
        )


@iqthon.on(admin_cmd(pattern="الغاء التثبيت(?: |$)(.*)"))
async def pin(event):
    "⌔︙لإلغاء تثبيت رسائل من المجموعة  ⚠️"
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edit_delete(
            event,
            "⌔︙ يرجى الرد على الرسالة التي تريد تثبيتها استخدم `.الغاء التثبيت للكل`  لالغاء تثبيت جميع الرسائل  📍",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "للكل":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event, "⌔︙ يرجى الرد على الرسالة التي تريد تثبيتها استخدم `.الغاء التثبيت للكل`  لالغاء تثبيت جميع الرسائل  📍", 5
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{str(e)}`", 5)
    await edit_delete(event, "**⌔︙تم الغاء التثبيت بنجاح  ✅**", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"**⌔︙ الـغاء التثبيت  ❗️ \
                \n** ⌔︙ تم بنجاح الغاء التثبيـت في الدردشة  ✅ \
                \n⌔︙الدردشـه  🔖 : {event.chat.title}(`{event.chat_id}`)",
        )


@iqthon.on(admin_cmd(pattern="جلب الاحداث(?: |$)(.*)"))
async def _iundlt(event):  # sourcery no-metrics
    "⌔︙لأخذ نظرة عن آخر الرسائل المحذوفة في المجموعة  💠"
    catevent = await edit_or_reply(event, "**⌔︙يتم البحث عن اخر الاحداث انتظر  🔍**")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**⌔︙ اخر {lim} رسائل محذوفة في هذه المجموعة  🗑 :**"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n⌔︙ {msg.old.message} \n **تم ارسالها بـواسطة  🛃** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n⌔︙ {_media_type} \n **تم ارسالها بـواسطة  🛃** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(catevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(catevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"⌔︙ {msg.old.message}\n**تم ارسالها بـواسطة  🛃** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"⌔︙ {msg.old.message}\n**تم ارسالها بـواسطة  🛃** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )


@iqthon.on(admin_cmd(pattern="حظر(?: |$)(.*)"))
async def _ban_person(event):
    "⌔︙ لحـظر شخص في كـروب مـعين"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == 1226408155:
        return await edit_delete(event, "**⌔︙ عـذرا أنـة مبـرمج السـورس  ⚜️**")
    if user.id == event.client.uid:
        return await edit_delete(event, "⌔︙ عـذرا لا تسـتطيع حـظر شـخص")
    catevent = await edit_or_reply(event, "⌔︙ تـم حـظره بـنجاح")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await catevent.edit(
            "⌔︙ ليـس لـدي جـميع الصـلاحيـات لكـن سيـبقى محـظور"
        )
    if reason:
        await catevent.edit(
            f"⌔︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n ⌔︙ تـم حـظره بنـجاح !!\n**⌔︙السبب : **`{reason}`"
        )
    else:
        await catevent.edit(
            f"⌔︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n ⌔︙ تـم حـظره بنـجاح ✅"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \nايدي الكروب(`{event.chat_id}`)\
                \nالسبـب : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \n ايـدي الكـروب: (`{event.chat_id}`)",
            )


@iqthon.on(admin_cmd(pattern="الغاء الحظر(?: |$)(.*)"))
async def nothanos(event):
    "⌔︙ لألـغاء الـحظر لـشخص في كـروب مـعين"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "⌔︙ جـار الـغاء الـحظر أنتـظر")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit(
            f"⌔︙ الـمستخدم {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم الـغاء حـظره بنـجاح "
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "⌔︙ الـغاء الـحظر \n"
                f"الـمستخدم: [{user.first_name}](tg://user?id={user.id})\n"
                f"الـدردشـة: {event.chat.title}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("⌔︙ يـبدو أن هذه الـعمليـة تم إلغاؤهـا")
    except Exception as e:
        await catevent.edit(f"**خـطأ :**\n`{e}`")


@iqthon.iq_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))

@iqthon.on(admin_cmd(pattern=r"نقل الاعظاء ?(.*)"))
async def add(addiqthon):
    klanr = await addiqthon.get_klanr()
    l5 = await addiqthon.client.get_l5()
    if not klanr.id == l5.id:
        kno = await addiqthon.reply(f"** أنتظر العمليّـة إنتظـر قليلاً  ↯**")
    else:
        kno = await addiqthon.edit(f"** أنتظر العمليّـة إنتظـر قليلاً  ↯**")
    IQTHON = await get_chatinfo(addiqthon)
    chat = await addiqthon.get_chat()
    if addiqthon.is_private:
        return await kno.edit(f"** لا يُمڪـنني إضافـة المُـستخدمين هُـنا  ✕ **\n `1- تأكد من أنك لست محظور من الاضافة  .`\n `2- تاكد ان صلاحيه اضافه الاعضاء مفتوحه .`")
    s = 0
    f = 0
    error = "None"
    await kno.edit("** أنتظر جمـع معلومـات المُـستخدمين ↯**")
    async for user in addiqthon.client.iter_participants(IQTHON.full_chat.id):
        try:
            if error.startswith("Too"):
                return (
                    await kno.edit(f"** لا يُمڪـنني إضافـة المُـستخدمين هُـنا  ✕ :**\n `1- تأكد من أنك لست محظور من الاضافة  .`\n `2- تاكد ان صلاحيه اضافه الاعضاء مفتوحه .` \n `{error}`"),)
            await addiqthon.client(functions.channels.InviteToChannelRequest(channel=chat, users=[user.id]))
            s = s + 1
            await kno.edit(f"** أنتظر عمليّـة الأضافة :**\n**  عدد الأضافات 👤 :** `{s}` \n**  خـطأ الأضافات ❄️ :** `{f}` \n")
        except Exception as e:
            error = str(e)
            f = f + 1
    return await kno.edit(f"**⌔︙ اڪتـملت الأضافـة ✅** : \n\n⌔︙ تـم بنجـاح اضافـة `{s}` \n⌔︙ خـطأ بأضافـة `{f}`")
    

