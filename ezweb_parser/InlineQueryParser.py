from ezweb_parser.Parser import Parser
from UserStates import UserStates
from commands.EditWebsiteAICommand import EditWebsiteAICommand
from commands.StartCommand import StartCommand
from commands.RevertEditWebsiteAICommand import RevertEditWebsiteAICommand

class InlineQueryParser(Parser):

    def __init__(self, chat_id, bot, user):
        self.chat_id = chat_id
        self.bot = bot
        self.user = user

    def parse(self, query):
        if query == UserStates.EDIT_WEBSITE:
            return EditWebsiteAICommand(self.chat_id, self.bot, self.user)
        elif query == UserStates.EDIT_WEBSITE_REVERT_CHANGES:
            return RevertEditWebsiteAICommand(self.chat_id, self.bot, self.user)
        elif query == UserStates.EDIT_WEBSITE_KEEP_CHANGES:
            return StartCommand(self.chat_id, self.bot, self.user)
        elif query == UserStates.EDIT_WEBSITE_GPT_PROMPTING_ABORT:
            if self.user['state'] == UserStates.EDIT_WEBSITE_GPT_PROMPTING:
                return AbortUserQueryCommand(self.chat_id, self.bot, self.user)
            else:
                self.bot.send_message(chat_id=self.chat_id, text="Nothing to be aborted. Press /start if you would like me to do something else")
