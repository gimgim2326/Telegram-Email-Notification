import json
import os
import pathlib

# Load config data
config = json.load(open(pathlib.Path(__file__).parent / '../settings.json'))

mail_config = config['email']
mail_config['mail'] = os.environ['MAIL_USER']
mail_config['secret'] = os.environ['MAIL_PASSWORD']

telegram_config = {
        "bot_name": os.environ['TELEGRAM_BOT_NAME'],
        "token": os.environ['TELEGRAM_BOT_TOKEN']
}

imap_config = config['imap']


def get_telegram_uri(message, token, chat_id, reply_message_id=None) -> str:
    reply_message_id_text = ""
    if reply_message_id is not None:
        reply_message_id_text = "&reply_to_message_id=" + reply_message_id
    return f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}" + reply_message_id_text