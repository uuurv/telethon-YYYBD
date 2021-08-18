import asyncio
from datetime import datetime

from userbot import iqthon

from ..core.managers import edit_or_reply

plugin_category = "tools"


@iqthon.iq_cmd(
    pattern="بنك( الاعلى|$)",
    command=("بنك", plugin_category),
    info={
        "header": "check how long it takes to ping your userbot",
        "flags": {"-a": "average ping"},
        "usage": ["{tr}ping", "{tr}ping -a"],
    },
)
async def _(event):
    "To check ping"
    flag = event.pattern_match.group(1)
    start = datetime.now()
    if flag == " الاعلى":
        catevent = await edit_or_reply(event, "**⌔︙ جاري قياس البنك  📶..**")
        await asyncio.sleep(0.3)
        await catevent.edit("**⌔︙ جاري قياس البنك  📶..**")
        await asyncio.sleep(0.3)
        await catevent.edit("**⌔︙ جاري قياس البنك  📶..**")
        end = datetime.now()
        tms = (end - start).microseconds / 1000
        ms = round((tms - 0.6) / 3, 3)
        await catevent.edit(f"**⌔︙ سرعه الاستجابة للبنك هيه  📶 :**  `{ms} بالثانية`  ")
    else:
        catevent = await edit_or_reply(event, "Pong!")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await catevent.edit(f"**⌔︙ سرعه الاستجابة للبنك هيه  📶 :**  `{ms} بالثانية`  ")


@iqthon.iq_cmd(
    pattern="البنك$",
    command=("البنك", plugin_category),
    info={"header": "Shows the server ping with extra animation", "usage": "{tr}البنك"},
)
async def _(event):
    "To check ping with animation"
    start = datetime.now()
    animation_interval = 0.3
    animation_ttl = range(26)
    event = await edit_or_reply(event, "**⌔︙ جاري قياس البنك بتسليه 📶..**")
    animation_chars = [
        "╔══╗─╔╗╔╗",
        "╚║║╬═╣╚╣╚╦═╦═╦╗",
        "╔║║╣╬║╔╣║║╬║║║║",
        "╚══╩╗╠═╩╩╩═╩╩═╝",
        "────╚╝",
        f"\n**⌔︙ تم تحديث البنك الخاص بك هوه  :**  {ms}  بالثانية  📶",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 26])
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(
        f"╔══╗─╔╗╔╗\n ╚║║╬═╣╚╣╚╦═╦═╦╗ \n ╔║║╣╬║╔╣║║╬║║║║\n ╚══╩╗╠═╩╩╩═╩╩═╝ \n ────╚╝\n⌔︙ تم تحديث البنك الخاص بك هوه  :  {ms}  بالثانية  ⚜️"
    )
