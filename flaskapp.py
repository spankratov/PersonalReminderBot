from application import handlers, Application

app = Application(handlers)
celery = app.celery()

import tasks