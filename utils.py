import logging
import logging.config
import traceback
import sys
import telegram_api
import atexit


def initialize_logging(config):
    logging.config.dictConfig(config['LOG_SETTINGS'])

    def log_except_hook(*exc_info):
        text = "".join(traceback.format_exception(*exc_info))
        logging.getLogger(config['LOG_PYTHON_EXCEPTIONS_NAME']).error(text)
    sys.excepthook = log_except_hook


def stop_app(config):
    logging.info("Stopping the app")
    telegram_api.reset_webhook(telegram_url=config['TELEGRAM_URL'], certificate=config['CERTIFICATE'])


def start_app(config):
    logging.info("Starting the app")
    telegram_api.set_webhook(config['TELEGRAM_URL'], config['WEBHOOK_URL'], config['CERTIFICATE'])
    atexit.register(stop_app)
