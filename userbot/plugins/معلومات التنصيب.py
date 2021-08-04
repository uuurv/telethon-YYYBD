from userbot import iqthon

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _catutils, parse_pre, yaml_format

plugin_category = "tools"


@iqthon.iq_cmd(
    pattern="حذف جميع الملفات$",
    command=("suicide", plugin_category),
    info={
        "header": "Deletes all the files and folder in the current directory.",
        "usage": "{tr}suicide",
    },
)
async def _(event):
    "To delete all files and folders in userbot"
    cmd = "rm -rf .*"
    await _catutils.runcmd(cmd)
    OUTPUT = f"**⌔︙تنبيـه، لقـد تم حـذف جميـع المجلـدات والملفـات الموجـودة في البـوت بنجـاح ✓**"
    event = await edit_or_reply(event, OUTPUT)



@iqthon.iq_cmd(
    pattern="معلومات تنصيبي$",
    command=("env", plugin_category),
    info={
        "header": "To list all environment values in userbot.",
        "description": "to show all heroku vars/Config values in your userbot",
        "usage": "{tr}env",
    },
)
async def _(event):
    "To show all config values in userbot"
    cmd = "env"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = (
        f"⌔︙وحـدة المعلومات الخاصه بتنصيبك مع جميع الفارات  لتنصيب سورس تليثون @M4_STORY :**\n\n{o}"
    )
    await edit_or_reply(event, OUTPUT)





@iqthon.iq_cmd(
    pattern="تاريخ الرساله$",
    command=("when", plugin_category),
    info={
        "header": "To get date and time of message when it posted.",
        "usage": "{tr}when <reply>",
    },
)
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
