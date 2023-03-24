from telegram import *
from UserStates import UserStates
from commands.Command import Command
from UserInfo import UserInfo
import requests
import json
from Delimiters import Delimiters
from AIPrompts import AIPrompts

class ProcessUserQuery(Command):

    def __init__(self, chat_id, bot, user, message):
        self.chat_id = chat_id
        self.bot = bot
        self.user = user
        self.message = message

    def execute(self):
        self.user[UserInfo.CURRENT_WEBSITE_CSS] = {}
        self.user[UserInfo.CURRENT_WEBSITE_HTML] = {}
        self.user[UserInfo.PREV_WEBSITE_HTML] = {}
        self.user[UserInfo.PREV_WEBSITE_CSS] = {}
        self.get_html()
        #self.get_css()
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
        self.user[UserInfo.PREV_WEBSITE_HTML]["file"] = resp.text

    def get_css(self):
        resp = requests.get("http://localhost:3000/style")
        self.user[UserInfo.CURRENT_WEBSITE_CSS]["file"] = resp.text

    def get_chat_gpt_response(self):
        #api_key = "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"
        api_key = "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"
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        user_prompt = self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] \
                + "\n\n\nABOVE IS THE HTML FILE AND HERE ARE THE REQUESTED CHANGES\n'" + self.message + "'"
        print(user_prompt)

        system_context = AIPrompts.EDIT_SYSTEM_CONTEXT
        system_context += self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"]
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system",
                          "content": system_context},
                         {"role": "user",
                          "content": user_prompt}],
            "temperature": 0.3,
            "n": 1
        }
        response = requests.post(url,
                                 headers=headers,
                                 data=json.dumps(data))
        print(response.status_code)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            resp = response_data['choices'][0]['message']['content']
            print("Printing response: " + resp)
            self.process_html(resp)
            new_html = self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"]
            #css = self.process_css(resp)
            print("New HTML:\n\n" + new_html)
            # print("CSS:\n\n" + css)

            #response = requests.post('http://localhost:3000/uploadcss', data=css)
            response = requests.post('http://localhost:3000/uploadhtml', data=new_html)
        else:
            self.bot.send_message(chat_id=self.chat_id, text="Something went wrong..")

    def process_html(self, resp):
        info = resp.split("\n")
        counter = 0
        while(True):
            if counter >= len(info):
                break
            curr = info[counter]
            print(curr)
            if curr.startswith(Delimiters.ADD_ACTION):
                start = counter + 1
                end = counter + 1
                while (end < len(info)):
                    if info[end].startswith(Delimiters.ADD_ACTION) or info[end].startswith(Delimiters.DELETE_ACTION):
                        break
                    else:
                        end += 1
                if (end == start + 1):
                    counter += 1
                    continue
                full_query = ""
                for i in range(start, end):
                    full_query += (info[i] + '\n')
                self.process_add_query(full_query)
                counter = end
            elif curr.startswith(Delimiters.DELETE_ACTION):
                start = counter + 1
                end = counter + 1
                while (end <= len(info)):
                    if info[end].startswith(Delimiters.ADD_ACTION) or info[end].startswith(Delimiters.DELETE_ACTION):
                        break
                    else:
                        end += 1
                if (end == start + 1):
                    counter += 1
                    continue
                full_query = ""
                for i in range(start, end):
                    full_query += (info[i] + '\n')
                self.process_delete_query(full_query)
                counter = end
            else:
                counter += 1
        print("Done!")

    def process_add_query(self, full_query):
        to_process = full_query.split("\n")
        line_target = -1
        new_content = ""
        for i in range(len(to_process)):
            if to_process[i] == Delimiters.ADD_ACTION:
                continue
            elif to_process[i].startswith(Delimiters.ADD_ACTION_ID):
                line_target = int(to_process[i].split(Delimiters.ADD_ACTION_ID)[1].strip())
            elif to_process[i].startswith(Delimiters.ADD_ACTION_CONTENT):
                new_content = to_process[i].split(Delimiters.ADD_ACTION_CONTENT)[1]
        self.add_html(line_target, new_content)

    def add_html(self, id, new_content):
        html_file = self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"]
        output = ""
        to_check = 'id="' + str(id) + '"'
        html_lines = html_file.split("\n")
        for line in html_lines:
            if to_check in line:
                output += (line + "\n")
                output += (new_content + "\n")
            else:
                output += (line + "\n")
        self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] = output

    def process_delete_query(self, full_query):
        to_process = full_query.split("\n")
        line_target = -1
        for i in range(len(to_process)):
            if to_process[i] == Delimiters.DELETE_ACTION:
                continue
            elif to_process[i].startswith(Delimiters.DELETE_ACTION_ID):
                line_target = int(to_process[i].split(Delimiters.DELETE_ACTION_ID)[1].strip())
        self.delete_html(line_target)

    def delete_html(self, id):
        html_file = self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"]
        output = ""
        to_check = 'id="' + str(id) + '"'
        html_lines = html_file.split("\n")
        for line in html_lines:
            if to_check in line:
                continue
            else:
                output += line + "\n"
        self.user[UserInfo.CURRENT_WEBSITE_HTML]["file"] = output


    def process_css(self, css):
        info = css.split("/*$CSS*/")
        info = "/*$CSS*/" + info[1] + "/*$CSS*/"
        return info[1]

