import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 数据存储目录
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 加密相关配置
ENCRYPTION_KEY_FILE = DATA_DIR / "encryption.key"
SECRET_KEY_FILE = DATA_DIR / "secret.key"

# 数据库文件
DATABASE_FILE = DATA_DIR / "passwords.db"

# TOTP配置
TOTP_ISSUER = "2FA Password Manager"
TOTP_DIGITS = 6
TOTP_INTERVAL = 30

# UI配置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
APP_TITLE = "2FA Password Manager"

# 日志配置
LOG_FILE = BASE_DIR / "app.log"
