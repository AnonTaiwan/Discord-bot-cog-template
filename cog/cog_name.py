import discord
from discord.ext import commands
import utils

class CogName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.logger = utils.get_logger(__name__)
        self.logger.info("cog/cog_name.py: 日誌系統初始化完成")

    @commands.Cog.listener()
    async def on_ready(self):
        # 當 Cog 準備就緒時觸發
        self.channel = self.bot.get_channel(utils.OFFTOPIC_CHANNEL_ID) # 閒聊大廳
        self.logger.info(f'cog_name.cog: {self.bot.user} (ID: {self.bot.user.id}) Ready!')
        try:
            # await self.channel.send("CogName 已啟動！") # 發送準備就緒消息，僅供示範
            pass
        except Exception as e:
            self.logger.error(f"Error sending ready message: {e}")


    @discord.slash_command(name="example", description="這是一個範例指令")
    async def example_command(self, ctx: discord.ApplicationContext):
        try:
            await ctx.respond("這是一個範例指令的回應！")
            self.logger.info(f"cog_name.cog: {ctx.author} 使用了 /example 指令")
        except Exception as e:
            self.logger.info(f"cog_name.cog: {ctx.author} 嘗試使用 /example 指令時發生錯誤")
            self.logger.error(f"Error in example_command: {e}")
            await ctx.respond("發生錯誤，請稍後再試。", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(CogName(bot))