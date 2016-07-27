import logging
import atexit
from telegram_api import TelegramApi
from pymongo import MongoClient
from datetime import datetime, timedelta


class PersonalReminderBot:
    def __init__(self, config):
        logging.info("Starting the app")
        telegram_api = TelegramApi(config['TELEGRAM_URL'], config['CERTIFICATE'])
        telegram_api.set_webhook(config['WEBHOOK_URL'])
        self.telegram_api = telegram_api

        self.mongodb_name = config['MONGO_DEFAULT_BD']

        self.reminder_text = config['DEFAULT_REMINDER_TEXT']
        self.message_types = config['DEFAULT_MESSAGE_TYPES']
        self.delay = config['DEFAULT_REMINDER_DELAY']

        def stop_bot():
            logging.info("Stopping the app")
            telegram_api.reset_webhook()

        atexit.register(stop_bot)

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
                    mongo_client = MongoClient()
                    db = mongo_client[self.mongodb_name]
                    inserted_note = db.notes.insert_one(note)
                    logging.info("Inserted new note to database:\n" + str(note))
                    mongo_client.close()
                    self.remind.apply_async(args=[str(inserted_note.inserted_id)], eta=note['due'])
                    break
        return "Got the message"
