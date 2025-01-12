# Backup TG Bot

**Backup TG Bot** is a Telegram bot designed to automate the creation of backups for specified files and directories and send them to a designated chat. The bot supports scheduling, manual triggers, and automatic splitting of large archives.

## Features

- 📁 **Backup Files and Directories**: Archive specified files and directories defined in the configuration.
- ⏰ **Scheduling**: Perform backups at predefined times.
- 🛠️ **Manual Trigger**: Manually initiate a backup and send it immediately.
- 🗂️ **File Splitting**: Automatically split archives if their size exceeds Telegram's file limit (19 MB).
- 📤 **Send to Telegram**: Deliver archives (or their parts) to the specified chat.

## Installation

### Requirements

- Python 3.8+
- Telegram Bot API token ([create a bot here](https://core.telegram.org/bots#botfather))
- Your Telegram ID (for bot control)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/D1manPRO/backup-tg-bot.git
   cd backup-tg-bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Open the `bot.py` file.
   - Replace the following values:
     - `TOKEN`: Your Telegram Bot API token.
     - `ADMIN_ID`: Your Telegram user ID.
     - `CHAT_ID`: The chat ID where backups will be sent.
     - `TIMEZONE`: Your timezone for scheduling backups.

4. Specify files and directories to back up:
   - Update the `directories_to_backup` and `files_to_backup` dictionaries with the paths you want to include.

5. Run the bot:

   ```bash
   python bot.py
   ```

## Usage

### Commands

- **`/start`**: Initialize the bot. Displays Chat ID and Thread ID (if applicable).
- **`/backup`**: Manually trigger the creation and sending of a backup.

### Scheduling Backups

The bot is preconfigured to run backups at 8:30 AM and 8:30 PM in the specified timezone. To modify these times, edit the `start_scheduler` function in `bot.py`.

### File Splitting

If an archive exceeds 19 MB, it will be automatically split into smaller parts. To recombine these parts, use the following command:

```bash
cat backup_<hostname>_part_* > backup_<hostname>.zip
```

## Deployment

### Local Deployment

Run the bot locally using the following command:

```bash
python bot.py
```

### Server Hosting

For continuous operation, deploy the bot on a server or cloud platform such as AWS, Heroku, or DigitalOcean.

### Docker Deployment (Optional)

1. Create a `Dockerfile`:

   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY . .
   RUN pip install --no-cache-dir -r requirements.txt
   CMD ["python", "bot.py"]
   ```

2. Build and run the container:

   ```bash
   docker build -t backup-tg-bot .
   docker run -d backup-tg-bot
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

## Author

Developed by [D1manPRO](https://github.com/D1manPRO). Contact me on [Telegram](https://t.me/dpdevops) for any inquiries.
