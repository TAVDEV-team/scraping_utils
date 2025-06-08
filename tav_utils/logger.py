"""
📦 logger.py — Reusable Logger for Any Python Project

This file gives you:
- ✅ Rotating file-based logging (5MB chunks, 3 backups)
- ✅ Pretty terminal + file formatting
- ✅ Drop-in logger per module: get_logger(__name__)
- ✅ Emoji-level cheat sheet for expressive logs

🔧 How to Use:

    from logger import get_logger
    logger = get_logger(__name__)

    logger.info("ℹ️ App initialized")
    logger.warning("⚠️ Disk space low")
    logger.error("❌ Couldn't connect to DB")

📚 === EMOJI LOGGER CHEAT SHEET ===

🔥 Basic Logging Levels with Emojis

| Level         | Emoji(s)                              | Vibe / Usage                                      |
|---------------|----------------------------------------|---------------------------------------------------|
| DEBUG         | 🐛 🔍 🧠 🛠️                          | Dev insights, bug hunting, internal values        |
| INFO          | ℹ️ ✅ 📘 🧾 🪄                         | Normal ops, tracking flow                         |
| SUCCESS       | ✅ 🎉 🟢 🚀 💯                         | Task done, ops success                            |
| WARNING       | ⚠️ 🟡 👀 🚧 🫣                         | Something fishy, not broken yet                   |
| ERROR         | ❌ 🔴 🛑 💥 🤬                         | Something failed, needs fix                       |
| CRITICAL      | 💣 🚨 🔥 😱 💀                        | System down, emergency!                         

🔮 Context-Specific Emojis

| Context             | Emoji(s)                        |
|---------------------|---------------------------------|
| API Call            | 🌐 📡 📲                        |
| Database            | 🗄️ 💾 📦                        |
| Authentication      | 🔐 🧑‍💻 🪪                      |
| File System         | 📁 📝 📂                        |
| Time/Delay          | ⏳ ⏰ 🕒                        |
| Start/Init          | 🟢 🚀 🛫                        |
| Shutdown/Exit       | 🔚 🛑 👋                        |
| Network/Proxy       | 🌍 🕸️ 🧱                       |
| Retry/Loop          | 🔁 ♻️ 🔄                       |
"""

import logging
import datetime
import os
from typing import List
from logging.handlers import RotatingFileHandler

# ========== 🎨 Formatter ==========
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# ========== 🗃️ Log File Path and Directory ==========
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # Create log directory if it doesn't exist
log_file = os.path.join(log_dir, "user_manager.log")

# ========== 🔧 Logger Factory Function ==========
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers (very important!)
    if not logger.handlers:
        # ========== 🗃️ Rotating File Handler ==========
        log_size = 5 * 1024 * 1024  # 5 MB
        fh = RotatingFileHandler(log_file, maxBytes=log_size, backupCount=3)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # ========== 🖥️ Optional: Terminal Output ==========
        # ch = logging.StreamHandler()
        # ch.setFormatter(formatter)
        # logger.addHandler(ch)

    return logger



def parse_log_line(line: str):
    """Extract timestamp and return parsed line info, or None if invalid."""
    if not line.startswith('['):
        return None, None
    
    try:
        date_str = line.split('] [')[0][1:]  # Extract 'YYYY-MM-DD HH:MM:SS'
        log_time = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return log_time, line.strip()
    except Exception:
        return None, None


def filter_logs(
    file_path: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    level: str = None,
    page: str = None
) -> List[str]:
    """Filter log lines by time range, level, and page/module name."""
    results = []

    level_tag = f"[{level.upper()}]" if level else None
    page_tag = f"[{page.lower()}]" if page else None

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            log_time, clean_line = parse_log_line(line)
            if not log_time:
                continue
            if not (start_time <= log_time <= end_time):
                continue
            if level_tag and level_tag not in clean_line.upper():
                continue
            if page_tag and page_tag not in clean_line.lower():
                continue
            results.append(clean_line)

    return results



# # ==================== USAGE ==================== #

# if __name__ == "__main__":
#     start = datetime.datetime(2025, 5, 5,0,0,0)
#     till = datetime.datetime(2025, 5, 8,12,0,0)
#     # level = 'warning'
#     # page = 'main'

#     logs = filter_logs('logs/user_manager.log', start, till)

#     for log in logs:
#         print(log)
