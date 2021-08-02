import asyncio
import base64
import io
import logging
import os
import time
from datetime import datetime
from io import BytesIO
from shutil import copyfile

import fitz
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from pymediainfo import MediaInfo
from telethon import types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.functions.messages import SendMediaRequest
from telethon.utils import get_attributes

from userbot import iqthon

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, progress, thumb_from_audio
from ..helpers.functions import (
    convert_toimage,
    convert_tosticker,
    invert_frames,
    l_frames,
    r_frames,
    spin_frames,
    ud_frames,
    vid_to_gif,
)
from ..helpers.utils import _cattools, _catutils, _format, parse_pre, reply_id
from . import make_gif

plugin_category = "misc"


if not os.path.isdir("./temp"):
    os.makedirs("./temp")


LOGS = logging.getLogger(__name__)
PATH = os.path.join("./temp", "temp_vid.mp4")

thumb_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@iqthon.iq_cmd(
    pattern="تحويل فديو دائري(?: |$)((-)?(s)?)$",
    command=("spin", plugin_category),
    info={
        "header": "To convert replied image or sticker to spining round video.",
        "flags": {
            "-s": "to save in saved gifs.",
        },
        "usage": [
            "{tr}spin <flag>",
        ],
        "examples": ["{tr}spin", "{tr}spin -s"],
    },
)
async def pic_gifcmd(event):  # sourcery no-metrics
    "To convert replied image or sticker to spining round video."
    args = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "**⌔︙قـم بالـرد على وسائـط مدعومـة !**")
    media_type(reply)
    catevent = await edit_or_reply(event, "**⌔︙جـاري تحويل الملصق الى فيديو مرئي دائـري ⌯**")
    output = await _cattools.media_to_pic(event, reply, noedits=True)
    if output[1] is None:
        return await edit_delete(
            output[0], "**⌔︙تعـذّر إستخـراج الصـورة من الرسالـة التي تـم الـرّد عليهـا ✕**"
        )
    meme_file = convert_toimage(output[1])
    image = Image.open(meme_file)
    w, h = image.size
    outframes = []
    try:
        outframes = await spin_frames(image, w, h, outframes)
    except Exception as e:
        return await edit_delete(output[0], f"**⌔︙خطـأ ⚠️ :**\n__{str(e)}__")
    output = io.BytesIO()
    output.name = "Output.gif"
    outframes[0].save(output, save_all=True, append_images=outframes[1:], duration=1)
    output.seek(0)
    with open("Output.gif", "wb") as outfile:
        outfile.write(output.getbuffer())
    final = os.path.join(Config.TEMP_DIR, "output.gif")
    output = await vid_to_gif("Output.gif", final)
    if output is None:
        return await edit_delete(catevent, "**⌔︙تعـذّر صنـع صـورة متحرڪـة دوارة ✕**")
    media_info = MediaInfo.parse(final)
    aspect_ratio = 1
    for track in media_info.tracks:
        if track.track_type == "Video":
            aspect_ratio = track.display_aspect_ratio
            height = track.height
            width = track.width
    PATH = os.path.join(Config.TEMP_DIR, "round.gif")
    if aspect_ratio != 1:
        crop_by = width if (height > width) else height
        await _catutils.runcmd(
            f'ffmpeg -i {final} -vf "crop={crop_by}:{crop_by}" {PATH}'
        )
    else:
        copyfile(final, PATH)
    time.time()
    ul = io.open(PATH, "rb")
    uploaded = await event.client.fast_upload_file(
        file=ul,
    )
    ul.close()
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type="video/mp4",
        attributes=[
            types.DocumentAttributeVideo(
                duration=0,
                w=1,
                h=1,
                round_message=True,
                supports_streaming=True,
            )
        ],
        force_file=False,
        thumb=await event.client.upload_file(meme_file),
    )
    sandy = await event.client.send_file(
        event.chat_id,
        media,
        reply_to=reply,
        video_note=True,
        supports_streaming=True,
    )
    if not args:
        await _catutils.unsavegif(event, sandy)
    await catevent.delete()
    for i in [final, "Output.gif", meme_file, PATH, final]:
        if os.path.exists(i):
            os.remove(i)


@iqthon.iq_cmd(
    pattern="تحويل ملصق دائري ?((-)?s)?$",
    command=("circle", plugin_category),
    info={
        "header": "To make circular video note/sticker.",
        "description": "crcular video note supports atmost 60 sec so give appropariate video.",
        "usage": "{tr}circle <reply to video/sticker/image>",
    },
)
async def video_catfile(event):  # sourcery no-metrics
    "To make circular video note."
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    catid = await reply_id(event)
    if not reply or not reply.media:
        return await edit_delete(event, "**⌔︙قـم بالـرد على وسائـط مدعومـة !**")
    mediatype = media_type(reply)
    if mediatype == "Round Video":
        return await edit_delete(
            event,
            "⌔︙الوسائـط التي تم الـرد عليهـا هـي بالفعـل في شڪـل دائـري، أعـد التحـقق !",
        )
    if mediatype not in ["Photo", "Audio", "Voice", "Gif", "Sticker", "Video"]:
        return await edit_delete(event, "**⌔︙لم يتـم العثـور على وسائـط مدعومـة !**")
    flag = True
    catevent = await edit_or_reply(event, "**⌔︙جـاري التحويـل إلى شڪـل دائـري ⌯**")
    catfile = await reply.download_media(file="./temp/")
    if mediatype in ["Gif", "Video", "Sticker"]:
        if not catfile.endswith((".webp")):
            if catfile.endswith((".tgs")):
                hmm = await make_gif(catevent, catfile)
                os.rename(hmm, "./temp/circle.mp4")
                catfile = "./temp/circle.mp4"
            media_info = MediaInfo.parse(catfile)
            aspect_ratio = 1
            for track in media_info.tracks:
                if track.track_type == "Video":
                    aspect_ratio = track.display_aspect_ratio
                    height = track.height
                    width = track.width
            if aspect_ratio != 1:
                crop_by = width if (height > width) else height
                await _catutils.runcmd(
                    f'ffmpeg -i {catfile} -vf "crop={crop_by}:{crop_by}" {PATH}'
                )
            else:
                copyfile(catfile, PATH)
            if str(catfile) != str(PATH):
                os.remove(catfile)
            try:
                catthumb = await reply.download_media(thumb=-1)
            except Exception as e:
                LOGS.error(f"circle - {str(e)}")
    elif mediatype in ["Voice", "Audio"]:
        catthumb = None
        try:
            catthumb = await reply.download_media(thumb=-1)
        except Exception:
            catthumb = os.path.join("./temp", "thumb.jpg")
            await thumb_from_audio(catfile, catthumb)
        if catthumb is not None and not os.path.exists(catthumb):
            catthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, catthumb)
        if (
            catthumb is not None
            and not os.path.exists(catthumb)
            and os.path.exists(thumb_loc)
        ):
            flag = False
            catthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, catthumb)
        if catthumb is not None and os.path.exists(catthumb):
            await _catutils.runcmd(
                f"""ffmpeg -loop 1 -i {catthumb} -i {catfile} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -vf \"scale=\'iw-mod (iw,2)\':\'ih-mod(ih,2)\',format=yuv420p\" -shortest -movflags +faststart {PATH}"""
            )
            os.remove(catfile)
        else:
            os.remove(catfile)
            return await edit_delete(
                catevent, "**لا يوجـد ما يصلـح لجعلـه ملاحظـة فيديـو ⚠️**", 5
            )
    if (
        mediatype
        in [
            "Voice",
            "Audio",
            "Gif",
            "Video",
            "Sticker",
        ]
        and not catfile.endswith((".webp"))
    ):
        if os.path.exists(PATH):
            c_time = time.time()
            attributes, mime_type = get_attributes(PATH)
            ul = io.open(PATH, "rb")
            uploaded = await event.client.fast_upload_file(
                file=ul,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "**⌔︙قـم بالـرد على وسائـط مدعومـة !**")
                ),
            )
            ul.close()
            media = types.InputMediaUploadedDocument(
                file=uploaded,
                mime_type="video/mp4",
                attributes=[
                    types.DocumentAttributeVideo(
                        duration=0,
                        w=1,
                        h=1,
                        round_message=True,
                        supports_streaming=True,
                    )
                ],
                force_file=False,
                thumb=await event.client.upload_file(catthumb) if catthumb else None,
            )
            sandy = await event.client.send_file(
                event.chat_id,
                media,
                reply_to=catid,
                video_note=True,
                supports_streaming=True,
            )

            if not args:
                await _catutils.unsavegif(event, sandy)
            os.remove(PATH)
            if flag:
                os.remove(catthumb)
        await catevent.delete()
        return
    data = reply.photo or reply.media.document
    img = io.BytesIO()
    await event.client.download_file(data, img)
    im = Image.open(img)
    w, h = im.size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.paste(im, (0, 0))
    m = min(w, h)
    img = img.crop(((w - m) // 2, (h - m) // 2, (w + m) // 2, (h + m) // 2))
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((10, 10, w - 10, h - 10), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    img = ImageOps.fit(img, (w, h))
    img.putalpha(mask)
    im = io.BytesIO()
    im.name = "cat.webp"
    img.save(im)
    im.seek(0)
    await event.client.send_file(event.chat_id, im, reply_to=catid)
    await catevent.delete()


@iqthon.iq_cmd(
    pattern="تحويل صوره$",
    command=("تحويل صوره", plugin_category),
    info={
        "header": "Reply this command to a sticker to get image.",
        "description": "This also converts every media to image. that is if video then extracts image from that video.if audio then extracts thumb.",
        "usage": "{tr}stoi",
    },
)
async def _(event):
    "Sticker to image Conversion."
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(
            event, "**⌔︙قم بالـرد على أيّ وسائـط أو ملصـق لتحويلـه إلى صـورة ❖**"
        )
    output = await _cattools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "**⌔︙قم بالـرد على أيّ وسائـط أو ملصـق لتحويلـه إلى صـورة ❖**"
        )
    meme_file = convert_toimage(output[1])
    await event.client.send_file(
        event.chat_id, meme_file, reply_to=reply_to_id, force_document=False
    )
    await output[0].delete()





@iqthon.iq_cmd(
    pattern="تحويل ملف ([\s\S]*)",
    command=("ttf", plugin_category),
    info={
        "header": "Text to file.",
        "description": "Reply this command to a text message to convert it into file with given name.",
        "usage": "{tr}ttf <file name>",
    },
)
async def get(event):
    "text to file conversion"
    name = event.text[5:]
    if name is None:
        await edit_or_reply(event, "**⌔︙قم بالـرد على الرسالـة لتحويلها الى ملف**")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await edit_or_reply(event, "**⌔︙قم بالـرد على الرسالـة لتحويلها الى ملف**")


@iqthon.iq_cmd(
    pattern="تحويل رساله$",
    command=("ftt", plugin_category),
    info={
        "header": "File to text.",
        "description": "Reply this command to a file to print text in that file to text message.",
        "support types": "txt, py, pdf and many more files in text format",
        "usage": "{tr}ftt <reply to document>",
    },
)
async def get(event):
    "File to text message conversion."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if mediatype != "Document":
        return await edit_delete(
            event, "**⌔︙يبـدو أن هـذا الملـف غـير قابـل للڪتابـة،  يرجـى الـرد على ملـف قابـل للكتابـة !**"
        )
    file_loc = await reply.download_media()
    file_content = ""
    try:
        with open(file_loc) as f:
            file_content = f.read().rstrip("\n")
    except UnicodeDecodeError:
        pass
    except Exception as e:
        LOGS.info(e)
    if file_content == "":
        try:
            with fitz.open(file_loc) as doc:
                for page in doc:
                    file_content += page.getText()
        except Exception as e:
            if os.path.exists(file_loc):
                os.remove(file_loc)
            return await edit_delete(event, f"**⌔︙خطـأ ⚠️**\n__{str(e)}__")
    await edit_or_reply(
        event,
        file_content,
        parse_mode=parse_pre,
        aslink=True,
        noformat=True,
        linktext="**⌔︙يسمـح تليڪرام فقـط بـ 4096 حرفًـا في الرسالـة الواحـدة، ولڪن الملـف الـذي قمـت بالـرد عليـه يحتـوي على أڪثـر مـن ذلـك بڪثيـر، لذلـك (( لصقها على رابط لصق )) غيرها انت)) !**",
    )
    if os.path.exists(file_loc):
        os.remove(file_loc)


@iqthon.iq_cmd(
    pattern="تحويل ملف صوره$",
    command=("تحويل ملف صوره", plugin_category),
    info={
        "header": "Reply this command to a image file to convert it to image",
        "usage": "{tr}ftoi",
    },
)
async def on_file_to_photo(event):
    "image file(png) to streamable image."
    target = await event.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return await edit_delete(event, "**⌔︙هـذه ليسـت صـورة !**")
    if not image.mime_type.startswith("image/"):
        return await edit_delete(event, "**⌔︙هـذه ليسـت صـورة !**")
    if image.mime_type == "image/webp":
        return await edit_delete(event, "**⌔︙لتحويـل الملصـق إلى صـورة إستخـدم الأمـر  ⩥ :**  `.تحويل ملف صوره`")
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise
    catt = await edit_or_reply(event, "**⌔︙جـاري التحويـل  ↯**")
    file = await event.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await event.client.upload_file(file)
    img.name = "image.png"
    try:
        await event.client(
            SendMediaRequest(
                peer=await event.get_input_chat(),
                media=types.InputMediaUploadedPhoto(img),
                message=target.message,
                entities=target.entities,
                reply_to_msg_id=target.id,
            )
        )
    except PhotoInvalidDimensionsError:
        return
    await catt.delete()


@iqthon.iq_cmd(
    pattern="تحويل ملصق متحرك(?:\s|$)([\s\S]*)",
    command=("gif", plugin_category),
    info={
        "header": "Converts Given animated sticker to gif.",
        "usage": "{tr}gif quality ; fps(frames per second)",
    },
)
async def _(event):  # sourcery no-metrics
    "Converts Given animated sticker to gif"
    input_str = event.pattern_match.group(1)
    if not input_str:
        quality = None
        fps = None
    else:
        loc = input_str.split(";")
        if len(loc) > 2:
            return await edit_delete(
                event,
                "**⌔︙بنـاء جملـة خاطـئ !**",
            )
        if len(loc) == 2:
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edit_delete(event, "**⌔︙إستخـدم جـودة النطـاق مـن 0 إلى 721 ✦**")
            if 0 < loc[1] < 20:
                quality = loc[1].strip()
            else:
                return await edit_delete(event, "**⌔︙إستخـدم جـودة النطـاق مـن 0 إلى 20 ✦**")
        if len(loc) == 1:
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edit_delete(event, "**⌔︙إستخـدم جـودة النطـاق مـن 0 إلى 721 ✦**")
    catreply = await event.get_reply_message()
    cat_event = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not catreply or not catreply.media or not catreply.media.document:
        return await edit_or_reply(event, "**⌔︙هـذا ليـس ملصـق متحرك   !**")
    if catreply.media.document.mime_type != "application/x-tgsticker":
        return await edit_or_reply(event, "**⌔︙هـذا ليـس ملصـق متحرك  !**")
    catevent = await edit_or_reply(
        event,
        "**⌔︙جـاري تحويـل هـذا الملصـق إلى صـورة متحرڪـة، قـد يستغـرق هـذا بضـع دقائـق ✦**",
        parse_mode=_format.parse_pre,
    )
    try:
        cat_event = Get(cat_event)
        await event.client(cat_event)
    except BaseException:
        pass
    reply_to_id = await reply_id(event)
    catfile = await event.client.download_media(catreply)
    catgif = await make_gif(event, catfile, quality, fps)
    sandy = await event.client.send_file(
        event.chat_id,
        catgif,
        support_streaming=True,
        force_document=False,
        reply_to=reply_to_id,
    )
    await _catutils.unsavegif(event, sandy)
    await catevent.delete()
    for files in (catgif, catfile):
        if files and os.path.exists(files):
            os.remove(files)





@iqthon.iq_cmd(
    pattern="تحويل متحركه(?: |$)((-)?(r|l|u|d|s|i)?)$",
    command=("itog", plugin_category),
    info={
        "header": "To convert replied image or sticker to gif",
        "description": "Bt deafualt will use -i as flag",
        "flags": {
            "-r": "Right rotate gif.",
            "-l": "Left rotate gif.",
            "-u": "Rotates upward gif.",
            "-d": "Rotates downward gif.",
            "-s": "spin the image gif.",
            "-i": "invert colurs gif.",
        },
        "usage": [
            "{tr}itog <flag>",
        ],
        "examples": ["{tr}itog s", "{tr}itog -s"],
    },
)
async def pic_gifcmd(event):  # sourcery no-metrics
    "To convert replied image or sticker to gif"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edit_delete(event, "**⌔︙قم بالـرد على صـورة أو ملصـق لجعلهـا صـورة متحرڪـة **")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edit_delete(
            event,
            "**⌔︙قم بالـرد على صـورة أو ملصـق لجعلهـا صـورة متحرڪـة، الملصقـات المتحرڪـة غيـر مدعومـة !**",
        )
    args = event.pattern_match.group(1)
    args = "i" if not args else args.replace("-", "")
    catevent = await edit_or_reply(event, "**⌔︙جـاري صنـع صـورة متحرڪـة من الوسائـط التي قمـت بالـرد عليهـا ↯**")
    imag = await _cattools.media_to_pic(event, reply, noedits=True)
    if imag[1] is None:
        return await edit_delete(
            imag[0], "**⌔︙تعـذّر إستخـراج الصـورة من الرسالـة التي تـم الـرّد عليهـا ✕**"
        )
    image = Image.open(imag[1])
    w, h = image.size
    outframes = []
    try:
        if args == "r":
            outframes = await r_frames(image, w, h, outframes)
        elif args == "l":
            outframes = await l_frames(image, w, h, outframes)
        elif args == "u":
            outframes = await ud_frames(image, w, h, outframes)
        elif args == "d":
            outframes = await ud_frames(image, w, h, outframes, flip=True)
        elif args == "s":
            outframes = await spin_frames(image, w, h, outframes)
        elif args == "i":
            outframes = await invert_frames(image, w, h, outframes)
    except Exception as e:
        return await edit_delete(catevent, f"**⌔︙خطـأ ⚠️**\n__{str(e)}__")
    output = io.BytesIO()
    output.name = "Output.gif"
    outframes[0].save(output, save_all=True, append_images=outframes[1:], duration=0.7)
    output.seek(0)
    with open("Output.gif", "wb") as outfile:
        outfile.write(output.getbuffer())
    final = os.path.join(Config.TEMP_DIR, "output.gif")
    output = await vid_to_gif("Output.gif", final)
    if output is None:
        await edit_delete(
            catevent, "**⌔︙حـدث خطـأ مـا في الوسائـط، لا أستطيـع تحويلهـا إلى صـورة متحرڪـة !**"
        )
        for i in [final, "Output.gif", imag[1]]:
            if os.path.exists(i):
                os.remove(i)
        return
    sandy = await event.client.send_file(event.chat_id, output, reply_to=reply)
    await _catutils.unsavegif(event, sandy)
    await catevent.delete()
    for i in [final, "Output.gif", imag[1]]:
        if os.path.exists(i):
            os.remove(i)


@iqthon.iq_cmd(
    pattern="تحويل فديو متحركه ?([0-9.]+)?$",
    command=("vtog", plugin_category),
    info={
        "header": "Reply this command to a video to convert it to gif.",
        "description": "By default speed will be 1x",
        "usage": "{tr}vtog <speed>",
    },
)
async def _(event):
    "⌔︙قم بالـرد على فيديـو لجعلـه صـورة متحرڪـة ✦"
    reply = await event.get_reply_message()
    mediatype = media_type(event)
    if mediatype and mediatype != "video":
        return await edit_delete(event, "⌔︙حـدث خطـأ مـا في الوسائـط، لا أستطيـع تحويلهـا إلى صـورة متحرڪـة !")
    args = event.pattern_match.group(1)
    if not args:
        args = 2.0
    else:
        try:
            args = float(args)
        except ValueError:
            args = 2.0
    catevent = await edit_or_reply(event, "⌔︙جـاري التحويـل إلى صـورة متحرڪة انتضر دقائق  ↯")
    inputfile = await reply.download_media()
    outputfile = os.path.join(Config.TEMP_DIR, "vidtogif.gif")
    result = await vid_to_gif(inputfile, outputfile, speed=args)
    if result is None:
        return await edit_delete(event, "⌔︙غيـر قـادر على تحويلهـا إلى صـورة متحرڪة !")
    sandy = await event.client.send_file(event.chat_id, result, reply_to=reply)
    await _catutils.unsavegif(event, sandy)
    await catevent.delete()
    for i in [inputfile, outputfile]:
        if os.path.exists(i):
            os.remove(i)
