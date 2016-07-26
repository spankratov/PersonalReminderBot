import logging
import logging.config
from telegram_api import TelegramBot
import atexit


def stop_app(bot):
    logging.info("Stopping the app")
    bot.reset_webhook()


def start_app(config):
    logging.info("Starting the app")
    bot = TelegramBot(config['TELEGRAM_URL'], config['CERTIFICATE'])
    bot.set_webhook(config['WEBHOOK_URL'])
    atexit.register(stop_app, bot=bot)
    return bot
