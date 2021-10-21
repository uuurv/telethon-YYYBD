import random

from userbot import iqthon

from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event

plugin_category = "utils"

kno = [
    "100% تحبك وتخاف عليك",
    "100% يحبج ويخاف عليج",
    "91% جـزء من گـلبه ",
    "81% تموت عليك ههاي ",
    "81% يموت عليج ههذا ",
    "هاه اخي ؟  🏳‍🌈",
    "40% واحد حيوان ومصلحه عوفه ",
    "50% شوف شعندك وياه ",
    "30% خاين نصحيا عوفيه ميفيدج ",
    "25% مصادق غيرج ويكلج احبج",
    "25% واحد كلب ابن كلب عوفه",
    "0% يكهرك ",
    "0% تكرهك ",
]

arb = [
    "100%",
    "99%",
    "98%",
    "97%",
    "96%",
    "95%",
    "90%",
    "89%",
    "88%",
    "87%",
    "86%",
    "85%",
    "80%",
    "79%",
    "78%",
    "77%",
    "76%",
    "75%",
    "70%",
    "69%",
    "68%",
    "67%",
    "66%",
    "65%",
    "60%",
    "59%",
    "58%",
    "57%",
    "56%",
    "55%",
    "50%",
    "48%",
    "47%",
    "46%",
    "45%",
    "40%",
    "39%",
    "38%",
    "37%",
    "36%",
    "35%",
    "30%",
    "29%",
    "28%",
    "27%",
    "25%",
    "20%",
    "19%",
    "18%",
    "17%",
    "16%",
    "15%",
    "10%",
    "9%",
    "8%",
    "7%",
    "6%",
    "5%",
    "4%",
    "3%",
    "2%",
    "1%",
    "0%",
    "@iqthon",

]

@iqthon.iq_cmd(
    pattern="نسبه الحب(?:\s|$)([\s\S]*)",
    command=("نسبه الحب", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    iqth = user.first_name.replace("\u2060", "") if user.first_name else user.username
    iqt = random.choice(kno)
    await edit_or_reply(
        mention, f"⌔︙ نـسـبتكم انـت و [{iqth}](tg://user?id={user.id}) هـي {iqt} 😔🖤"
    )


@iqthon.iq_cmd(
    pattern="نسبه الانوثه(?:\s|$)([\s\S]*)",
    command=("نسبه الانوثه", plugin_category),
)
async def permalink(mention):
    """"""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    iqth = user.first_name.replace("\u2060", "") if user.first_name else user.username
    iqt = random.choice(arb)
    await edit_or_reply(
        mention, f"⌔︙ نسبه الانوثه لـ [{iqth}](tg://user?id={user.id}) هـي {iqt} 🤰"
    )


@iqthon.iq_cmd(
    pattern="نسبه الغباء(?:\s|$)([\s\S]*)",
    command=("نسبة الغباء", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    iqth = user.first_name.replace("\u2060", "") if user.first_name else user.username
    iqt = random.choice(arb)
    await edit_or_reply(
        mention, f"⌔︙ نسبه الغباء لـ [{iqth}](tg://user?id={user.id}) هـي {iqt} 😂💔"
    )
@iqthon.iq_cmd(
    pattern="نسبه الانحراف(?:\s|$)([\s\S]*)",
    command=("نسبة الانحراف", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    iqth = user.first_name.replace("\u2060", "") if user.first_name else user.username
    iqt = random.choice(arb)
    await edit_or_reply(
        mention, f"⌔︙ نسبة الانحراف لـ [{iqth}](tg://user?id={user.id}) هـي {iqt} 🥵🖤"
    )
@iqthon.iq_cmd(
    pattern="نسبه المثليه(?:\s|$)([\s\S]*)",
    command=("نسبة المثليه", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    iqth = user.first_name.replace("\u2060", "") if user.first_name else user.username
    iqt = random.choice(arb)
    await edit_or_reply(
        mention, f"⌔︙ نسبه المثليه لـ [{iqth}](tg://user?id={user.id}) هـي {iqt} 🤡 🏳️‍🌈."
        
    )  
@iqthon.iq_cmd(
    pattern="نسبه النجاح(?:\s|$)([\s\S]*)",
    command=("نسبه النجاح", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    iqth = user.first_name.replace("\u2060", "") if user.first_name else user.username
    iqt = random.choice(arb)
    await edit_or_reply(
        mention, f"⌔︙ نسبه النجاح لـ [{iqth}](tg://user?id={user.id}) هـي {iqt} 🤓."
        
    )  
@iqthon.iq_cmd(
    pattern="نسبه الكراهيه(?:\s|$)([\s\S]*)",
    command=("نسبه الكراهيه", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    iqth = user.first_name.replace("\u2060", "") if user.first_name else user.username
    iqt = random.choice(arb)
    await edit_or_reply(
        mention, f"⌔︙ نسبه الكراهيه لـ [{iqth}](tg://user?id={user.id}) هـي {iqt} 🤮."
        
    )     
