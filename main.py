import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_ROLE_IDS = [
    1547803947295580240,
    1533463569683845160,
    1533463570564649121
]

def has_allowed_role():
    async def predicate(ctx):
        if ctx.author == ctx.guild.owner:
            return True
        return any(role.id in ALLOWED_ROLE_IDS for role in ctx.author.roles)
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")

# أمر الحذف بالرد على رسالة الشخص
@bot.command(name="حذف")
@has_allowed_role()
async def clear_messages(ctx, limit: int = 10):
    # التحقق من أن المستخدم قام بعمل Reply (رد) على رسالة شخص
    if not ctx.message.reference or not ctx.message.reference.message_id:
        await ctx.reply("يرجى الرد (Reply) على رسالة الشخص المطلوب وحذف رسائله.", delete_after=5, mention_author=True)
        return

    if limit > 100:
        await ctx.reply("عذراً، لا يمكن حذف أكثر من 100 رسالة دفعة واحدة.", delete_after=5, mention_author=True)
        return

    try:
        # جلب الرسالة التي تم الرد عليها لمعرفة صاحبها
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        target_user = referenced_message.author
    except discord.NotFound:
        await ctx.reply("لم يتم العثور على الرسالة المستهدفة.", delete_after=5, mention_author=True)
        return

    # حذف رسالة الأمر نفسها لتنظيف الشات
    await ctx.message.delete()

    # دالة للتحقق من رسائل العضو المستهدف فقط
    def is_target_user_message(message):
        return message.author.id == target_user.id

    # البحث في السجل وحذف العدد المطلوب من رسائل هذا الشخص فقط
    deleted = await ctx.channel.purge(limit=limit * 5, check=is_target_user_message)
    
    # اقتصار العدد المحذوف على الحد المطلوب بدقة
    final_deleted_count = len(deleted[:limit])

    await ctx.reply(f"تم حذف {final_deleted_count} رسالة تخص العضو {target_user.mention} بنجاح.", delete_after=4, mention_author=True)

@clear_messages.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("عذراً، لا تملك الصلاحية (الرتبة المخصصة) لاستخدام هذا الأمر.", delete_after=4, mention_author=True)

bot.run(os.getenv("DISCORD_TOKEN"))
