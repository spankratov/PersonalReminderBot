DEBUG = True
TESTING = True
SERVER_NAME = 'example.com'
CERTIFICATE = 'botssl.pem'
BOT_TOKEN = 'token'
TELEGRAM_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'
WEBHOOK_URL = SERVER_NAME + '/webhook/' + BOT_TOKEN
LOG_PATH = 'path/to/log_file.txt'
