from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode, Message
from telegram.ext import Updater, ContextTypes
from service.mail import send_email
from helper.config import telegram_config, mail_config
import redis


# Telegram update
updater = Updater(telegram_config['token'], use_context=True)
dispatcher = updater.dispatcher
r = redis.Redis(host='redis', port=6379, db=0)
available_commands="""Available Commands:

- /start - Set this chat group's id where the emails will be forwarded
- /commands - List the available commands
- /help - Displays the instructions on how to use the bot
- /chatid - Displays the chat id
- /status - Check if the bot is ready to use
"""

def handle_response(recipient, text) -> str:
    send_email( recipient, text)
    return "Email sent to " + recipient

def handle_new_chat_group(update: Update, context):
    welcome_message = """*Welcome to IS238 Group 2's Chatroom!*

Enter the /start command to begin forwarding new email from {mail} to this chat group.

Remember to set the *Chat History* to *Visible* or else the bot will not function properly.

Enter the /commands command to list the available commands.
""".format(mail=mail_config["mail"])
    
    update.effective_chat.send_message(welcome_message, parse_mode=ParseMode.MARKDOWN)

def handle_message(update: Update, context):
    # Get basic info of the incoming message
    msg = update.message
    message_type = msg.chat.type
    recipient = ""
    response = ""
    replied_msg = ""
    text = str(msg.text)
    bot_name = telegram_config["bot_name"]
    
    print("Reply Msg is ==> " + text )
    sender = msg.from_user.username if msg.from_user.username else msg.from_user.id
    print("### sender " + sender)

    if msg.reply_to_message:
        replied_msg = str(msg.reply_to_message.text)
        print("Parent Msg is ==> " + replied_msg)
        recipient = parse_reply(replied_msg)
        print("Email is ==> " + recipient)

        if recipient != '':
            keyboard = [
                [
                    InlineKeyboardButton("Yes", callback_data=recipient),
                    InlineKeyboardButton("No", callback_data="No")
                ]
            ]

            key = recipient + "." + str(update.effective_chat.id)
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            message_id = r.get(key)
            
            if message_id is not None:
                update.message.reply_to_message.message_id = str(message_id, 'utf-8')
                
            update.message.reply_text(f"Would you like to send this reply to {recipient}?", reply_markup=reply_markup)


def parse_reply(msg):
    if msg:
        #get first line, and retrieve email enclosed in < >
        first_line = msg.partition('\n')[0]
        try:
            recipient = first_line.split('<', 1)[1].split('>')[0]
            return recipient
        except (IndexError, ValueError):
            return ''

    return ''

def confirmationHandler(update, context) -> None:
    query = update.callback_query

    query.answer()
    if query.data == 'No':
        query.edit_message_text(text='User cancelled sending')
    else:
        query.edit_message_text(text="Sending...")
        message = "Telegram User <" + query.from_user.username + "> replied: \n" + query.message.reply_to_message.text
        response = handle_response(query.data, message)
        query.edit_message_text(text=response)
        
def start_command(update: Update, context) -> None:
    r.set("chat_id", update.effective_chat.id)
    update.effective_chat.send_message("Chat group id is set. New mails from {mail} will be forwarded to this chat group.".format(mail=mail_config['mail']))

def help_command(update: Update, context) -> None:
    mail = mail_config['mail']
    help = """*Please read the instructions carefully on how to use this bot*

1. Make sure you set the chat group id as the receiver by entering the /start command
2. Send an email to {mail} and it will be forwarded to this chat group
3. Tap 'Reply' on the message and enter your reply to send it back to the email sender
4. A confirmation prompt will show, tap on 'Yes' to send or 'No' to cancel
5. Replying to the same email sender will be grouped on the same thread (You don't have to scroll to the sender's first message)
6. New emails from the same sender will also be grouped together
7. Tap on 'View Replies' on the sender's very first email message to view all the messages in the thread
8. Have fun!""".format(mail=mail)
    update.effective_chat.send_message(text=help, parse_mode=ParseMode.MARKDOWN)

def chat_id_command(update: Update, context) -> None:
    update.effective_chat.send_message(update.effective_chat.id)
    
def status_command(update: Update, context) -> None:
    if r.get("chat_id") is None:
        update.effective_chat.send_message("Bot is not ready. Use the /start command to set this chat group's id as the email receiver")
        return
    
    error_message = "Bot is not ready. Make sure you follow the *Setup Guide* in https://github.com/juinfanteUP/is238-g2-project#setup-guide-from-a-fresh-ubuntu-installation"
    for conf in telegram_config:
        if telegram_config[conf] == "":
            update.effective_chat.send_message(error_message, parse_mode=ParseMode.MARKDOWN)
            return
        
    for conf in mail_config:
        if mail_config[conf] == "":
            update.effective_chat.send_message(error_message, parse_mode=ParseMode.MARKDOWN)
            return
    
    update.effective_chat.send_message("Bot is ready")

def list_commands(update: Update, context) -> None:
    update.effective_chat.send_message(text=available_commands, parse_mode=ParseMode.MARKDOWN)
    
def reset_command(update: Update, context) -> None:
    for key in r.scan_iter("*" + update.effective_chat.id):
        r.delete(key)
        
    update.effective_chat.send_message("Cache cleared successfully")