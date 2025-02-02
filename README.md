# Telegram Backup Bot

## Features

- 🔐 **Secure Backups**: Automatically archives specified directories and files.
- ⏳ **Scheduled Tasks**: Backups run on a customizable schedule (default: 8:30 AM & 8:30 PM).
- 📤 **Telegram Integration**: Sends backups to your specified chat or thread via Telegram.
- ✅ **Easy Configuration**: Customize what to back up, Telegram IDs, and time zones.

## Installation

### Requirements

- Python 3.7+
- Pip (Python package manager)
- Telegram bot API token
- Telegram client APT id & API hash
- MySQL database (if database backups are required)

### Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/d1manpro/backup-telegram-bot.git
cd backup-telegram-bot
```

#### 2. Install Dependencies

The script automatically installs required Python packages on startup. Alternatively, you can manually install them:

```bash
pip install aiogram apscheduler telethon pytz
```

#### 3. Configure the Bot

Edit the script variables to suit your environment:

- **BOT SETTINGS**:
  - `TOKEN`: Your Telegram Bot token provided by BotFather.
  - `ADMIN_IDS`: A list of Telegram user IDs that are allowed to control the bot.
  - `DEFAULT_CHAT_ID`: The Telegram chat ID where backups will be sent.
  - `DEFAULT_THREAD_ID`: Default thread ID for specific topics (set to `None` if not applicable).
  - `API_ID` and `API_HASH`: Telegram API credentials required for integrations such as file uploads.
  - `SEND_ARCHIVE_ON_START`: A flag indicating whether to send an archive on bot startup.

- **DATABASE SETTINGS**:
  - Set the database host, port, user, and password for MySQL backups.

- **BACKUP SETTINGS**:
  - `TIMEZONE`: Set your timezone.
  - `directories_to_backup`: Directories to include in the backup.
  - `files_to_backup`: Specific files to include in the backup.
  - `databases_to_backup`: Databases to back up (optional).

#### 4. Enable Backup on Startup (Optional)

To enable the bot to send a backup immediately upon startup, set the `SEND_ARCHIVE_ON_START` variable to `True` in the script configuration:

```python
SEND_ARCHIVE_ON_START = True
```

> **⚠️ Note:** Before enabling this feature, ensure that `DEFAULT_CHAT_ID` and `DEFAULT_THREAD_ID` are properly configured. If these values are not set, the bot may fail to start and throw an error.

#### 5. Run the Bot

Use the following command to start the bot:

```bash
python3 backup.py
```

## Usage

### Commands

- **/start**: Verify bot functionality and view your Chat ID and Thread ID.
- **/backup**: Trigger a manual backup and send it to the default chat/thread.

### Scheduled Backups

Backups are scheduled to run at:

- **8:30 AM**
- **8:30 PM**

Modify the `BACKUP_SCHEDULE_TIMES` list in the script to adjust the schedule:

```python
BACKUP_SCHEDULE_TIMES = [
    {"hour": 8, "minute": 30},  # 8:30 AM
    {"hour": 20, "minute": 30}, # 8:30 PM
]
```

## Advanced Configuration

### Excluding Directories

Update the `EXCLUDED_DIRS` list to skip unwanted directories during backups:

```python
EXCLUDED_DIRS = ['.cache', '__pycache__', '.local', '.idea']
```

### Maximum File Size

By default, files larger than **19 MB** are sent using `TelegramClient`, as Telegram's bots have a strict limit of **20 MB** per file. For this reason, it is **highly recommended not to change this parameter** to avoid upload errors when sending backups.

Additionally, it is important to note that:

1. **Non-premium Telegram accounts** cannot send files larger than **2 GB**.
2. **Premium Telegram accounts** increase this limit to **4 GB**.

Regardless of configuration, the bot will not be able to send files exceeding these limits due to Telegram's inherent restrictions. Adjust your backup strategy to ensure files fall within these bounds.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.

## Contribution

🙋️‍♂️ **Have ideas or found a bug?** Don’t hesitate to reach out! Your feedback is invaluable for improving this bot.

## Author

Hello! I’m d1manpro. I’m 16 years old, a DevOps and T-shaped developer. You can learn more about me on my website.

For any questions, feel free to contact me on Telegram:

[![Telegram](https://img.shields.io/badge/Telegram-Contact-blue?logo=telegram)](https://t.me/dpdevops)
[![Website](https://img.shields.io/badge/Website-Visit-green?logo=link)](https://dp-dev.ru)
