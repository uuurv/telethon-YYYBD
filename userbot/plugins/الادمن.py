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

# =================== STRINGS ============
PP_TOO_SMOL = "**⌔︙الصورة صغيرة جدًا  📸** ."
PP_ERROR = "**⌔︙فشل أثناء معالجة الصورة  📵** ."
NO_ADMIN = "**⌔︙أنا لست مشرف هنا ** ."
NO_PERM = "**⌔︙ليس لدي أذونات كافية  🚮** ."
CHAT_PP_CHANGED = "**⌔︙تغيّرت صورة الدردشة  🌅** ."
INVALID_MEDIA = "**⌔︙ملحق غير صالح  📳** ."

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


@iqthon.iq_cmd(
    pattern="حذف( صورة| -d)$",
    command=("صورة", plugin_category),
    info={
        "header": "لوضع صوره للمجموعه ",
        "description": "قم بالرد على الصوره المراد وضعها",
        "flags": {
            "ضع صوره": "لوضع صوره للمجموعة ",
            "-d": "To delete group pic",
        },
        "usage": [
            "{tr}ضع صوره <بالرد على الصوره>",
            "{tr}gpic -d",
        ],
    },
    groups_only=True,
    require_admin=True,
)
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


@iqthon.iq_cmd(
    pattern="رفع مشرف(?: |$)(.*)",
    command=("رفع مشرف", plugin_category),
    info={
        "الامر": "لرفع الشخص مشرف مع صلاحيات",
        "الشرح": "لرفع الشخص مشرف بالمجموعه قم بالرد على الشخص\
            \nNote : You need proper rights for this",
        "الاستخدام": [
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه>",
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
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


@iqthon.iq_cmd(
    pattern="تك(?: |$)(.*)",
    command=("تك", plugin_category),
    info={
        "الامر": "لتنزيل الشخص كن الاشراف",
        "الشرح": "يقوم هذا الامر بحذف جميع صلاحيات المشرف\
            \nملاحظه :**لازم تكون انت الشخص الي رفعه او تكون مالك المجموعه حتى تنزله**",
        "الاستخدام": [
            "{tr}تك <الايدي/المعرف/بالرد عليه>",
            "{tr}تك <الايدي/المعرف/بالرد عليه>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
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
    rank = "admin"
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



@iqthon.iq_cmd(
    pattern="طرد(?: |$)(.*)",
    command=("طرد", plugin_category),
    info={
        "header": "⌔︙ لطرد شخص من المجموعة ",
        "description": "Will kick the user from the group so he can join back.\
        \nNote : You need proper rights for this.",
        "usage": [
            "{tr}kick <userid/username/reply>",
            "{tr}kick <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "⌔︙إستخدم هذا لطرد مستخدم من المحادثة  🚷"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**⌔︙جاري طرد هذا الشخص من المجموعة  ❎**")
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


@iqthon.iq_cmd(
    pattern="تثبيت( بالاشعار|$)",
    command=("pin", plugin_category),
    info={
        "header": "For pining messages in chat",
        "description": "reply to a message to pin it in that in chat\
        \nNote : You need proper rights for this if you want to use in group.",
        "options": {"loud": "To notify everyone without this.it will pin silently"},
        "usage": [
            "{tr}pin <reply>",
            "{tr}pin loud <reply>",
        ],
    },
)
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


@iqthon.iq_cmd(
    pattern="الغاء التثبيت( للكل|$)",
    command=("الغاء التثبيت", plugin_category),
    info={
        "header": "For unpining messages in chat",
        "description": "reply to a message to unpin it in that in chat\
        \nNote : You need proper rights for this if you want to use in group.",
        "options": {"all": "To unpin all messages in the chat"},
        "usage": [
            "{tr}unpin <reply>",
            "{tr}unpin all",
        ],
    },
)
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


@iqthon.iq_cmd(
    pattern="الاحداث( -ر)?(?: |$)(\d*)?",
    command=("الاحداث", plugin_category),
    info={
        "header": "To get recent deleted messages in group",
        "description": "To check recent deleted messages in group, by default will show 5. you can get 1 to 15 messages.",
        "flags": {
            "u": "use this flag to upload media to chat else will just show as media."
        },
        "usage": [
            "{tr}undlt <count>",
            "{tr}undlt -u <count>",
        ],
        "examples": [
            "{tr}undlt 7",
            "{tr}undlt -u 7 (this will reply all 7 messages to this message",
        ],
    },
    groups_only=True,
    require_admin=True,
)
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
