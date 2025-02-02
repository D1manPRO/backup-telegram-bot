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
import zipfile
import shutil
import pytz
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import TelegramClient

# BOT SETTINGS
TOKEN = 'YOUR_BOT_TOKEN'            # Telegram bot token received from BotFather
ADMIN_IDS = [123456789, 987654321]  # Telegram IDs of the bot admins
DEFAULT_CHAT_ID = -1001234567890    # Default chat ID where archives will be sent
DEFAULT_THREAD_ID = 1               # Default thread ID for specific topics (if using threads in Telegram)
API_ID = 12341234                   # API ID for Telegram, used for certain integrations
API_HASH = 'YOUR_API_HASH'          # API hash for Telegram, used for certain integrations
SEND_ARCHIVE_ON_START = False       # Flag to determine if the bot should send an archive on startup

# DATABASE SETTINGS
DB_DATA = {
    "host": "example.com",          # Host address of the database
    "port": 3306,                   # Port for connecting to the database
    "user": "example_username",     # Username for database connection
    "password": "example_password"  # Password for database connection
}

# BACKUP SETTINGS
EXCLUDED_DIRS = ['.cache', '__pycache__', '.local', '.idea']  # List of directories to exclude from backup
MAX_FILE_SIZE = 19 * 1024 * 1024    # Maximum allowed file size (in bytes) for backups
archive_path = ""                   # Path to the archive file (leave empty to specify later)
backup_dir = "backup_temp"          # Temporary directory for creating backups
TIMEZONE = "Example/Timezone"       # Timezone for scheduling tasks and setting the backup filename
BACKUP_SCHEDULE_TIMES = [           # List of times (hour, minute) for scheduled backups
    {"hour": 8, "minute": 30},      # 8:30 AM
    {"hour": 20, "minute": 30},     # 8:30 PM
]

# FILE AND DIRECTORY BACKUP SETTINGS
directories_to_backup = {
    "/path/to/your/directory": "dir_backup",  # Replace with the directory path to back up
}

files_to_backup = {
    "~/example.conf": "configs/example.conf",            # Replace with the file path to back up
    "/usr/bin/your_script": "scripts/your_script.sh"     # Replace with the file path to back up
}

databases_to_backup = {
    "example": "db/example_export.sql",  # Replace with the database name and export file path
}

# Bot objects
bot = Bot(token=TOKEN)
dp = Dispatcher()

def expand_path(path):
    """Expand user home paths"""
    return os.path.expanduser(path)

def create_mysql_backup(database_name, output_path):
    """Exports data from mysql"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        dump_command = [
            "mysqldump",
            f"--host={DB_DATA['host']}",
            f"--port={DB_DATA['port']}",
            f"--user={DB_DATA['user']}",
            f"--password={DB_DATA['password']}",
            database_name
        ]
        with open(output_path, "w") as dump_file:
            process = subprocess.run(dump_command, stdout=dump_file, stderr=subprocess.PIPE, text=True)

        if process.returncode != 0:
            logging.error(f"Failed to export mysql for database {database_name}: {process.stderr}")
        else:
            logging.info(f"Database {database_name} successfully exported to {output_path}")
    except Exception as e:
        logging.error(f"Failed to export mysql for database {database_name}: {e}")

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
                    dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
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

        for db_name, db_path in databases_to_backup.items():
            temp_path = os.path.join(backup_dir, db_path)
            create_mysql_backup(db_name, temp_path)
            if os.path.exists(temp_path):
                archive.write(temp_path, db_path)

        if os.path.exists(__file__):
            archive.write(__file__, os.path.basename(__file__))
        logging.info("Archive created")

async def send_archive_via_client(target_chat_id, target_thread_id, log_msg):
    """Send the archive to the Telegram chat via Telegram-Client"""
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
                    caption=archive_path.replace(f'{backup_dir}/', '').replace("_", " ").replace(".zip", ""),
                    reply_to=target_thread_id if target_thread_id else None
                )
                await log_msg.delete()
                logging.info(
                    f"Archive {archive_path.replace(f'{backup_dir}/', '')} successfully sent to chat {target_chat_id} in thread {target_thread_id}.")
            except Exception as e:
                logging.error(f"Error sending archive: {e}")

async def send_archive_via_bot(target_chat_id, target_thread_id, log_msg):
    """Send the archive to the Telegram chat via Telegram-Bot"""
    log_text = "Sending the archive via Telegram-Bot"
    await log_msg.edit_text(log_text)
    logging.info(log_text)

    if os.path.exists(archive_path):
        try:
            document = FSInputFile(archive_path)
            await bot.send_document(
                chat_id=target_chat_id,
                document=document,
                caption=archive_path.replace(f'{backup_dir}/', '').replace("_", " ").replace(".zip", ""),
                message_thread_id=target_thread_id if target_thread_id else None
            )
            await log_msg.delete()
            logging.info(
                f"Archive {archive_path.replace(f'{backup_dir}/', '')} successfully sent via aiogram to chat {target_chat_id} in thread {target_thread_id}.")
        except Exception as e:
            logging.error(f"Error sending archive via aiogram: {e}")

def delete_archive():
    """Delete the backup directory and its contents"""
    shutil.rmtree(backup_dir, ignore_errors=True)

async def send_archive_task(message=None):
    """Run the full backup task"""
    target_chat_id = message.chat.id if message else DEFAULT_CHAT_ID
    target_thread_id = message.message_thread_id if message else DEFAULT_THREAD_ID

    log_msg = await bot.send_message(target_chat_id, "Building an archive...", message_thread_id=target_thread_id)
    create_archive()

    archive_size = os.path.getsize(archive_path)
    if archive_size <= MAX_FILE_SIZE:
        await send_archive_via_bot(target_chat_id, target_thread_id, log_msg)
    else:
        await send_archive_via_client(target_chat_id, target_thread_id, log_msg)

    delete_archive()

async def start_scheduler():
    """Schedule the archive task to run at specified times"""
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    for time_config in BACKUP_SCHEDULE_TIMES:
        scheduler.add_job(
            send_archive_task,
            'cron',
            hour=time_config['hour'],
            minute=time_config['minute']
        )
        logging.info(f"Backup task scheduled at {time_config['hour']:02}:{time_config['minute']:02}")
    scheduler.start()

@dp.message(CommandStart())
async def start(message: Message):
    """Handle the /start command"""
    if message.from_user.id not in ADMIN_IDS:
        return
    await message.answer(
        f"The /start command has been successfully processed. ChatID <code>{message.chat.id}</code>, ThreadID <code>{message.message_thread_id}</code>",
        parse_mode="html")

@dp.message(Command('backup'))
async def backup_command(message: Message):
    """Handle the /backup command to manually trigger the backup"""
    if message.from_user.id not in ADMIN_IDS:
        return
    await send_archive_task(message)

async def main():
    """Main function to start the bot and run initial tasks"""
    logging.info('SYSTEM: Bot is running')

    await start_scheduler()
    if SEND_ARCHIVE_ON_START:
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
