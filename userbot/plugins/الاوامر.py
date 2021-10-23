from userbot import iqthon

from ..core.managers import edit_or_reply

@iqthon.on(admin_cmd(pattern="الاوامر(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, "عذرا الامر قيد الصيانه حاليا لأضافه الاوامر الجديده حاليا الأوامر الشغاله هنا فقط \n https://t.me/M4_STORY")
@iqthon.on(admin_cmd(pattern="اعاده تشغيل(?: |$)(.*)"))    
async def iq(event):
    await edit_or_reply(event, " ⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` " "⌔︙ عـذرًا، الأمر لقد تغير قم بأرسال فقط  ⬅️ `.تحديث` ")
    
    

