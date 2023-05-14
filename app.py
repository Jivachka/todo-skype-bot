import datetime
import re
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import skype  # Модуль для работы со Skype API

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class Database:
    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'  # Конфигурация базы данных
        self.db = SQLAlchemy(app)

    def create_tables(self):
        self.db.create_all()

database = Database(app)

class Reminder(database.db.Model):  # Определение модели данных
    id = database.db.Column(database.db.Integer, primary_key=True)
    time = database.db.Column(database.db.DateTime, nullable=False)
    message = database.db.Column(database.db.String(500), nullable=False)


class MessageParser:
    def __init__(self):
        self.pattern = re.compile(r"(\d{2}\.\d{2}\.\d{2}) (\d{2}:\d{2}) (.*)")

    def parse(self, message):
        match = self.pattern.match(message)
        if match is None:
            raise ValueError("Invalid message format")

        date, time, reminder_message = match.groups()
        reminder_time = datetime.datetime.strptime(f'{date} {time}', '%d.%m.%y %H:%M')

        return reminder_time, reminder_message


class SkypeBot:
    def __init__(self, token):
        # self.client = skype.Skype(token)
        pass

    def send_message(self, user_id, message):
        # Отправка сообщения через Skype API
        pass


class ReminderManager:
    def __init__(self, db):
        self.db = db

    def add_reminder(self, reminder_time, reminder_message):
        reminder = Reminder(time=reminder_time, message=reminder_message)
        self.db.session.add(reminder)
        self.db.session.commit()

    def check_reminders(self):
        current_time = datetime.datetime.now()
        due_reminders = Reminder.query.filter(Reminder.time <= current_time).all()
        for reminder in due_reminders:
            self.db.session.delete(reminder)
        self.db.session.commit()
        return due_reminders


class App:
    def __init__(self, token, db):
        self.message_parser = MessageParser()
        self.reminder_manager = ReminderManager(db)
        self.bot = SkypeBot(token)

    def handle_message(self, message):
        try:
            reminder_time, reminder_message = self.message_parser.parse(message)
            self.reminder_manager.add_reminder(reminder_time, reminder_message)
        except ValueError as e:
            logging.error(f"Error parsing message: {e}")

    def run(self):
        # Мониторинг входящих сообщений и проверка напоминаний
        pass


try:
    database = Database(app)
    database.create_tables()
    logging.info("Connected to the database.")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")

my_app = App("your_skype_token", database.db)
my_app.run()
