import discord
from discord.ext import commands
import asyncio
import os
from time import sleep
import logging
from datetime import datetime, timedelta, date, time
from pathlib import Path
import json

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())  # 危險設定，僅供示範與個人測試用
        self.date = datetime.now().strftime("%Y%m%d")
        self.initial_extensions = []
        for p in Path("./cog").iterdir():
            if p.suffix == ".py":
                self.initial_extensions.append(f"cog.{p.stem}")

    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")
        self.remove_command("help")
        self.loop.create_task(self.auto_shutdown_at_midnight())

    def load_extensions(self):
        for ext in self.initial_extensions:
            try:
                self.load_extension(ext)
                print(f"✅ 已加載擴展: {ext}")
            except Exception as e:
                print(f"❌ 無法加載擴展 {ext}: {e}")

    async def auto_shutdown_at_midnight(self):
        now = datetime.now()
        # 算到下個 0 點還有幾秒
        tomorrow = datetime.combine(date.today() + timedelta(days=1), time.min)
        seconds_to_midnight = (tomorrow - now).seconds
        print(f"將於 {seconds_to_midnight + 5:,} 秒後自動關機")
        await asyncio.sleep(seconds_to_midnight + 5)
        print('每日12點自動關機')
        for ext in self.initial_extensions:
            self.unload_extension(ext)
            print(f"✅ 已卸載擴展: {ext}")
        await self.close()


def setup_daily_logger():
    """設定每日日誌"""
    # 清除現有的 handlers
    logging.getLogger().handlers.clear()
    
    # 創建日誌目錄
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_dir = Path('logs')
    if not log_dir.is_dir():
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # 設定日誌檔案名稱
    log_file = log_dir / f'fb_bot_{datetime.now():%Y%m%d}.log'
    
    # 重新配置日誌
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ],
        force=True  # 強制重新設定
    )
    
    return logging.getLogger()

async def main():
    with open("JSON/bot.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    TOKEN = config.get("TOKEN")

    logger = None
    current_date = None
    while True:
        now = datetime.now()
        today = now.strftime("%Y%m%d")
        
        # 檢查是否需要更新日誌檔案
        if current_date != today:
            logger = setup_daily_logger()
            current_date = today
            logger.info(f"日誌系統已更新至 {today}")
            
        async with MyBot() as bot:
            bot.load_extensions()
            await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())