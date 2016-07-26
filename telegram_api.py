import requests
import logging


class TelegramBot:
    def __init__(self, telegram_url, certificate):
        self.telegram_url = telegram_url
        self.certificate = certificate

    def set_webhook(self, webhook_url):
        r = requests.post(self.telegram_url + 'setWebhook', params={'url': webhook_url},
                          files={'certificate': open(self.certificate, 'rb')})
        if r.status_code != 200:
            msg = "Error during setting webhook.\nTelegram response:\nStatus code:" + r.status_code + "\nText:" + r.text
            logging.error(msg)
            raise RuntimeError(msg)
        else:
            logging.info('Webhook is set to %s' % webhook_url)

    def reset_webhook(self):
        r = requests.post(self.telegram_url + 'setWebhook', params={'url': ''},
                          files={'certificate': open(self.certificate, 'rb')})
        if r.status_code != 200:
            msg = "Error during resetting webhook.\nTelegram response:\nStatus code:" + r.status_code + "\nText:" + r.text
            raise RuntimeError(msg)
        else:
            logging.info('Webhook is reset')

    def send_message(self, chat_id, text):
        r = requests.post(self.telegram_url + 'sendMessage', params={'chat_id': chat_id, 'text': text})
        if r.status_code != 200:
            msg = "Error during setting webhook.\nTelegram response:\nStatus code:" + r.status_code + "\nText:" + r.text
            logging.error(msg)
            raise RuntimeError(msg)
        else:
            logging.info("Successfully sent message '%s' to %s chat" % (text, chat_id))
