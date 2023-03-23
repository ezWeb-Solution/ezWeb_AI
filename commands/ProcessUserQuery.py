from telegram import *
from UserStates import UserStates
from commands.Command import Command
from UserInfo import UserInfo
import requests
import json
import openai

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
        self.bot.send_message(chat_id=self.chat_id, text="Done!")
        self.user['state'] = UserStates.EDIT_WEBSITE_COMPLETED
        options = [[InlineKeyboardButton("Keep Changes", callback_data=UserStates.EDIT_WEBSITE_KEEP_CHANGES)],
                   [InlineKeyboardButton("Revert", callback_data=UserStates.EDIT_WEBSITE_REVERT_CHANGES)]]
        self.bot.send_message(chat_id=self.chat_id, text="Would you like to keep or revert changes?", reply_markup=InlineKeyboardMarkup(options))

    def get_html(self):
        resp = requests.get("http://localhost:3000/html")
        self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] = resp.text

    def get_css(self):
        resp = requests.get("http://localhost:3000/style")
        self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"] = resp.text

    def get_chat_gpt_response(self):
        #api_key = "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"
        api_key = "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"
        #openai.api_key = "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"
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        prompt = """
                I am going to give you IN MESSAGE TEXT FORMAT one css file and one html file that work with one another.
                I am also going to give you user inputs that want to change the content or appearance of the website, which you will do by changing the css file and the html file.
                Return IN MESSAGE TEXT FORMAT the changes that should be made to the html and css files.
                ONLY SEND ME THE LINES THAT I NEED TO CHANGE.
                GIVE ME ONLY CODE. DO NOT SAY ANYTHING ELSE. FOLLOW EXACTLY THE BELOW FORMAT.

                Example Response:
                HTML file Line Number Range: 7-8
                [Insert html code here] 
                CSS file Line Number Range: 8-9
                [Insert css code here]
                """

        # prompt = self.message + "\n" + \
        #          prompt + "\n" + self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] \
        #          + "\n" + self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"]
        # user_prompt =  self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] \
        #          + "\n" + self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"] \
        #         + "Here is the html line of code to search:\n" + self.message

        user_prompt =  self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] \
                + "\n\n\nHERE IS THE LINE OF CODE TO SEARCH\n'" + self.message + "'"
        print(user_prompt)
        # data = {
        #     "model": "gpt-3.5-turbo",
        #     "messages": [{"role": "system", "content": "You are a helpful assistant."},
        #                  {"role": "user", "content": prompt}],
        #     "temperature": 0.7,
        #     "n": 1
        # }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system",
                #           "content": """
                # I am going to give you IN MESSAGE TEXT FORMAT one css file and one html file that work with one another.
                # I am also going to give you user inputs that want to change the content or appearance of the website, which you will do by changing the css file and the html file.
                # Return IN MESSAGE TEXT FORMAT the changes that should be made to the html and css files.
                # ONLY SEND ME THE LINES THAT I NEED TO CHANGE.
                # GIVE ME ONLY CODE. DO NOT SAY ANYTHING ELSE. FOLLOW EXACTLY THE BELOW FORMAT.
                #
                # Example Response:
                # [Exact line(s) of html code to replace]
                # [Insert html code here]
                # [Exact line(s) of css code to replace]
                # [Insert css code here]
                # """
                "content": "I am going to give you a html file and a line of code. Give me the class where this line of code belongs to."},
                         {"role": "user", "content": user_prompt}],
            "temperature": 0.7,
            "n": 1
        }
        response = requests.post(url,
                                 headers=headers,
                                 data=json.dumps(data))
        print(response.status_code)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            resp = response_data['choices'][0]['message']['content']
            #resp2 = response_data['choices'][1]['message']['content']
            print("Printing response: " + resp)
            html = self.process_html(resp)
            css = self.process_css(resp)
            print("HTML:\n\n" + html)
            print("CSS:\n\n" + css)

            #response = requests.post('http://localhost:3000/uploadcss', data=css)
            #response = requests.post('http://localhost:3000/uploadhtml', data=html)
        else:
            self.bot.send_message(chat_id=self.chat_id, text="Something went wrong..")

    def process_html(self, html):
        info = html.split("<!--HTML-->")
        info = "<!--HTML-->" + info[1] + "<!--HTML-->"
        return info

    def process_css(self, css):
        info = css.split("/*$CSS*/")
        info = "/*$CSS*/" + info[1] + "/*$CSS*/"
        return info[1]

