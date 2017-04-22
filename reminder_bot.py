import logging
import atexit
from dateutil.relativedelta import relativedelta
from telegram_api import TelegramApi
from datetime import datetime


class PersonalReminderBot:
    def __init__(self, config):
        self.telegram_api = TelegramApi(config['TELEGRAM_URL'], config['CERTIFICATE'])
        self.webhook_url = config['WEBHOOK_URL']
        self.reminder_text = config['DEFAULT_REMINDER_TEXT']
        self.message_types = config['DEFAULT_MESSAGE_TYPES']
        self.delay = config['DEFAULT_REMINDER_DELAY']

    def set_webhook(self):
        logging.info("Starting the app")
        telegram_api = self.telegram_api
        telegram_api.set_webhook(self.webhook_url)

        def stop_bot():
            logging.info("Stopping the app")
            telegram_api.reset_webhook()

        atexit.register(stop_bot)

    def handle_update(self, update):
        if 'message' in update:
            import tasks
            message = update['message']
            chat_id = message['chat']['id']
            if 'text' in message:
                predicted_due = tasks.detect_datetime.apply_async(args=[message['text'], self.delay], queue='nlp').wait()
                if not isinstance(predicted_due, datetime):
                    predicted_due = datetime.strptime(predicted_due, "%Y-%m-%dT%H:%M:%S.%f")
                if predicted_due < datetime.utcnow():
                    due = datetime.utcnow() + relativedelta(microseconds=self.delay)
                else:
                    due = predicted_due
            else:
                due = datetime.utcnow() + relativedelta(microseconds=self.delay)
            for send_type in self.message_types:
                if send_type in message:
                    if send_type == 'text':
                        content = message['text']
                    elif send_type == 'photo':
                        content = message['photo'][0]['file_id']
                    else:
                        content = message[send_type]['file_id']
                    tasks.remind.apply_async(args=[chat_id, send_type, content], eta=due, queue='reminders')
                    self.telegram_api.send_message(chat_id, 'Ok! You will be reminded at ' + (due + relativedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
                    break
        return "Got the message"

    def handle_retransmission(self, body):
        if 'send_type' not in body or 'chat_id' not in body or 'content' not in body:
            return "Wrong format"
        if body['send_type'] in self.message_types:
            if body['send_type'] == 'text':
                self.telegram_api.send_message(body['chat_id'], self.reminder_text % 'message' + '\n' + body['content'])
            else:
                self.telegram_api.send_message(body['chat_id'], self.reminder_text % body['send_type'])
                getattr(self.telegram_api, 'send_' + body['send_type'])(body['chat_id'], body['content'])
        return "Message is retransmitted"
