import asyncio
import time
import os
import shutil
from datetime import datetime
from asyncio import sleep
from asyncio.exceptions import TimeoutError
from telethon import functions, types
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest, GetFullChannelRequest, GetParticipantsRequest, EditAdminRequest, EditPhotoRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest, ExportChatInviteRequest
from telethon.errors import ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError, BadRequestError, ChatAdminRequiredError, FloodWaitError, MessageNotModifiedError, UserAdminInvalidError
from telethon.errors.rpcerrorlist import YouBlockedUserError, UserAdminInvalidError, UserIdInvalidError
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.tl.types import ChatAdminRights, InputChatPhotoEmpty, MessageMediaPhoto
from telethon.tl.types import ChannelParticipantsKicked, ChannelParticipantAdmin, ChatBannedRights, ChannelParticipantCreator, ChannelParticipantsAdmins, ChannelParticipantsBots, MessageActionChannelMigrateFrom, UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently
from telethon.utils import get_display_name, get_input_location
from math import sqrt
from prettytable import PrettyTable
from emoji import emojize
from userbot import iqthon
from userbot.utils import admin_cmd
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from . import humanbytes
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event
from ..helpers import reply_id, readable_time
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..helpers import media_type
from ..helpers.google_image_download import googleimagesdownload
from ..helpers.tools import media_type
from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from ..sql_helper import no_log_pms_sql
from ..sql_helper.globals import addgvar, gvarstatus
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
KLANR_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
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
plugin_category = "utils"

TYPES = [
    "Photo",
    "Audio",
    "Video",
    "Document",
    "Sticker",
    "Gif",
    "Voice",
    "Round Video",
]

class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0
LOG_CHATS_ = LOG_CHATS()

PP_TOO_SMOL = "**⌔︙الصورة صغيرة جدًا  📸** ."
PP_ERROR = "**⌔︙فشل أثناء معالجة الصورة  📵** ."
NO_ADMIN = "**⌔︙أنا لست مشرف هنا ** ."
NO_PERM = "**⌔︙ليس لدي أذونات كافية  🚮** ."
CHAT_PP_CHANGED = "**⌔︙تغيّرت صورة الدردشة  🌅** ."
INVALID_MEDIA = "**⌔ ︙ ملحق غير صالح  📳** ."
IMOGE_IQTHON = "⌔︙"



@iqthon.on(admin_cmd(pattern=r"المحظورين?(.*)"))
async def gablist(event):
    "Shows you the list of all gbanned users by you."
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Current Gbanned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Reason None\n"
                )
    else:
        GBANNED_LIST = "no Gbanned Users (yet)"
    await edit_or_reply(event, GBANNED_LIST)

@iqthon.on(admin_cmd(pattern=r"كتم(?:\s|$)([\s\S]*)"))
async def startgmute(event):
    if event.is_private:
        await event.edit("**⌔︙ جاري الكتم**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == iqthon.uid:
            return await edit_or_reply(
                event, "**⌔︙ لا يـمكنك كتم نـفسك**"
            )
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event, "**⌔︙ غيـر قـادر عـلى جـلب مـعلومات الـشخص **"
        )
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"**⌔︙ تـم كـتم الـمستـخدم بـنجاح ✅**",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خـطأ**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"**⌔︙ تـم كـتم الـمستـخدم بـنجاح ✅**",
            )
        else:
            await edit_or_reply(
                event,
                f"**⌔︙ تـم كـتم الـمستـخدم بـنجاح ✅**",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**⌔︙ الـمستخدم** {_format.mentionuser(user.first_name ,user.id)}\n **⌔︙ تـم كتمه بنـجاح**\n **⌔︙ الدردشـة** {event.chat.title}\n"
                f"**⌔︙ السـبب:** {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**⌔︙ الـمستخدم** {_format.mentionuser(user.first_name ,user.id)} \n**⌔︙ تـم كتمه بنـجاح**",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)

@iqthon.on(admin_cmd(pattern=r"الغاء كتم(?:\s|$)([\s\S]*)"))
async def endgmute(event):
    "iqthon"
    if event.is_private:
        await event.edit("**⌔︙ قـد تـحدث بعـض الأخـطاء**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == iqthon.uid:
            return await edit_or_reply(event, "**⌔︙ لا يـمكنك كتم نـفسك**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event, "**⌔︙ غيـࢪ قـادࢪ عـلى جـلب مـعلومات الـشخص **"
        )
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(event, f"**⌔︙ هـذا الـمستخدم لـيس مكـتوم**")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خـطأ **\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"**⌔︙ تـم الـغاء كـتم الـمستـخدم بـنجاح**",
            )
        else:
            await edit_or_reply(
                event,
                f"**⌔︙ تـم الـغاء كـتم الـمستـخدم بـنجاح**",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔︙ الـغاء الكـتم**\n"
                f"**⌔︙ الـمستخدم :* {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**⌔︙ السبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                 "**⌔︙ الـغاء الكـتم**\n"
                f"**⌔︙ المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )

@iqthon.iq_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()

@iqthon.on(admin_cmd(pattern=r"المشرفين(?: |$)(.*)"))
async def _(event):
    "لإظهـار قائمـة المشرفيـن  ✪"
    mentions = "**⌔︙ مشرفيـن هـذه المجموعـة  ✪**: \n"
    reply_message = await reply_id(event)
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if input_str:
        mentions = f"**⌔︙مشرفيـن فـي → :** {input_str} **مـن المجموعـات ⌂ :** \n"
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, str(e))
    else:
        chat = to_write_chat
        if not event.is_group:
            return await edit_or_reply(event, "**⌔︙ هـذه ليسـت مجموعـة ✕**")
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if not x.deleted and isinstance(x.participant, ChannelParticipantCreator):
                mentions += "\n - [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
        mentions += "\n"
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if x.deleted:
                mentions += "\n `{}`".format(x.id)
            else:
                if isinstance(x.participant, ChannelParticipantAdmin):
                    mentions += "\n- [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_message)
    await event.delete()


@iqthon.on(admin_cmd(pattern=r"البوتات?(.*)"))
async def _(event):
    "⌔︙ لإظهـار قائمـة البوتـات 🝰"
    mentions = "**⌔︙البـوتات في هذه الـمجموعة 🝰 : ** \n"
    input_str = event.pattern_match.group(1)
    if not input_str:
        chat = await event.get_input_chat()
    else:
        mentions = "**⌔︙البوتـات في {} من المجموعات 🝰 : ** \n".format(input_str)
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_or_reply(event, str(e))
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsBots
        ):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n - [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await edit_or_reply(event, mentions)


@iqthon.on(admin_cmd(pattern=r"الأعضاء(?: |$)(.*)"))
async def get_users(show):
    "⌔︙لإظهـار قائمـة الأعضـاء 𖤍"
    mentions = "**مستخدمين هذه المجموعة**: \n"
    await reply_id(show)
    input_str = show.pattern_match.group(1)
    if input_str:
        mentions = "**⌔︙الأعضاء في {} من المجموعات 𖤍  :** \n".format(input_str)
        try:
            chat = await show.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(show, f"`{str(e)}`", 10)
    else:
        if not show.is_group:
            return await edit_or_reply(show, "**⌔︙هـذه ليسـت مجموعـة ✕**")
    catevent = await edit_or_reply(show, "**⌔︙جـاري سحـب قائمـة معرّفـات الأعضـاء 🝛**")
    try:
        if show.pattern_match.group(1):
            async for user in show.client.iter_participants(chat.id):
                if user.deleted:
                    mentions += f"\n**⌔︙الحسـابات المحذوفـة ⌦** `{user.id}`"
                else:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
        else:
            async for user in show.client.iter_participants(show.chat_id):
                if user.deleted:
                    mentions += f"\n**⌔︙الحسـابات المحذوفـة ⌦** `{user.id}`"
                else:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await edit_or_reply(catevent, mentions)


@iqthon.on(admin_cmd(pattern=r"معلومات(?: |$)(.*)"))
async def info(event):
    "⌔︙للحصـول على معلومـات المجموعـة 🝢"
    catevent = await edit_or_reply(event, "**⌔︙يتـمّ جلـب معلومـات الدردشـة، إنتظـر ⅏**")
    chat = await get_chatinfo(event, catevent)
    caption = await fetch_info(chat, event)
    try:
        await catevent.edit(caption, parse_mode="html")
    except Exception as e:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, f"**⌔︙هنـاك خطـأ في معلومـات الدردشـة ✕ : **\n`{str(e)}`"
            )
        await catevent.edit("**⌔︙ حـدث خـطأ مـا، يرجـى التحقق من الأمـر ⎌**")


async def get_chatinfo(event, catevent):
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
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await catevent.edit("**⌔︙لـم يتـمّ العثـور على القنـاة/المجموعـة ✕**")
            return None
        except ChannelPrivateError:
            await catevent.edit(
                '**⌔︙ هـذه مجموعـة أو قنـاة خاصـة أو لقد تمّ حظـري منه ⛞**'
            )
            return None
        except ChannelPublicGroupNaError:
            await catevent.edit("**⌔︙القنـاة أو المجموعـة الخارقـة غيـر موجـودة ✕**")
            return None
        except (TypeError, ValueError) as err:
            await catevent.edit(str(err))
            return None
    return chat_info

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

async def fetch_info(chat, event):  # sourcery no-metrics
    # chat.chats is a list so we use get_entity() to avoid IndexError
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat_obj_info.title
    warn_emoji = emojize(":warning:")
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        LOGS.error(f"Exception: {str(e)}")
   
    first_msg_valid = bool(
        msg_info and msg_info.messages and msg_info.messages[0].id == 1
    )

    
    creator_valid = bool(first_msg_valid and msg_info.users)
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom)
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception:
        dc_id = "Unknown"

    # this is some spaghetti I need to change
    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    members_online = (
        chat.full_chat.online_count if hasattr(chat.full_chat, "online_count") else 0
    )
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "No"
    )
    slowmode = (
        "<b>مـفعل</b>"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "غير مفـعل"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "<b>نـعم</b>"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "لا"
    )
    verified = (
        "<b>مـوثق</b>"
        if hasattr(chat_obj_info, "verified") and chat_obj_info.verified
        else "غيـر موثق"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None
    # end of spaghetti block

    if admins is None:
        # use this alternative way if chat.full_chat.admins_count is None,
        # works even without being an admin
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            LOGS.error(f"Exception:{str(e)}")
    if bots_list:
        for _ in bots_list:
            bots += 1  

    caption = "<b>⌔︙معلومـات الدردشـة  🝢 :</b>\n"
    caption += f"⌔︙الآيـدي  : <code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"⌔︙إسـم المجموعـة  :{chat_title}\n"
    if former_title is not None:  # Meant is the very first title
        caption += f"⌔︙الإسم السابـق  : {former_title}\n"
    if username is not None:
        caption += f"⌔︙نـوع المجموعـة ⌂ : مجموعـة عامّـة  \n"
        caption += f"⌔︙الرابـط  : \n {username}\n"
    else:
        caption += f"⌔︙ نـوع المجموعـة ⌂ : مجموعـة عامّـة  \n"
    if creator_username is not None:
        caption += f"⌔︙ المالـك  :  {creator_username}\n"
    elif creator_valid:
        caption += (
            '⌔︙ المالـك  : <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
        )
    if created is not None:
        caption += f"⌔︙تاريـخ الإنشـاء  : \n <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"⌔︙الإنتـاج  :   <code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"⌔︙آيـدي قاعـدة البيانـات : {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"⌔︙الأعضـاء : <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"⌔︙الرسائـل التي يمڪن مشاهدتها : <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"⌔︙الرسائـل المرسلـة  :<code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"⌔︙الرسـائل المرسلة: <code>{messages_sent_alt}</code> {warn_emoji}\n"
    if members is not None:
        caption += f"⌔︙الأعضـاء : <code>{members}</code>\n"
    if admins is not None:
        caption += f"⌔︙المشرفيـن : <code>{admins}</code>\n"
    if bots_list:
        caption += f"⌔︙البـوتات : <code>{bots}</code>\n"
    if members_online:
        caption += f"⌔︙المتصليـن حـالياً : <code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"⌔︙الأعضـاء المقيّديـن : <code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"⌔︙الأعضـاء المحظوريـن : <code>{banned_users}</code>"
    if group_stickers is not None:
        caption += f'{chat_type} ⌔︙الملصقـات : <a href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>'
    caption += "\n"
    if not broadcast:
        caption += f"⌔︙الوضـع البطيئ : {slowmode}"
        if (
            hasattr(chat_obj_info, "slowmode_enabled")
            and chat_obj_info.slowmode_enabled
        ):
            caption += f", <code>{slowmode_time}s</code>\n"
        else:
            caption += "\n"
        caption += f"⌔︙الـمجموعـة الخارقـة  : {supergroup}\n"
    if hasattr(chat_obj_info, "restricted"):
        caption += f"⌔︙المقيّـد : {restricted}"
        if chat_obj_info.restricted:
            caption += f"> : {chat_obj_info.restriction_reason[0].platform}\n"
            caption += f"> ⌔︙السـبب  : {chat_obj_info.restriction_reason[0].reason}\n"
            caption += f"> ⌔︙النّـص  : {chat_obj_info.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "⌔︙السارقيـن : <b>Yes</b>\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"⌔︙الحسابـات الموثقـة   : {verified}\n"
    if description:
        caption += f"⌔︙الوصـف  : \n<code>{description}</code>\n"
    return caption

@iqthon.on(admin_cmd(pattern=r"اضافه ?(.*)"))
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        ram = await event.reply("`proses...`")
    else:
        ram = await event.edit("`proses...`")
    ramubotteam = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await ram.edit("`Sorry, Please add users here`")
    s = 0
    f = 0
    error = "None"

    await ram.edit("**TerminalStatus**\n\n`Collecting Users.......`")
    async for user in event.client.iter_participants(ramubotteam.full_chat.id):
        try:
            if error.startswith("Too"):
                return await ram.edit(
                    f"**Terminal Finished With Error**\n(`May Got Limit Error from telethon Please try agin Later`)\n**Error** : \n`{error}`\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people"
                )
            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s = s + 1
            await ram.edit(
                f"**Terminal Running...**\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people\n\n**× LastError:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await ram.edit(
        f"**Terminal Finished** \n\n• Successfully Invited `{s}` people \n• failed to invite `{f}` people"
    )

@iqthon.on(admin_cmd(pattern=r"تفليش(.*)"))
async def _(event):
    "iqthon"
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid)
    )
    if not result:
        return await edit_or_reply(
            event, "**⌔︙ ليس لديك صلاحيه حظر في هذا الدردشة**"
        )
    iqthonevent = await edit_or_reply(event, "**⌔︙جاري تفليش مجموعتك أنتظر قليلآ 🚮**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, KLANR_RIGHTS)
                )
                success += 15
                await sleep(0.2)  # for avoid any flood waits !!-> do not remove it
        except Exception as e:
            LOGS.info(str(e))
    await iqthonevent.edit(f"**⌔︙ تم بنجاح تفليش مجموعتك من {total} الاعضاء 🚮**")
    
async def ban_user(chat_id, i, rights):
    try:
        await iqthon(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


@iqthon.on(admin_cmd(pattern=r"غادر(.*)"))
async def kickme(leave):
    await leave.edit("**⌔︙ جـاري مـغادرة المجـموعة مـع السـلامة  🚶‍♂️  ..**")
    await leave.client.kick_participant(leave.chat_id, "me")

@iqthon.on(admin_cmd(pattern=r"مسح المحظورين(.*)"))
async def _(event):
    "To unban all banned users from group."
    catevent = await edit_or_reply(
        event, "**⌔︙  إلغاء حظر جميع الحسابات المحظورة في هذه المجموعة 🆘**"
    )
    succ = 0
    total = 0
    flag = False
    chat = await event.get_chat()
    async for i in event.client.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        total += 1
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await event.client(
                functions.channels.EditBannedRequest(event.chat_id, i, rights)
            )
        except FloodWaitError as e:
            LOGS.warn(f"**⌔︙ هناك ضغط كبير بالاستخدام يرجى الانتضار .. ‼️ بسبب  : {e.seconds} **")
            await catevent.edit(
                f"**⌔︙ {readable_time(e.seconds)} مطلـوب المـعاودة مـرة اخـرى للـمسح 🔁 **"
            )
            await sleep(e.seconds + 5)
        except Exception as ex:
            await catevent.edit(str(ex))
        else:
            succ += 1
            if flag:
                await sleep(2)
            else:
                await sleep(1)
            try:
                if succ % 10 == 0:
                    await catevent.edit(
                        f"**⌔︙ جـاري مسـح المحـظورين ⭕️  : \n {succ} الحسـابات الـتي غيـر محظـورة لحـد الان.**"
                    )
            except MessageNotModifiedError:
                pass
    await catevent.edit(f"**⌔︙ تـم مسـح المحـظورين مـن أصـل 🆘 :**{succ}/{total} \n اسـم المجـموعـة 📄 : {chat.title}")

@iqthon.on(admin_cmd(pattern=r"المحذوفين ?([\s\S]*)"))
async def rm_deletedacc(show):
    "To check deleted accounts and clean"
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**⌔︙لا توجـد حـسابات محذوفـة في هـذه المجموعـة !**"
    if con != "تنظيف":
        event = await edit_or_reply(
            show, "**⌔︙جـاري البحـث عـن الحسابـات المحذوفـة ⌯**"
        )
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"**⌔︙لقد وجـدت  {del_u}  من  حسابـات محذوفـة في هـذه المجموعـة لحذفهـم إستخـدم الأمـر  ⩥ :  `.المحذوفين تنظيف`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "⌔︙أنـا لسـت مشـرفـاً هنـا !", 5)
        return
    event = await edit_or_reply(
        show, "**⌔︙جـاري حـذف الحسـابات المحذوفـة ⌯**"
    )
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, "**⌔︙  ليس لدي صلاحيات الحظر هنا**", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**⌔︙تـم حـذف  {del_u}  الحسـابات المحذوفـة ✓**"
    if del_a > 0:
        del_status = f"**⌔︙تـم حـذف {del_u} الحسـابات المحذوفـة، ولڪـن لـم يتـم حذف الحسـابات المحذوفـة للمشرفيـن !**"
    await edit_delete(event, del_status, 5)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"**⌔︙تنظيف :**\
            \n⌔︙ {del_status}\
            \n*⌔︙المحادثـة ⌂** {show.chat.title}(`{show.chat_id}`)",
        )

@iqthon.on(admin_cmd(pattern=r"احصائيات الاعضاء ?([\s\S]*)"))
async def _(event):  # sourcery no-metrics
    "To get breif summary of members in the group.1 11"
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not chat.admin_rights and not chat.creator:
            await edit_or_reply(event, "**⌔︙ انت لست مشرف هنا**")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    et = await edit_or_reply(event, "**⌔︙ جـاري البحـث عـن قوائـم المشارڪيـن ⌯**")
    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**⌔︙ احتاج الى صلاحيات المشرفين للقيام بهذا الامر **")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**⌔︙أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """**⌔︙ الـمطرودين {} / {} الأعـضاء
⌔︙ الحـسابـات المـحذوفة: {}
⌔︙ حـالة المستـخدم الفـارغه: {}
⌔︙ اخر ظهور منذ شـهر: {}
⌔︙ اخر ظـهور منـذ اسبوع: {}
⌔︙ غير متصل: {}
⌔︙ المستخدمين النشطون: {}
⌔︙ اخر ظهور قبل قليل: {}
⌔︙ البوتات: {}
⌔︙ مـلاحظة: {}**"""
        await et.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await sleep(5)
    await et.edit(
        """**⌔︙ : {} مـجموع المـستخدمين
⌔︙ الحـسابـات المـحذوفة: {}
⌔︙ حـالة المستـخدم الفـارغه: {}
⌔︙ اخر ظهور منذ شـهر: {}
⌔︙ اخر ظـهور منـذ اسبوع: {}
⌔︙ غير متصل: {}
⌔︙ المستخدمين النشطون: {}
⌔︙ اخر ظهور قبل قليل: {}
⌔︙ البوتات: {}
⌔︙ مـلاحظة: {}**""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )    

def weird_division(n, d):
    return n / d if d else 0

@iqthon.on(admin_cmd(pattern=r"معلومات تخزين المجموعه(?:\s|$)([\s\S]*)"))
async def _(event):  # sourcery no-metrics
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    if reply and input_str:
        try:
            entity = int(input_str)
        except ValueError:
            entity = input_str
        userentity = reply.sender_id
    elif reply:
        entity = event.chat_id
        userentity = reply.sender_id
    elif input_str:
        entity = event.chat_id
        try:
            userentity = int(input_str)
        except ValueError:
            userentity = input_str
    else:
        entity = event.chat_id
        userentity = event.sender_id
    starttime = int(time.monotonic())
    x = PrettyTable()
    totalcount = totalsize = msg_count = 0
    x.title = "File Summary"
    x.field_names = ["Media", "Count", "File size"]
    largest = "   <b>أكبر حجم</b>\n"
    try:
        chatdata = await event.client.get_entity(entity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>⌔︙خطـأ ⚠️ : </b><code>{str(e)}</code>", 5, parse_mode="HTML"
        )
    try:
        userdata = await event.client.get_entity(userentity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>⌔︙خطـأ ⚠️ : </b><code>{str(e)}</code>", time=5, parse_mode="HTML"
        )
    if type(chatdata).__name__ == "Channel":
        if chatdata.username:
            link = f"<a href='t.me/{chatdata.username}'>{chatdata.title}</a>"
        else:
            link = chatdata.title
    else:
        link = f"<a href='tg://user?id={chatdata.id}'>{chatdata.first_name}</a>"
    catevent = await edit_or_reply(
        event,
        f"<code>⌔︙حسـاب عـدد الملفـات وحجـم الملـف حسـب ✦ </code>{_format.htmlmentionuser(userdata.first_name,userdata.id)}<code> in Group </code><b>{link}</b>\n<code>This may take some time also depends on number of user messages</code>",
        parse_mode="HTML",
    )

    media_dict = {
        m: {"file_size": 0, "count": 0, "max_size": 0, "max_file_link": ""}
        for m in TYPES
    }
    async for message in event.client.iter_messages(
        entity=entity, limit=None, from_user=userentity
    ):
        msg_count += 1
        media = media_type(message)
        if media is not None:
            media_dict[media]["file_size"] += message.file.size
            media_dict[media]["count"] += 1
            if message.file.size > media_dict[media]["max_size"]:
                media_dict[media]["max_size"] = message.file.size
                if type(chatdata).__name__ == "Channel":
                    media_dict[media][
                        "max_file_link"
                    ] = f"https://t.me/c/{chatdata.id}/{message.id}"
                else:
                    media_dict[media][
                        "max_file_link"
                    ] = f"tg://openmessage?user_id={chatdata.id}&message_id={message.id}"
            totalsize += message.file.size
            totalcount += 1
    for mediax in TYPES:
        x.add_row(
            [
                mediax,
                media_dict[mediax]["count"],
                humanbytes(media_dict[mediax]["file_size"]),
            ]
        )
        if media_dict[mediax]["count"] != 0:
            largest += f"  •  <b><a href='{media_dict[mediax]['max_file_link']}'>{mediax}</a>  : </b><code>{humanbytes(media_dict[mediax]['max_size'])}</code>\n"
    endtime = int(time.monotonic())
    if endtime - starttime >= 120:
        runtime = str(round(((endtime - starttime) / 60), 2)) + " minutes"
    else:
        runtime = str(endtime - starttime) + " seconds"
    avghubytes = humanbytes(weird_division(totalsize, totalcount))
    avgruntime = (
        str(round((weird_division((endtime - starttime), totalcount)) * 1000, 2))
        + " ms"
    )
    totalstring = f"<code><b> ⌔︙إجمالـي الملفـات ✦ : </b>       | {str(totalcount)}\
                  \n <b> ⌔︙الحجـم الإجمالـي للملـف ✦ : </b>   | {humanbytes(totalsize)}\
                  \n <b> حجم الملف  : </b>    | {avghubytes}\
                  \n</code>"
    runtimestring = f"<code><b> ⌔︙وقـت التشغيـل ✦ :</b>            | {runtime}\
                    \n <b> وقـت التشغيـل لڪل ملـف ✦ :</b>   | {avgruntime}\
                    \n</code>"
    line = "<code>+--------------------+-----------+</code>\n"
    result = f"<b>⌔︙المجموعـة ✦ : {link}\nUser : {_format.htmlmentionuser(userdata.first_name,userdata.id)}\n\n"
    result += f"<code><b>⌔︙مجمـوع الرسائـل ✦ :</b> {msg_count}</code>\n"
    result += "<b>⌔︙ملخـص الملـف ✦ : </b>\n"
    result += f"<code>{str(x)}</code>\n"
    result += f"{largest}"
    result += line + totalstring + line + runtimestring + line
    await catevent.edit(result, parse_mode="HTML", link_preview=False)    
    
@iqthon.iq_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def monito_p_m_s(event):
    if Config.PM_LOGGER_GROUP_ID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    if LOG_CHATS_.COUNT > 1:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "⌔︙ رسـالة جـديدة", f"{LOG_CHATS_.COUNT} "
                            )
                        )
                    else:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "⌔︙ رسـالة جـديدة", f"{LOG_CHATS_.COUNT} "
                            )
                        )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await event.client.send_message(
                    Config.PM_LOGGER_GROUP_ID,
                    f"👤{_format.mentionuser(sender.first_name , sender.id)}\n **⌔︙ قام بأرسال رسالة جديدة** \n⌔︙ ايدي الشخص   : `{chat.id}`",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))

@iqthon.iq_cmd(incoming=True, func=lambda e: e.mentioned, edited=False, forword=None)
async def log_tagged_messages(event):
    hmm = await event.get_chat()
    from .afk import AFK_

    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        return
    if (
        (no_log_pms_sql.is_approved(hmm.id))
        or (Config.PM_LOGGER_GROUP_ID == -100)
        or ("on" in AFK_.USERAFK_ON)
        or (await event.get_sender() and (await event.get_sender()).bot)
    ):
        return
    full = None
    try:
        full = await event.client.get_entity(event.message.from_id)
    except Exception as e:
        LOGS.info(str(e))
    messaget = media_type(event)
    resalt = f"⌔︙ المجموعه : </b><code>{hmm.title}</code>"
    if full is not None:
        resalt += (
            f"\n<b>⌔︙ من : </b> 👤{_format.htmlmentionuser(full.first_name , full.id)}"
        )
    if messaget is not None:
        resalt += f"\n<b>⌔︙ رسـالة جـديدة : </b><code>{messaget}</code>"
    else:
        resalt += f"\n<b>⌔︙ رسـالة جـديدة: </b>{event.message.message}"
    resalt += f"\n<b>⌔︙ رابط الرساله : </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> اضغط هنا</a>"
    if not event.is_private:
        await event.client.send_message(
            Config.PM_LOGGER_GROUP_ID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )
@iqthon.on(admin_cmd(pattern=r"تخزين الخاص (تشغيل|ايقاف)$"))
async def set_pmlog(event):
    "iqthon"
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        h_type = False
    elif input_str == "تشغيل":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await event.edit("**⌔︙ تـخزين رسـائل الخـاص بالفـعل مُمكـنة ✅**")
        else:
            addgvar("PMLOG", h_type)
            await event.edit("**⌔︙ تـم تعـطيل تخـزين رسائل الـخاص بنـجاح ✅**")
    elif h_type:
        addgvar("PMLOG", h_type)
        await event.edit("**⌔︙ تـم تفعيل تخـزين رسائل الـخاص بنـجاح ✅**")
    else:
        await event.edit("**⌔︙ تـخزين رسـائل الخـاص بالفـعل معـطلة ✅**")

@iqthon.on(admin_cmd(pattern=r"تخزين الكروبات (تشغيل|ايقاف)$"))
async def set_grplog(event):
    "iqthon"
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        h_type = False
    elif input_str == "تشغيل":
        h_type = True
    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        GRPLOG = False
    else:
        GRPLOG = True
    if GRPLOG:
        if h_type:
            await event.edit("**⌔︙ تـخزين رسـائل الكروبات بالفـعل مُمكـنة ✅**")
        else:
            addgvar("GRPLOG", h_type)
            await event.edit("**⌔︙ تـم تعـطيل تخـزين رسائل الكروبات بنـجاح ✅**")
    elif h_type:
        addgvar("GRPLOG", h_type)
        await event.edit("**⌔︙ تـم تفعيل تخـزين رسائل الكروبات بنـجاح ✅**")
    else:
        await event.edit("**⌔︙ تـخزين رسـائل الكروبات بالفـعل معـطلة ✅**")    
    
@iqthon.on(admin_cmd(pattern="الرابط ?(.*)"))
async def iq(SLQ):
    await SLQ.edit("جاري جلب الرابط")
    try:
        l5 = await SLQ.client(
            ExportChatInviteRequest(SLQ.chat_id),
        )
    except ChatAdminRequiredError:
        return await bot.send_message(f"**عزيزي {ALIVE_NAME} لست مشرف في هذا المجموعه **")
    await SLQ.edit(f"**رابط المجموعه :**: {l5.link}")   
    
@iqthon.on(admin_cmd(pattern="عدد رسائلي ?(.*)"))
async def iq(SLQ):
    k = await SLQ.get_reply_message()
    if k:
        a = await bot.get_messages(SLQ.chat_id, 0, from_user=k.sender_id)
        return await SLQ.edit(
            f"**مجموع** `{a.total}` **الرسائل** {thon} **هنا**"
        )
    thon = SLQ.pattern_match.group(1)
    if not thon:
        thon = "me"
    a = await bot.get_messages(SLQ.chat_id, 0, from_user=thon)
    await SLQ.edit(
        f"*مجموع `{a.total}` الرسائل هنا**"
    )   

@iqthon.on(admin_cmd(pattern="تغير صورة( المجموعة| -d)$"))
async def set_group_photo(event):  # sourcery no-metrics
    "For changing Group dp"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "المجموعة":
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
                return await edit_delete(event, f"**Error : **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**Error : **`{e}`")
        process = "deleted"
        await edit_delete(event, "```successfully group profile pic deleted.```")
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
        ban_users=False,
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
@iqthon.on(admin_cmd(pattern="صورة(?: |$)(\d*)? ?([\s\S]*)"))
async def img_sampler(event):
    reply_to_id = await reply_id(event)
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edit_or_reply(
            event, "**⌔︙ الرد على رسالة أو تمرير استعلام للبحث**"
        )
    cat = await edit_or_reply(event, "**⌔︙ جـاري البحـث علـى الصورة 🗾**")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim > 10:
            lim = int(10)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(3)
    response = googleimagesdownload()
    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }
    
    try:
        paths = response.download(arguments)
    except Exception as e:
        return await cat.edit(f"**⌔︙ حدث خطأ  ❌ :** \n`{e}`")
    lst = paths[0][query]
    await event.client.send_file(event.chat_id, lst, reply_to=reply_to_id)
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await cat.delete()
