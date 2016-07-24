DEBUG = True
TESTING = True
SERVER_NAME = 'example.com'
CERTIFICATE = 'botssl.pem'
BOT_TOKEN = 'token'
TELEGRAM_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'
WEBHOOK_URL = SERVER_NAME + '/webhook/' + BOT_TOKEN
ERROR_LOG_PATH = 'path/to/error_log_file.txt'
INFO_LOG_PATH = 'path/to/info_log_file.txt'
LOG_CAPACITY_BYTES = 1024 * 1024 * 10
LOG_BACKUP_COUNT = 20
LOG_SETTINGS = {
    'version': 1,
    'root': {
        'level': 'NOTSET',
        'handlers': ['info_file', 'error_file'],
    },
    'handlers': {
        'info_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': INFO_LOG_PATH,
            'mode': 'a',
            'maxBytes': LOG_CAPACITY_BYTES,
            'backupCount': LOG_BACKUP_COUNT,
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'default',
            'filename': ERROR_LOG_PATH,
            'mode': 'a',
            'maxBytes': LOG_CAPACITY_BYTES,
            'backupCount': LOG_BACKUP_COUNT,
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    }
}
