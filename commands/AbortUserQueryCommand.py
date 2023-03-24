from UserStates import UserStates
from commands.Command import Command
import requests
import json
from commands.StartCommand import StartCommand

class AbortUserQueryCommand(Command):

    def __init__(self, chat_id, bot, user):
        self.chat_id = chat_id
        self.bot = bot
        self.user = user


    def execute(self):
        self.bot['state'] = UserStates.EDIT_WEBSITE_GPT_PROMPTING_ABORT
        api_key = "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"
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system",
                          "content": "You are a helpful AI"},
                         {"role": "user",
                          "content": "Hello"}],
            "abort": True,
            "temperature": 0.3,
            "n": 1
        }
        response = requests.post(url,
                                 headers=headers,
                                 data=json.dumps(data))
        print(response.status_code)
        if response.status_code == 200:
            self.bot.send_message(chat_id=self.chat_id, text="Prompt aborted! Returning to main menu..")
            StartCommand(self.chat_id, self.bot, self.user).execute()
        else:
            self.bot.send_message(chat_id=self.chat_id, text="Something went wrong..")