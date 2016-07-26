import logging
import atexit
from pymongo import MongoClient
from telegram_api import TelegramApi
from celery import Celery
from celery.contrib.methods import task_method
from datetime import datetime, timedelta

celery = Celery('reminder_bot', broker='amqp://guest@localhost//')


class PersonalReminderBot:
    def __init__(self, config):
        logging.info("Starting the app")
        telegram_api = TelegramApi(config['TELEGRAM_URL'], config['CERTIFICATE'])
        telegram_api.set_webhook(config['WEBHOOK_URL'])
        self.telegram_api = telegram_api

        mongo_client = MongoClient()
        self.mongo_client = mongo_client
        self.db = mongo_client[config['MONGO_DEFAULT_BD']]

        self.reminder_text = config['DEFAULT_REMINDER_TEXT']
        self.message_types = config['DEFAULT_MESSAGE_TYPES']
        self.delay = config['DEFAULT_REMINDER_DELAY']

        def stop_bot():
            logging.info("Stopping the app")
            mongo_client.close()
            logging.info("Mongodb connection closed")
            telegram_api.reset_webhook()

        atexit.register(stop_bot)

    @celery.task(filter=task_method)
    def remind(self, object_id):
        logging.info("Celery task is invoked, ObjectId: " + str(object_id))
        note = self.db.notes.find_one({'_id': object_id})
        chat_id = note['chat_id']
        send_type = note['type']
        if send_type in self.message_types:
            if send_type == 'text':
                self.telegram_api.send_message(chat_id, self.reminder_text % 'message' + '\n' + note['text'])
            else:
                self.telegram_api.send_message(chat_id, self.reminder_text % send_type)
                getattr(self.telegram_api, 'send_' + send_type)(chat_id, note['file_id'])
        self.db.notes.delete_one({'_id': object_id})
        logging.info("Note is removed from database, ObjectId: " + str(object_id))

    def handle_update(self, update):
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            note = {'chat_id': chat_id, 'due': datetime.utcnow() + timedelta(microseconds=self.delay)}
            for send_type in self.message_types:
                if send_type in message:
                    note['type'] = send_type
                    if send_type == 'text':
                        note['text'] = message['text']
                    elif send_type == 'photo':
                        note['file_id'] = message['photo'][0]['file_id']
                    else:
                        note['file_id'] = message[send_type]['file_id']
                    inserted_note = self.db.notes.insert_one(note)
                    logging.info("Inserted new note to database:\n" + str(note))
                    self.remind.apply_async(args=[inserted_note.inserted_id], eta=note['due'])
                    break
        return "Got the message"
