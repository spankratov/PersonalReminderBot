DEBUG = True
TESTING = True
SERVER_NAME = 'example.com'
CERTIFICATE = 'botssl.pem'
BOT_TOKEN = 'token'
TELEGRAM_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'
WEBHOOK_URL = SERVER_NAME + '/webhook/' + BOT_TOKEN
MONGO_DEFAULT_BD = 'botdb'
DEFAULT_REMINDER_DELAY = 1000 * 1000 * 10
DEFAULT_REMINDER_TEXT = 'Hi! Remind you about the %s you sent to me:'
DEFAULT_MESSAGE_TYPES = ['text', 'photo', 'audio', 'document', 'video', 'voice']
ERROR_LOG_PATH = 'path/to/error_log_file.txt'
INFO_LOG_PATH = 'path/to/info_log_file.txt'
PYTHON_EXCEPTIONS_LOG_PATH = 'path/to/python_exceptions_log_file.txt'
LOG_CAPACITY_BYTES = 1024 * 1024 * 10
LOG_BACKUP_COUNT = 20
LOG_FLASK_EXCEPTIONS_NAME = 'flaskapp'  # use the same name that is sent to Flask function during app initialization
LOG_SETTINGS = {
    'version': 1,
    'root': {
        'level': 'NOTSET',
        'handlers': ['info_file', 'error_file'],
    },
    'loggers': {
        LOG_FLASK_EXCEPTIONS_NAME: {
            'level': 'ERROR',
            'handlers': ['exceptions_file'],
            'propagate': False
        }
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
        },
        'exceptions_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'exceptions',
            'filename': PYTHON_EXCEPTIONS_LOG_PATH,
            'mode': 'a',
            'maxBytes': LOG_CAPACITY_BYTES,
            'backupCount': LOG_BACKUP_COUNT,
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'exceptions': {
            'format': '%(asctime)s Exception ocurred:\n%(message)s\n'
        }
    }
}
