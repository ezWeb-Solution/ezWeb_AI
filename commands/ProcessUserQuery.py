from telegram import *
from UserStates import UserStates
from commands.Command import Command
from UserInfo import UserInfo
import requests
import json

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
        self.bot.send_message(chat_id=self.chat_id, text="Generating...")
        self.get_chat_gpt_response()
        print("HTML: \n" + self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"])
        print("CSS: \n" + self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"])
        options = [[InlineKeyboardButton("Test out AI processes!", callback_data=UserStates.EDIT_WEBSITE)]]
        bot_response = "How can I help you today?"
        self.bot.send_message(chat_id=self.chat_id, text="Done!")

    def get_html(self):
        resp = requests.get("http://localhost:3000/html")
        self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] = resp.text

    def get_css(self):
        resp = requests.get("http://localhost:3000/html")
        self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"] = resp.text

    def get_chat_gpt_response(self):
        api_key = "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"
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        prompt = "I am going to give you one css file and one html file that work with one another. I am also (may be later) going to give you user inputs that want to change the content or appearance of the website, which you will do by changing the css file and the html file. Return the new html and css files directly to me. Do not write anything else in the response."
        prompt = prompt + "\n" + self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] +\
                         "\n" + self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"]
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system", "content": "You are a helpful assistant."},
                         {"role": "user", "content": prompt}],
            "temperature": 0.7,
            "n": 1
        }
        #print(prompt)
        response = requests.post(url,
                                 headers=headers,
                                 data=json.dumps(data))
        print(response.status_code)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            print(response_data)
            resp = response_data['choices'][0]['message']['content']
            #print(resp)
            return resp
        else:
            return None

