import Parser
from UserStates import UserStates
from commands.ProcessUserQuery import ProcessUserQuery

class MessageParser(Parser):

    def __init__(self, chat_id, bot, user):
        self.chat_id = chat_id
        self.bot = bot
        self.user = user

    def parse(self, message):
        if self.user.get('state') is None:
            self.bot.send_message(chat_id=self.chat_id, text="Sorry, I do not understand.")
        elif self.user['state'] == UserStates.EDIT_WEBSITE:
            return ProcessUserQuery(self.chat_id, self.bot, self.user, message)
