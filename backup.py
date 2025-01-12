import subprocess
import sys

# Install requirements
def install_requirements():
    requirements = [
        "aiogram",
        "apscheduler",
        "telethon",
        "pytz"
    ]
    for package in requirements:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install_requirements()

import asyncio
import logging
import os
import time
import zipfile
import shutil
import pytz
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import TelegramClient

# Sensitive data (replace with your own values)
TOKEN = 'YOUR_BOT_TOKEN'          # Telegram API token for the bot
ADMIN_ID = 123456789              # Telegram ID of the bot admin
DEFAULT_CHAT_ID = -1001234567890  # Default chat ID for sending archives
DEFAULT_THREAD_ID = 1             # Default thread ID for specific Telegram topics (if applicable)
API_ID = 12341234                 # API ID for Telegram (used for certain integrations)
API_HASH = 'YOUR_API_HASH'        # API hash for Telegram (used for certain integrations)

# Parameters
archive_path = ""                 # Path to the archive
backup_dir = "backup_temp"        # Temporary directory for archive creation
TIMEZONE = "Example/Timezone"     # Timezone for scheduler and filename

# Bot objects
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Directories and files to back up
directories_to_backup = {
    "/path/to/your/directory": "dir_backup",  # Replace with the directory path to back up
}

files_to_backup = {
    "~/example.conf": "configs/example.conf", # Replace with the file path to back up
    "/usr/bin/your_script": "scripts/your_script.sh" # Replace with the file path to back up
}

def expand_path(path):
    """Expand user home paths"""
    return os.path.expanduser(path)

def create_archive():
    """Create a zip archive of specified files and directories"""
    global archive_path
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d_%H-%M-%S")
    archive_path = os.path.join(backup_dir, f"backup_{os.uname().nodename}_{timestamp}.zip")

    with zipfile.ZipFile(archive_path, 'w') as archive:
        for src, dest in directories_to_backup.items():
            src = expand_path(src)
            if os.path.exists(src):
                for root, dirs, files in os.walk(src):
                    dirs[:] = [d for d in dirs if d not in ['.cache', '__pycache__', '.local', '.idea']]
                    if backup_dir in root:
                        continue
                    for file in files:
                        full_path = os.path.join(root, file)
                        arc_path = os.path.relpath(full_path, src)
                        archive.write(full_path, os.path.join(dest, arc_path))

        for src, dest in files_to_backup.items():
            src = expand_path(src)
            if os.path.exists(src):
                archive.write(src, dest)

        if os.path.exists(__file__):
            archive.write(__file__, os.path.basename(__file__))
        logging.info("Archive created")


async def send_archive_via_client(target_chat_id, target_thread_id, log_msg):
    """Send the archive to the Telegram chat"""
    log_text = "Connecting to Telegram-Client"
    await log_msg.edit_text(log_text)
    logging.info(log_text)

    client = TelegramClient("client_session", API_ID, API_HASH)
    await client.start(bot_token=TOKEN)

    log_text = "Sending the archive via Telegram-Client"
    await log_msg.edit_text(log_text)
    logging.info(log_text)

    async with client:
        if os.path.exists(archive_path):
            try:
                await client.send_file(
                    target_chat_id,
                    archive_path,
                    caption=archive_path,
                    reply_to=target_thread_id if target_thread_id else None
                )
                await log_msg.delete()
                logging.info(
                    f"Archive {archive_path.replace('backup_temp/', '')} successfully sent to chat {target_chat_id} in thread {target_thread_id}.")
            except Exception as e:
                logging.error(f"Error sending archive: {e}")


def delete_archive():
    """Delete the backup directory and its contents"""
    shutil.rmtree(backup_dir, ignore_errors=True)

async def send_archive_task(message = None):
    """Run the full backup task"""
    target_chat_id = message.chat.id if message else DEFAULT_CHAT_ID
    target_thread_id = message.message_thread_id if message else DEFAULT_THREAD_ID

    log_msg = await bot.send_message(target_chat_id, "Building an archive...", message_thread_id=target_thread_id)
    create_archive()

    await send_archive_via_client(target_chat_id, target_thread_id, log_msg)

    delete_archive()

async def start_scheduler():
    """Schedule the archive task to run at specified times"""
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(send_archive_task, 'cron', hour=8, minute=30)   # Scheduled at 8:30 AM
    scheduler.add_job(send_archive_task, 'cron', hour=20, minute=30)  # Scheduled at 8:30 PM
    scheduler.start()

@dp.message(CommandStart())
async def start(message: Message):
    """Handle the /start command"""
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer(
        f"The /start command has been successfully processed. ChatID <code>{message.chat.id}</code>, ThreadID <code>{message.message_thread_id}</code>",
        parse_mode="html")

@dp.message(Command('backup'))
async def backup_command(message: Message):
    """Handle the /backup command to manually trigger the backup"""
    if message.from_user.id != ADMIN_ID:
        return
    await send_archive_task(message)

async def main():
    """Main function to start the bot and run initial tasks"""
    start_time = time.time()
    msg = await bot.send_message(ADMIN_ID, "SYSTEM: бот запущен. Проверка пинга...")
    end_time = time.time()
    ping = (end_time - start_time) * 1000
    log_text = f'SYSTEM: бот запущен. Пинг бота: {ping:.2f} ms'
    await msg.edit_text(log_text)
    logging.info(log_text)

    await start_scheduler()
    await send_archive_task()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d][%H:%M:%S',
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Exit')
