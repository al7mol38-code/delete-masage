import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# قائمة آيديkات الرتب المسموح لها باستخدام الأوامر
ALLOWED_ROLE_IDS = [
    1547803947295580240,
    1533463569683845160,
    1533463570564649121
]

# دالة للتحقق مما إذا كان العضو يمتلك إحدى الرتب المحددة
def has_allowed_role():
    async def predicate(ctx):
        # التحقق إذا كان الشخص هو صاحب السيرفر (اختياري، لضمان عدم منعه)
        if ctx.author == ctx.guild.owner:
            return True
        # التحقق من وجود إحدى الرتب ضمن رتب العضو
        return any(role.id in ALLOWED_ROLE_IDS for role in ctx.author.roles)
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")

# أمر حذف عدد معين من الرسائل: !حذف 100
@bot.command(name="حذف")
@has_allowed_role()
async def clear_messages(ctx, limit: int = 10):
    if limit > 100:
        await ctx.send("عذراً، لا يمكن حذف أكثر من 100 رسالة دفعة واحدة.", delete_after=5)
        return
    
    deleted = await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f"تم حذف {len(deleted) - 1} رسالة بنجاح.", delete_after=3)

# أمر حذف كل رسائل شخص معين منشنته: !حذف_الكل @الشخص
@bot.command(name="حذف_الكل")
@has_allowed_role()
async def delete_user_messages(ctx, member: discord.Member):
    await ctx.message.delete()
    
    def is_user_message(message):
        return message.author.id == member.id

    deleted = await ctx.channel.purge(limit=200, check=is_user_message)
    await ctx.send(f"تم حذف جميع رسائل العضو {member.mention} (عددها: {len(deleted)}) بنجاح.", delete_after=4)

# معالجة الخطأ في حال حاول شخص ليس لديه الرتبة استخدام الأمر
@clear_messages.error
@delete_user_messages.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("عذراً، لا تملك الصلاحية (الرتبة المخصصة) لاستخدام هذا الأمر.", delete_after=4)

bot.run(os.getenv("DISCORD_TOKEN"))
