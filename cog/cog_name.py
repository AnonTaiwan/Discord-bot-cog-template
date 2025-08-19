import discord
from discord.ext import commands
import logging
from datetime import datetime
import os

class CogName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.setup_logging()

    def setup_logging(self):
        """設置日誌系統"""
        # 創建 logs 目錄（如果不存在）
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # 設置日誌文件名（包含日期）
        log_filename = f'logs/fb_bot_{datetime.now().strftime("%Y%m%d")}.log'
        
        # 配置日誌格式
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # 配置日誌
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()  # 同時輸出到控制台
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("cog/cog_name.py: 日誌系統初始化完成")

    @commands.Cog.listener()
    async def on_ready(self):
        # 當 Cog 準備就緒時觸發
        self.channel = self.bot.get_channel(1354880766126985358) # 閒聊大廳
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