from telegram import *
from UserStates import UserStates
from commands.Command import Command
from UserInfo import UserInfo
import requests

class ProcessUserQuery(Command):

    def __init__(self, chat_id, bot, user, message):
        self.chat_id = chat_id
        self.bot = bot
        self.user = user
        self.message = message

    def execute(self):
        self.user[UserInfo.CURRENT_WEBSITE_CSS] = {}
        self.user[UserInfo.CURRENT_WEBSITE_HTML] = {}
        self.get_html()
        self.get_css()
        print("CSS: \n" + self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"])
        print("CSS: \n" + self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"])
        options = [[InlineKeyboardButton("Test out AI processes!", callback_data=UserStates.EDIT_WEBSITE)]]
        bot_response = "How can I help you today?"
        self.bot.send_message(chat_id=self.chat_id, text=bot_response,
                              reply_markup=InlineKeyboardMarkup(options))

    def get_html(self):
        resp = requests.get("http://localhost:3000/html")
        self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] = resp.text

    def get_css(self):
        resp = requests.get("http://localhost:3000/html")
        self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"] = resp.text

