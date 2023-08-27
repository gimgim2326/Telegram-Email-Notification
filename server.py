from dotenv import load_dotenv
load_dotenv()

from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, CommandHandler
from apscheduler.schedulers.background import BlockingScheduler
from service.mail import read_email
from service.telegram import handle_message, updater, dispatcher, confirmationHandler, help_command, chat_id_command, status_command, start_command, handle_new_chat_group, list_commands, reset_command
from helper.config import mail_config


# Log Error Method
def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Startup Method
def main():
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    dispatcher.add_handler(CommandHandler("chatid", chat_id_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("commands", list_commands))
    dispatcher.add_handler(CommandHandler("reset", reset_command))
    dispatcher.add_handler(MessageHandler(Filters.status_update.chat_created, handle_new_chat_group))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(confirmationHandler))
    

    #Log errors
    dispatcher.add_error_handler(error)
    updater.start_polling()

    #To Run as a separate python program, to serve as cron job
    email_reader = BlockingScheduler()
    email_reader.add_job(read_email, "interval", seconds = mail_config["delay"] )
    email_reader.start()
    updater.idle()


# Run main
if __name__ == "__main__":
    main()