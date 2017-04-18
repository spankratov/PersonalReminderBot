import logging
from flaskapp import app, celery


@celery.task
def remind(chat_id, send_type, content):
    logging.info("Celery task is invoked, chat_id: {}, send_type: {}, content: {}".format(chat_id, send_type, content))
    if send_type in app.bot.message_types:
        if send_type == 'text':
            app.bot.telegram_api.send_message(chat_id, app.bot.reminder_text % 'message' + '\n' + content)
        else:
            app.bot.telegram_api.send_message(chat_id, app.bot.reminder_text % send_type)
            getattr(app.bot.telegram_api, 'send_' + send_type)(chat_id, content)
