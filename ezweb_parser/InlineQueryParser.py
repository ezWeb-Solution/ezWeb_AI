from ezweb_parser.Parser import Parser
from UserStates import UserStates
from commands.EditWebsiteAICommand import EditWebsiteAICommand

class InlineQueryParser(Parser):

    def __init__(self, chat_id, bot, user):
        self.chat_id = chat_id
        self.bot = bot
        self.user = user

    def parse(self, query):
        if query == UserStates.EDIT_WEBSITE:
            return EditWebsiteAICommand(self.chat_id, self.bot, self.user)
