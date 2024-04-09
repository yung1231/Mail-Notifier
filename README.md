# Gmail to Telegram Notifier
This is a Python script that sets up a Telegram bot to monitor your Gmail inbox and send notifications to a specified Telegram chat when new emails arrive. The bot will send the sender's name and the email snippet to the chat.

## Prerequisites
Before running this script, you'll need to:
1. Create a Telegram bot and obtain its `API token`. You can follow the instructions [here](https://core.telegram.org/bots/tutorial) to create a new bot.
2. Enable the Gmail API for your Google account and download the `credentials.json` file. You can follow the instructions [here](https://developers.google.com/gmail/api/quickstart/python) to set up the Gmail API.
3. Install the required Python packages:
```shell
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

pip install pyTelegramBotAPI
```

## Setup
1. Clone this repository or download the source code.
2. Create a new file named `.env` in the project directory and add the following lines, replacing `YOUR_TELEGRAM_BOT_TOKEN` and `CHAT_ID` with your actual Telegram bot token and chat ID.
3. Place the `credentials.json` file you downloaded earlier in the project directory.

## Usage
1. Run the script with `python main.py`.
2. The first time you run the script, it will prompt you to authenticate with your Google account and grant access to the Gmail API.
3. Once authenticated, the script will start monitoring your Gmail inbox for new emails.
4. When a new email arrives, the bot will send a notification to the specified Telegram chat with the sender's name and the email snippet.

## Notes
- The script stores the IDs of processed emails in a set to avoid sending duplicate notifications.
- Error handling and logging are currently minimal. You may want to enhance these aspects for production use.

## License
This project is licensed under the [MIT License](LICENSE).