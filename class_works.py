import logging
from skpy import Skype, SkypeFileMsg, SkypeMessageEvent, SkypeTextMsg

from data import allowed_friends

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SkypeFileManager:
    def __init__(self, username, password):
        self.skype = Skype(username, password)

    def is_allowed_friend(self, friend_id):
        return friend_id in allowed_friends

    def send_message(self, chat, message):
        chat.sendMsg(f"\n{message}")

    def handle_message(self, event):
        if isinstance(event, SkypeMessageEvent):
            msg = event.msg
            friend_id = msg.user.id
            ch = msg.chat

            if isinstance(msg, SkypeFileMsg) and self.is_allowed_friend(friend_id):
                self.send_message(ch, 'Ok.Файл')
                logging.info(f'{msg.content}')
                return msg.content
            elif isinstance(msg, SkypeTextMsg) and self.is_allowed_friend(friend_id):
                self.send_message(ch, 'Хорошо написал')
                logging.info(f'{msg.content}')
                return msg.content

        return None

    def start_thread(self):
        while True:
            events = self.skype.getEvents()
            for event in events:
                if event.type == "NewMessage":
                    file_content = self.handle_message(event)
