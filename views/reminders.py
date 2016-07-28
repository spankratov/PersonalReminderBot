import logging
from flask import request
from flask.views import MethodView
from flaskapp import app


class UpdatePost(MethodView):

    def post(self):
        logging.info("Got the update:\n%s" % request.data)
        return app.bot.handle_update(request.get_json())
