from flask import Flask, request

import atexit
import telegram_api
import logging

app = Flask(__name__)
app.config.from_pyfile('default_config.py')
app.config.from_envvar('PERSONALREMINDERBOT_SETTINGS', silent=True)

if app.debug is not True:
    import logging.config
    logging.config.dictConfig(app.config['LOG_SETTINGS'])

telegram_api.set_webhook(app.config['TELEGRAM_URL'], app.config['WEBHOOK_URL'], app.config['CERTIFICATE'])
atexit.register(telegram_api.reset_webhook, telegram_url=app.config['TELEGRAM_URL'],
                certificate=app.config['CERTIFICATE'])


@app.route('/webhook/' + app.config['BOT_TOKEN'], methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        logging.info("Got the message.\nHeaders:\n%s\nData:\n%s\n" % (request.headers, request.data))
    return "Got the message"

if __name__ == '__main__':
    app.run()
