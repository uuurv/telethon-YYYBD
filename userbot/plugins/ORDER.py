import math
import os
import random
import re
import time
from uuid import uuid4
from platform import python_version

from telethon import Button, types, version, functions
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.utils import get_display_name

from userbot import iqthon
from ..plugins import mention
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import rand_key, catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import mention






@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"List1")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**Sorry, these options are not for you**"
        return await event.answer(text, cache_time=0, alert=True)
    text = "Command List 1: Coming Soon"
    sqllist.add_to_list(event.query.user_id)
    await event.edit(text)


@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"List2")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**Sorry, these options are not for you**"
        return await event.answer(text, cache_time=0, alert=True)
    text = "Command List 1: Coming Soon"
    sqllist.add_to_list(event.query.user_id)
    await event.edit(text)


@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"List3")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**Sorry, these options are not for you**"
        return await event.answer(text, cache_time=0, alert=True)
    text = "Command List 1: Coming Soon"
    sqllist.add_to_list(event.query.user_id)
    await event.edit(text)


@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"List4")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**Sorry, these options are not for you**"
        return await event.answer(text, cache_time=0, alert=True)
    text = "Command List 1: Coming Soon"
    sqllist.add_to_list(event.query.user_id)
    await event.edit(text)



@iqthon.tgbot.on(CallbackQuery(data=re.compile(b"lists(?: |$)(.*)")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**Sorry, these options are not for you**"
        return await event.answer(text, cache_time=0, alert=True)
    text = f"Welcome to the list of orders"
    buttons = [
        (Button.inline(text="Command 1", data="List1"),),
        (Button.inline(text="Command 2", data="List2"),),
        (Button.inline(text="Command 3", data="List3"),),
        (Button.inline(text="Command 4",data="List4",
            ),
        ),
    ]
    sqllist.add_to_list(event.query.user_id)
    await event.edit(text, buttons=buttons)
