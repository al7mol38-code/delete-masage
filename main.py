import os
import discord
from discord.ext import commands

# إعداد الصلاحيات (Intents) وتشغيل البوت مع بادئة الأوامر (!)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")

# أمر حذف عدد معين من الرسائل: !حذف 100
@bot.command(name="حذف")
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, limit: int = 10):
    if limit > 100:
        await ctx.send("عذراً، لا يمكن حذف أكثر من 100 رسالة دفعة واحدة.", delete_after=5)
        return
    
    # حذف الرسائل (يتم إضافة 1 لحذف رسالة الأمر نفسها)
    deleted = await ctx.channel.purge(limit=limit + 1)
    
    # رسالة تأكيد تختفي بعد 3 ثوانٍ
    await ctx.send(f"تم حذف {len(deleted) - 1} رسالة بنجاح.", delete_after=3)

# أمر حذف كل رسائل شخص معين منشنته: !حذف_الكل @الشخص
@bot.command(name="حذف_الكل")
@commands.has_permissions(manage_messages=True)
async def delete_user_messages(ctx, member: discord.Member):
    await ctx.message.delete() # حذف رسالة الأمر لتنظيف الشاشة
    
    # دالة للتحقق مما إذا كانت الرسالة تخص الشخص المحدد
    def is_user_message(message):
        return message.author.id == member.id

    # البحث في آخر 200 رسالة في القناة وحذف رسائل العضو فقط
    deleted = await ctx.channel.purge(limit=200, check=is_user_message)
    
    await ctx.send(f"تم حذف جميع رسائل العضو {member.mention} (عددها: {len(deleted)}) بنجاح.", delete_after=4)

# تشغيل البوت باستخدام متغير البيئة الحساس للحفاظ على الأمان
bot.run(os.getenv("DISCORD_TOKEN"))
