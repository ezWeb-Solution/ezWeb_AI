from telegram import *
from UserStates import UserStates
from commands.Command import Command

class StartCommand(Command):

    def __init__(self, chat_id, bot, user):
        self.chat_id = chat_id
        self.bot = bot
        self.user = user

    def execute(self):
        self.user['state'] = UserStates.START
        options = [[InlineKeyboardButton("Test out AI processes!", callback_data=UserStates.EDIT_WEBSITE)]]
        bot_response = "How can I help you today?"
        self.bot.send_message(chat_id=self.chat_id, text=bot_response,
                              reply_markup=InlineKeyboardMarkup(options))
