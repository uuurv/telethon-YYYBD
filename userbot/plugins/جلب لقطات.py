import os

from userbot import iqthon

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import _catutils, reply_id
from . import make_gif

plugin_category = "utils"


@iqthon.iq_cmd(
    pattern="جلب لقطات(?:\s|$)([\s\S]*)",
    command=("collage", plugin_category),
    info={
        "header": "To create collage from still images extracted from video/gif.",
        "description": "Shows you the grid image of images extracted from video/gif. you can customize the Grid size by giving integer between 1 to 9 to cmd by default it is 3",
        "usage": "{tr}collage <1-9>",
    },
)
async def collage(event):
    "To create collage from still images extracted from video/gif."
    catinput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    catid = await reply_id(event)
    event = await edit_or_reply(
        event, "**⌔︙جاري الالتقاط قـد يستغـرق هـذا الأمـر عـدة دقائـق انتضر ...**"
    )
    if not (reply and (reply.media)):
        await event.edit("**⌔︙تنسيـق الوسائـط غيـر مدعـوم ⚠️**")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith((".mp4", ".mkv", ".tgs")):
        os.remove(catsticker)
        await event.edit("**⌔︙تنسيـق الوسائـط غيـر مدعـوم ⚠️**")
        return
    if catinput:
        if not catinput.isdigit():
            os.remove(catsticker)
            await event.edit("**⌔︙إدخـالك غيـر صالـح، يرجـىٰ التحـقق مـن المساعـدة ⚠️**")
            return
        catinput = int(catinput)
        if not 0 < catinput < 10:
            os.remove(catsticker)
            await event.edit(
                "**⌔︙يرجـىٰ وضـع عـدد الصـور بجانـب الأمـر إختـر رقـماً بيـن 1 إلـى 9 ✦**"
            )
            return
    else:
        catinput = 3
    if catsticker.endswith(".tgs"):
        hmm = await make_gif(event, catsticker)
        if hmm.endswith(("@tgstogifbot")):
            os.remove(catsticker)
            return await event.edit(hmm)
        collagefile = hmm
    else:
        collagefile = catsticker
    endfile = "./temp/collage.png"
    catcmd = f"vcsi -g {catinput}x{catinput} '{collagefile}' -o {endfile}"
    stdout, stderr = (await _catutils.runcmd(catcmd))[:2]
    if not os.path.exists(endfile):
        for files in (catsticker, collagefile):
            if files and os.path.exists(files):
                os.remove(files)
        return await edit_delete(
            event, f"**⌔︙تنسيـق الوسائـط غيـر مدعـوم، حـاول إستخـدام عـدد أصغـر  ⚠️**", 5
        )
    await event.client.send_file(
        event.chat_id,
        endfile,
        reply_to=catid,
    )
    await event.delete()
    for files in (catsticker, collagefile, endfile):
        if files and os.path.exists(files):
            os.remove(files)
