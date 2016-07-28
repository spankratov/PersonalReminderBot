import logging
from bson import ObjectId
from pymongo import MongoClient
from flaskapp import app, celery


@celery.task
def remind(object_id_str):
    object_id = ObjectId(object_id_str)
    logging.info("Celery task is invoked, ObjectId: " + str(object_id))
    mongo_client = MongoClient()
    db = mongo_client[app.bot.mongodb_name]
    note = db.notes.find_one({'_id': object_id})
    chat_id = note['chat_id']
    send_type = note['type']
    if send_type in app.bot.message_types:
        if send_type == 'text':
            app.bot.telegram_api.send_message(chat_id, app.bot.reminder_text % 'message' + '\n' + note['text'])
        else:
            app.bot.telegram_api.send_message(chat_id, app.bot.reminder_text % send_type)
            getattr(app.bot.telegram_api, 'send_' + send_type)(chat_id, note['file_id'])
    db.notes.delete_one({'_id': object_id})
    logging.info("Note is removed from database, ObjectId: " + str(object_id))
    mongo_client.close()
