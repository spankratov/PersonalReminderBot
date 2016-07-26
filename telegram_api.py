import requests
import logging


class TelegramApi:
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

    def send(self, method, params, description):
        r = requests.post(self.telegram_url + method, params=params)
        if r.status_code != 200:
            msg = "Error during " + description + "\nTelegram response:\nStatus code:" + r.status_code + "\nText:" + r.text
            logging.error(msg)
            raise RuntimeError(msg)
        else:
            logging.info("Successful " + description + "\nParameters:\n" + str(params))

    def send_message(self, chat_id, text):
        self.send('sendMessage', {'chat_id': chat_id, 'text': text}, 'sending message')

    def send_text(self, chat_id, text):
        self.send_message(chat_id, text)

    def send_photo(self, chat_id, photo_id):
        self.send('sendPhoto', {'chat_id': chat_id, 'photo': photo_id}, 'sending photo')

    def send_audio(self, chat_id, audio_id):
        self.send('sendAudio', {'chat_id': chat_id, 'audio': audio_id}, 'sending audio')

    def send_document(self, chat_id, document_id):
        self.send('sendDocument', {'chat_id': chat_id, 'document': document_id}, 'sending document')

    def send_video(self, chat_id, video_id):
        self.send('sendVideo', {'chat_id': chat_id, 'video': video_id}, 'sending video')

    def send_voice(self, chat_id, voice_id):
        self.send('sendVoice', {'chat_id': chat_id, 'voice': voice_id}, 'sending voice')
