# 🗂️ Telegram Backup Bot 📦

A Python-based Telegram bot for creating and sending backups of specified files and directories. This bot is designed to automate backups and send them to a Telegram chat using scheduled tasks.

---

## 🚀 Features

- Automatically creates backups of specified files and directories.
- Scheduled backups twice a day (default: 08:30 AM and 08:30 PM).
- Sends backups to a Telegram chat or group.
- Manually trigger backups using the `/backup` command.
- Easy configuration and setup.

---

## 🛠️ Setup & Usage

### 🔧 Configuration

To set up the bot, edit the **`backup.py`** file and replace the following configuration variables with your values:

- `TOKEN` - Telegram bot API token.
- `ADMIN_ID` - Your Telegram ID (admin of the bot).
- `DEFAULT_CHAT_ID` - Default chat ID where the backups will be sent.
- `DEFAULT_THREAD_ID` - Default thread ID for topics in the Telegram chat (set `None` if not needed).
- `API_ID` & `API_HASH` - API credentials for Telethon client.
- `TIMEZONE` - Specify your timezone (e.g., `"Europe/London"`).

Also, configure the files and directories you want to back up:

- Add directories in `directories_to_backup`.
- Add individual files in `files_to_backup`.

### ▶️ Running the Bot

1. Save the file as `backup.py`.
2. Run the script:

```bash
python backup.py
```

The bot will automatically install all necessary dependencies.

---

## 🗂️ Commands

- `/start` - Initialize the bot (admin only).
- `/backup` - Manually trigger a backup (admin only).

---

## 📅 Scheduled Backups

The bot is configured to run backups at the following times:

- **08:30 AM**
- **08:30 PM**

Modify the schedule in the `start_scheduler` function if needed.

---

## 🔑 Permissions

Ensure the bot has sufficient permissions to send messages and upload files in the specified chat.

---

## 👨‍💻 About the Author

Created with ❤️ by [dpdevops](https://t.me/dpdevops).

Feel free to reach out to me via Telegram for any questions or feedback: [@dpdevops](https://t.me/dpdevops).
