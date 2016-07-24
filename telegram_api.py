import requests
import logging


def set_webhook(telegram_url, webhook_url, certificate):
    r = requests.post(telegram_url + 'setWebhook', params={'url': webhook_url},
                      files={'certificate': open(certificate, 'rb')})
    if r.status_code != 200:
        msg = "Error during setting webhook.\nTelegram response:\nStatus code:" + r.status_code + "\nText:" + r.text
        logging.error(msg)
        raise RuntimeError(msg)
    else:
        logging.info('Webhook is set to %s' % webhook_url)


def reset_webhook(telegram_url, certificate):
    r = requests.post(telegram_url + 'setWebhook', params={'url': ''},
                      files={'certificate': open(certificate, 'rb')})
    if r.status_code != 200:
        msg = "Error during resetting webhook.\nTelegram response:\nStatus code:" + r.status_code + "\nText:" + r.text
        raise RuntimeError(msg)
    else:
        logging.info('Webhook is reset')
