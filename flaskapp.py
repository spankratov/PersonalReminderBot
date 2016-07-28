from flask import Flask, request, current_app
from reminder_bot import PersonalReminderBot
from utils import make_celery
import logging
import logging.config

app = Flask(__name__)
app.config.from_pyfile('default_config.py')
app.config.from_envvar('PERSONALREMINDERBOT_SETTINGS', silent=True)

if app.debug is not True:
    # app.logger is called in order to load default flask logger name
    app.logger
    logging.config.dictConfig(app.config['LOG_SETTINGS'])


celery = make_celery(app)
app.bot = PersonalReminderBot(app.config)


@app.route('/webhook/' + app.config['BOT_TOKEN'], methods=['POST'])
def webhook_handler():
    logging.info("Got the update:\n%s" % request.data)
    return current_app.bot.handle_update(request.get_json())

if __name__ == '__main__':
    app.run()
