import logging
from flask import current_app, request
from flask.views import MethodView


class UpdatePost(MethodView):

    def post(self):
        logging.info("Got the update:\n%s" % request.data)
        return current_app.bot.handle_update(request.get_json())
