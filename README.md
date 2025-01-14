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

### Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/d1manpro/backup-telegram-bot.git
cd backup-telegram-bot
```

#### 2. Dependencies

The bot automatically installs all required dependencies (e.g., `aiogram`, `apscheduler`) during startup.

#### 3. Configure the Bot

Edit the following variables in the script to suit your environment:

- **TOKEN**: Your bot’s Telegram API token.
- **ADMIN\_ID**: Your Telegram user ID (only you can control the bot).
- **DEFAULT\_CHAT\_ID**: ID of the Telegram chat where backups will be sent.
- **DEFAULT\_THREAD\_ID**: ID of the thread for sending backups (set to `None` if not applicable).
- **API\_ID** and **API\_HASH**: Your Telegram API credentials.
- **TIMEZONE**: Your local timezone for scheduling tasks.
- **directories\_to\_backup**: Directories to include in the backup.
- **files\_to\_backup**: Specific files to include in the backup.

#### 4. Enable Backup on Startup (Optional)

If you want the bot to send a backup immediately upon startup, uncomment the following line in the `main()` function of the script:

```python
# await send_archive_task()
```

> **⚠️ Note:** Before enabling this feature, make sure you have correctly configured `DEFAULT_CHAT_ID` and `DEFAULT_THREAD_ID`. If these values are not set, the bot will fail to start and throw an error.

#### 5. Run the Bot

Use the following command to start the bot:

```bash
python3 backup.py
```

## Usage

### Commands

- **/start**: Verify bot functionality and view your Chat ID and Thread ID.
- **/backup**: Trigger a manual backup and send it to the default chat/thread.

### Scheduling Backups

Backups run automatically at the following times:

- **8:30 AM**
- **8:30 PM**

You can adjust these times by modifying the `start_scheduler()` function:

```python
scheduler.add_job(send_archive_task, 'cron', hour=8, minute=30)
scheduler.add_job(send_archive_task, 'cron', hour=20, minute=30)
```

You can also change the number of backups per day by adding more `add_job` lines or removing existing ones.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.

## Contribution

🙋️‍♂️ **Have ideas or found a bug?** Don’t hesitate to reach out! Your feedback is invaluable for improving this bot.

## Author

Hello! I’m d1manpro. I’m 16 years old, a DevOps and T-shaped developer. You can learn more about me on my website.

For any questions, feel free to contact me on Telegram:

[![Telegram](https://img.shields.io/badge/Telegram-Contact-blue?logo=telegram)](https://t.me/dpdevops)
[![Website](https://img.shields.io/badge/Website-Visit-green?logo=link)](https://dp-dev.ru)
