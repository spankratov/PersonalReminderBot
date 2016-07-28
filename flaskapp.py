from application import handlers, Application

app = Application(handlers)
flask_app = app.flask_app
celery = app.celery()

import tasks