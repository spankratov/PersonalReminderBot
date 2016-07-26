from flask import Flask, request
from reminder_bot import PersonalReminderBot
import logging

app = Flask(__name__)
app.config.from_pyfile('default_config.py')
app.config.from_envvar('PERSONALREMINDERBOT_SETTINGS', silent=True)

if app.debug is not True:
    # app.logger is called in order to load default flask logger name
    app.logger
    logging.config.dictConfig(app.config['LOG_SETTINGS'])

bot = PersonalReminderBot(app.config)


@app.route('/webhook/' + app.config['BOT_TOKEN'], methods=['POST'])
def webhook_handler():
    logging.info("Got the update:\n%s" % request.data)
    return bot.handle_update(request.get_json())

if __name__ == '__main__':
    app.run()
