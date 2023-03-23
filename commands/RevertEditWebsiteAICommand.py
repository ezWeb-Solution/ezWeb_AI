from commands.Command import Command
from UserStates import UserStates
import requests
from UserInfo import UserInfo

class RevertEditWebsiteAICommand(Command):

    def __init__(self, chat_id, bot, user):
        self.chat_id = chat_id
        self.bot = bot
        self.user = user

    def execute(self):
        self.user['state'] = UserStates.EDIT_WEBSITE
        bot_response = "How do you want to edit the website?"
        self.bot.send_message(chat_id=self.chat_id, text=bot_response)
        old_css = self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"]
        old_html = self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"]
        response = requests.post('http://localhost:3000/uploadcss', data=old_css)
        response = requests.post('http://localhost:3000/uploadhtml', data=old_html)
