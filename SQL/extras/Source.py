import re
import time
from datetime import datetime
from userbot import StartTime, iqthon
from userbot.Config import Config
from userbot.plugins import mention
help1 = ("**⎈ ⦙ كيفيه التنصيب :**")
help2 = ("**⎈ ⦙ قـائمـه الاوامـر :**\n**⎈ ⦙ قنـاه السـورس :** @IQTHON\n**⎈ ⦙ شـرح اوامـر السـورس : @L3LL3**\n**⎈ ⦙ شـرح فـارات السـورس : @TEAMTELETHON** ")
TG_BOT = Config.TG_BOT_USERNAME
TM = time.strftime("%I:%M")
ALIVE_TEXT = "𝗐𝖾𝗅𝖼𝗈𝗆𝖾 𝗍𝖾𝗅𝖾𝗍𝗁𝗈𝗇 𝖺𝗅 𝖺𝗋𝖺𝖻 𓃠"
EMOJI = "⎈ ⦙"
Sour = f"**{ALIVE_TEXT}**\n𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n**{EMOJI}  النسخـة :  ِ7.1 ** \n**{EMOJI} حسـابك  :   {mention} **\n**{EMOJI} الـوقت  : {TM} **\n**{EMOJI} البوت :** {TG_BOT}\n**{EMOJI} السـورس :** @IQTHON \n𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n"
