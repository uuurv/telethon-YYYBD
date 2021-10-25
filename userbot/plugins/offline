import os

from telethon.tl import functions
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.users import GetFullUserRequest


from userbot import iqthon

OFFLINE_TAG = f"#OFFLINE "
ONLINE_TAG = f"#ONLINE "


@iqthon.on(admin_cmd(pattern="مشغول(?: |$)(.*)"))
async def iq(event):
    if event.fwd_from:
        return
    user_it = "me"
    user = await event.client.get_entity(user_it)
    if user.first_name.startswith(OFFLINE_TAG):
        await event.edit("بالفعل تم تشغيل وضع الانشغال")
        return
    await event.edit("تم تشغيل وضع الانشغال")



@iqthon.on(admin_cmd(pattern="نشط(?: |$)(.*)"))
async def iq(event):
    if event.fwd_from:
        return
    user_it = "me"
    user = await event.client.get_entity(user_it)
    if user.first_name.startswith(OFFLINE_TAG):
        await event.edit("بالفعل تم تشغيل وضع الاونلانين")
    else:
        await event.edit("تم تشغيل وضع الاونلاين")
