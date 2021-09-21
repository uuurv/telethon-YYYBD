from userbot import iqthon
from userbot.utils import admin_cmd
from telethon.tl.types import Channel, Chat, User
from telethon.tl import functions, types
from telethon.tl.functions.messages import  CheckChatInviteRequest, GetFullChatRequest
from telethon.errors import (ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError, InviteHashEmptyError, InviteHashExpiredError, InviteHashInvalidError)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest


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
            await event.reply("**⌔︙ لا يمكنني استخدام الامر من الكروبات او القنوات الخاصة**")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**⌔︙ لم يتم العثور على المجموعة او القناة**")
            return None
        except (TypeError, ValueError) as err:
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
    full_name = ' '.join(names)
    return full_name
 
@iqthon.iq(admin_cmd(pattern=r"نقل الاعضاء ?(.*)"))
async def get_users(event):   
    sender = await event.get_sender() ; me = await event.client.get_me()
    if not sender.id == me.id:
        kno = await event.reply("**⌔︙ جـاري نـقل الأعـضـاء 🚻**")
    else:
        kno = await event.edit("**⌔︙ جـاري نـقل الأعـضـاء 🚻**")
    IQTHON = await get_chatinfo(event) ; chat = await event.get_chat()
    if event.is_private:
              return await kno.edit("**⌔︙ لا يمكننـي اضافـة المـستخدمين هـنا**")    
    s = 0 ; f = 0 ; error = 'None'   
  
    await kno.edit("⌔︙ حـالة الأضافة:**\n\n**⌔︙ تتـم جـمع معـلومات الـمستخدمين 🔄 ...**")
    async for user in event.client.iter_participants(IQTHON.full_chat.id):
                try:
                    if error.startswith("Too"):
                        return await kno.edit(f"**⌔︙ حـالة الأضـافة انتـهت مـع الأخـطاء**\n⌔︙ (**ربـما هـنالك ضغـط عـلى الأمࢪ حاول مججـدا لاحقـا **) \n**⌔︙ الـخطأ** : \n⌔︙ `{error}`\n\n⌔︙ اضالـة `{s}` \n⌔︙ خـطأ بأضافـة `{f}`"),
                    await event.client(functions.channels.InviteToChannelRequest(channel=chat,users=[user.id]))
                    s = s + 1                                                    
                    await kno.edit(f"**⌔︙ تتـم الأضـافة  **\n\n⌔︙ اضـيف `{s}` \n⌔︙  خـطأ بأضافـة `{f}` \n\n**× اخـر خـطأ:** `{error}`") 
                except Exception as e:
                    error = str(e) ; f = f + 1             
    return await kno.edit(f"**⌔︙ اڪتـملت الأضافـة ✅** \n\n⌔︙ تـم بنجـاح اضافـة `{s}` \n⌔︙ خـطأ بأضافـة `{f}`")
