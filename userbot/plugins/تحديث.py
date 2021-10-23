import asyncio
import os
import sys
from asyncio.exceptions import CancelledError

import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import HEROKU_APP, UPSTREAM_REPO_URL, iqthon

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import delgvar

plugin_category = "tools"
cmdhd = Config.COMMAND_HAND_LER

LOGS = logging.getLogger(__name__)
# -- Constants -- #

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting heroku application"
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)


# -- Constants End -- #

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**⌔︙مطـور تـليثون العـرب قام بأضافـة ⚛️ : [{ac_br}]:\n\n⌔︙التغـيرات هيـة 🛃 :**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("**⌔︙ سجل التغيير كبير جدًا ، اعرض الملف لرؤيته.**")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    sandy = await event.edit(
        " ⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` " "⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` "
    )
    await event.client.reload(sandy)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is None:
        return await event.edit("⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` ")
    heroku = heroku3.from_key(HEROKU_API_KEY)
    heroku_app = None
    heroku_applications = heroku.apps()
    if HEROKU_APP_NAME is None:
        await event.edit(
            "⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` "
            
        )
        repo.__del__()
        return
    for app in heroku_applications:
        if app.name == HEROKU_APP_NAME:
            heroku_app = app
            break
    if heroku_app is None:
        await event.edit(
            f"{txt}\n" "⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` "
        )
        return repo.__del__()
    sandy = await event.edit(
        "⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` "
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS.error(e)
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace(
        "https://", "https://api:" + HEROKU_API_KEY + "@"
    )
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**⌔︙عذرا هناك خطأ ⁉️ :**\n`{error}`")
        return repo.__del__()
    build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build_status.status == "failed":
        return await edit_Delete(
            event, "`Build failed!\n" "⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` "
        )
    try:
        remote.push("master:main", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` ")
        return repo.__del__()
    await event.edit("⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` ")
    delgvar("ipaddress")
    try:
        await event.client.disconnect()
        if HEROKU_APP is not None:
            HEROKU_APP.restart()
    except CancelledError:
        pass

@iqthon.on(admin_cmd(pattern="تحديث الان(?: |$)(.*)"))    
async def upstream(event):
    event = await edit_or_reply(event, "⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` ")
    off_repo = "https://github.com/telethon-Arab/teletho-help"
    os.chdir("/app")
    try:
        txt = "⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` "
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n**⌔︙ الدليل {error} غير موجود **")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n**⌔︙فشـل مبڪـر ϟ : {error}`**")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("**⌔︙جـاري تحديث تليثون العرب  ، يرجـى الإنتـظار ↺**")
    await deploy(event, repo, ups_rem, ac_br, txt)


