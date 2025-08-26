from datetime import datetime
import json
import logging
import os
from pathlib import Path

# 專案路徑

ROOT_DIR = Path(__file__).resolve().parent
LOGS_DIR = ROOT_DIR / 'logs'
JSON_DIR = ROOT_DIR / 'JSON'
STATIC_DIR = ROOT_DIR / 'static'

# Bot 相關配置

BOT_CONFIG_FILE = JSON_DIR / 'bot.json'
try:
    with open(JSON_DIR / 'bot.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    BOT_TOKEN = config.get("DISCORD_BOT_TOKEN", "")
except Exception as e:
    print(f"Error reading {BOT_CONFIG_FILE}: {e}")

# Discord 相關配置

OFFTOPIC_CHANNEL_ID = 1354880766126985358  # 閒聊大廳

ADMIN_ROLE_ID = 1354875493610164255  # 管理員身份組

# 通用函數

def get_logger(name):
    """設置日誌系統"""
    # 創建 logs 目錄（如果不存在）
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # 設置日誌文件名（包含日期）
    log_filename = LOGS_DIR / f'bot_{datetime.now().strftime("%Y%m%d")}.log'
    
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
    
    return logging.getLogger(name)

def check_exist_or_create_json(logger: logging.Logger, file: Path, default_content: dict = {}):
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(default_content, f, ensure_ascii=False, indent=4)
        logger.info(f"{file} 不存在，已創建一個空的 {file}")
    else:
        logger.info(f"{file} 已存在")

def read_json(logger: logging.Logger, file: Path, default_content: dict = {}) -> dict:
    with open(file, 'r', encoding='utf-8') as f:
        try:
            content = json.load(f)
            logger.info(f"已成功讀取 {file}")
        except json.JSONDecodeError as e:
            logger.error(f"讀取 {file} 時發生錯誤: {e}")
            content = default_content
    return content

def write_json(logger: logging.Logger, file: Path, data: dict) -> bool:
    with open(file, 'w', encoding='utf-8') as f:
        try:
            json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"已成功寫入 {file}")
            return True
        except Exception as e:
            logger.error(f"寫入 {file} 時發生錯誤: {e}")
            return False