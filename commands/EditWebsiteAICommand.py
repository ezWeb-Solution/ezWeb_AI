from commands.Command import Command
from telegram import *;
from UserStates import UserStates
import requests

class EditWebsiteAICommand(Command):

    def __init__(self, chat_id, bot, user):
        self.chat_id = chat_id
        self.bot = bot
        self.user = user

    def execute(self):
        self.user['state'] = UserStates.EDIT_WEBSITE
        bot_response = "How do you want to edit the website?"
        self.bot.send_message(chat_id=self.chat_id, text=bot_response)
