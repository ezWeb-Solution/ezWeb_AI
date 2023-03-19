from telegram.ext import *
import logging
from commands.StartCommand import StartCommand
from ezweb_parser.MessageParser import MessageParser
from ezweb_parser.InlineQueryParser import InlineQueryParser

bot_token = "5880446535:AAGx1DuORcGOaY8YpXTYBnmvUjScmerhuwg"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
current_user = {}

def start(update, context):
    start_command = StartCommand(update.effective_chat.id, context.bot, get_user(update.effective_chat.id))
    start_command.execute()

def get_user(chat_id):
    if chat_id in current_user:
        return current_user[chat_id]
    current_user[chat_id] = {}
    return current_user[chat_id]

def message_handler(update, context):
    chat_id = update.effective_chat.id
    bot = context.bot
    message = update.message.text
    MessageParser(chat_id, bot, get_user(chat_id))\
        .parse(message)\
        .execute()

def inline_query(update, context):
    chat_id = update.effective_chat.id
    bot = context.bot
    query = update.callback_query.data
    update.callback_query.answer()
    clear_query(update, context)
    InlineQueryParser(chat_id, bot, get_user(chat_id))\
        .parse(query)\
        .execute()

def clear_query(update, context):
    context.bot.edit_message_reply_markup(
        message_id=update.callback_query.message.message_id,
        chat_id=update.callback_query.message.chat.id,
        reply_markup=None)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

query_handler = CallbackQueryHandler(inline_query)
dispatcher.add_handler(query_handler)

catchall_handler = MessageHandler(Filters.text, message_handler)
dispatcher.add_handler(catchall_handler)

updater.start_polling()
updater.idle()