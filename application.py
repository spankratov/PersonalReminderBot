import flask
import logging
import logging.config
from celery import Celery
from views.reminders import UpdatePost, RetransmitMessage
from reminder_bot import PersonalReminderBot


class Route(object):

    def __init__(self, url, route_name, resource):
        self.url = url
        self.route_name = route_name
        self.resource = resource

handlers = [
    Route('/webhook/', 'webhook.update', UpdatePost),
    Route('/retransmit/', 'retransmit', RetransmitMessage)
]


class Application(object):

    def __init__(self, routes):
        self.flask_app = flask.Flask(__name__)
        self.routes = routes
        self._configure_app()
        self._set_routes()
        self.bot = PersonalReminderBot(self.flask_app.config)

    def celery(self):
        app = self.flask_app
        celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROCKER_URL'])
        celery.conf.update(app.config)

        TaskBase = celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
        celery.Task = ContextTask

        return celery

    def _set_routes(self):
        for route in self.routes:
            app_view = route.resource.as_view(route.route_name)
            self.flask_app.add_url_rule(route.url + self.flask_app.config['BOT_TOKEN'], view_func=app_view)

    def _configure_app(self):
        self.flask_app.config.from_pyfile('default_config.py')
        self.flask_app.config.from_envvar('PERSONALREMINDERBOT_SETTINGS', silent=True)

        if self.flask_app.debug is not True:
            # app.logger is called in order to load default flask logger name
            self.flask_app.logger
            logging.config.dictConfig(self.flask_app.config['LOG_SETTINGS'])
