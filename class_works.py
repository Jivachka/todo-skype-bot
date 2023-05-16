import logging
import re
from datetime import datetime

from skpy import Skype, SkypeFileMsg, SkypeMessageEvent, SkypeTextMsg

from data import allowed_friends, login_name, password

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SkypeFileManager:
    def __init__(self, username, password):
        self.skype = Skype(username, password)
        self.message_parse = MessageParser(file_manager)
        self.reminder_time = ''
        self.reminder_message = ''

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
                # self.send_message(ch, 'Ok.Файл')
                # logging.info(f'{msg.content}')
                return msg.content
            elif isinstance(msg, SkypeTextMsg) and self.is_allowed_friend(friend_id):
                # self.send_message(ch, 'Хорошо написал')
                # logging.info(f'{msg.content}')
                return msg.content
        return None

    def start_thread(self):
        while True:
            events = self.skype.getEvents()
            for event in events:
                if event.type == "NewMessage":
                    self.handle_message(event)

class MessageParser:
    def __init__(self, skype_manager):
        self.skype_manager = skype_manager
        self.pattern = re.compile(r"(\d{2}\.\d{2}\.\d{2}) (\d{2}:\d{2}) (.*)")

    def parse(self, message):
        match = self.pattern.match(message)
        if match is None:
            self.skype_manager.send_message('Invalid message format. Please use the following format: "dd.mm.yy hh:mm Your message"')
            return None, 'Invalid message format. Please use the following format: "dd.mm.yy hh:mm Your message"'

        date, time, reminder_message = match.groups()
        reminder_time = datetime.strptime(f'{date} {time}', '%d.%m.%y %H:%M')
        # logging.info(f'[{reminder_time}]-[{reminder_message}]!!!!!!')
        return reminder_time, reminder_message

file_manager = SkypeFileManager(login_name, password)
message_parser = MessageParser(file_manager)

