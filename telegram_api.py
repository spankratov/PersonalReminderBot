import requests


def set_webhook(telegram_url, webhook_url, certificate):
    r = requests.post(telegram_url + 'setWebhook', params={'url': webhook_url},
                      files={'certificate': open(certificate, 'rb')})
    if r.status_code != 200:
        raise RuntimeError(
            "Error during setting webhook.\nTelegram response:\nStatus code:" + r.status_code + "\nText:" + r.text)


def reset_webhook(telegram_url, certificate):
    r = requests.post(telegram_url + 'setWebhook', params={'url': ''},
                      files={'certificate': open(certificate, 'rb')})
    if r.status_code != 200:
        raise RuntimeError(
            "Error during resetting webhook.\nTelegram response:\nStatus code:" + r.status_code + "\nText:" + r.text)
