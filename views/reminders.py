import logging
from flask import request
from flask.views import MethodView
import flaskapp


class UpdatePost(MethodView):

    def post(self):
        logging.info("Got the update:\n%s" % request.data)
        return flaskapp.app.bot.handle_update(request.get_json())


class RetransmitMessage(MethodView):

    def post(self):
        logging.info("Got message retransmission request:\n%s" % request.data)
        return flaskapp.app.bot.handle_retransmission(request.get_json())
