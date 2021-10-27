import os
from pathlib import Path

from ..Config import Config
from ..utils import load_module, remove_plugin
from . import CMD_HELP, CMD_LIST, SUDO_LIST, iqthon, edit_delete, edit_or_reply, reply_id

plugin_category = "tools"

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@iqthon.iq_cmd(
    pattern="تحميل ملف$",
    command=("تحميل ملف", plugin_category),
    info={
        "header": "To install an external plugin.",
        "description": "Reply to any external plugin(supported by cat) to install it in your bot.",
        "usage": "{tr}install",
    },
)
async def install(event):
    "To install an external plugin."
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "userbot/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await edit_delete(
                    event,
                    f"**⌔︙ تم تثبيـت الملـف بنجـاح ✓** `{os.path.basename(downloaded_file_name)}`",
                    10,
                )
            else:
                os.remove(downloaded_file_name)
                await edit_delete(
                    event, "**⌔︙حـدث خطـأ، هـذا الملف مثبـت بالفعـل !**", 10
                )
        except Exception as e:
            await edit_delete(event, f"**⌔︙خطـأ ⚠️:**\n`{str(e)}`", 10)
            os.remove(downloaded_file_name)


@iqthon.iq_cmd(
    pattern="تثبيت ثاني ([\s\S]*)",
    command=("تثبيت ثاني", plugin_category),
    info={
        "header": "To load a plugin again. if you have unloaded it",
        "description": "To load a plugin again which you unloaded by {tr}unload",
        "usage": "{tr}load <plugin name>",
        "examples": "{tr}load markdown",
    },
)
async def load(event):
    "To load a plugin again. if you have unloaded it"
    shortname = event.pattern_match.group(1)
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await edit_delete(event, f"**⌔︙تم التحميـل بنجـاح ✓** `{shortname}`", 10)
    except Exception as e:
        await edit_or_reply(
            event,
            f"**⌔︙لا يمڪـن التحميـل ⚠️** {shortname} بسـبب الخطـأ الآتـي ϟ :.\n{str(e)}",
        )





@iqthon.iq_cmd(
    pattern="حذف التثبيت ([\s\S]*)",
    command=("حذف التثبيت", plugin_category),
    info={
        "header": "To uninstall a plugin temporarily.",
        "description": "To stop functioning of that plugin and remove that plugin from bot.",
        "note": "To unload a plugin permanently from bot set NO_LOAD var in heroku with that plugin name, give space between plugin names if more than 1.",
        "usage": "{tr}uninstall <plugin name>",
        "examples": "{tr}uninstall markdown",
    },
)
async def unload(event):
    "To uninstall a plugin."
    shortname = event.pattern_match.group(1)
    path = Path(f"userbot/plugins/{shortname}.py")
    if not os.path.exists(path):
        return await edit_delete(
            event, f"**⌔︙لا يوجـد ملـف مـع مسـار ⚠️ {path} لإلغـاء التثبيـت ⊠**"
        )
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"**⌔︙ {shortname} تم إلغـاء التثبيـت بنجـاح ✓**")
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙تمـت الإزالـة بنجـاح ✓ : {shortname}\n{str(e)}**")
