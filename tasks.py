from datetime import datetime
import logging
import re

from dateutil.parser import parse as parse_datetime
from dateutil.relativedelta import relativedelta
from flaskapp import app, celery

dates_words = ['year', 'month', 'week', 'day', 'hour', 'minute', 'second']
in_general = r'(((?P<{0}>1) {0}|(?P<{0}s>\d+) {0}s))'
in_patterns = []
for word in dates_words:
    in_patterns.append(in_general.format(word))
in_altogether_regex = re.compile(r'in ' + r'(' + r'|'.join([pattern + r',? ?' for pattern in in_patterns]) + r')+', re.IGNORECASE)
words_pattern = re.compile(r'(?P<word_date>tomorrow|tonight|today|day after tomorrow|next week|next month|next year|end of this week)', re.IGNORECASE)


def process_word_for_date(word, now):
    if word == 'tomorrow':
        tomorrow = now + relativedelta(days=1)
        return tomorrow, {'year': True, 'month': True, 'day': True, 'time': False}
    elif word == 'tonight':
        tonight = datetime(year=now.year, month=now.month, day=now.day, hour=22)
        if now > tonight:
            return now, {'year': True, 'month': True, 'day': True, 'time': True}
        else:
            return tonight, {'year': True, 'month': True, 'day': True, 'time': True}
    elif word == 'today':
        today = now + relativedelta(hours=1)
        if now.day == today.day:
            return today, {'year': True, 'month': True, 'day': True, 'time': True}
        else:
            return datetime(year=now.year, month=now.month, day=now.day, hour=23, minute=59, second=59), {'year': True, 'month': True, 'day': True, 'time': True}
    elif word == 'day after tomorrow':
        tomorrow = now + relativedelta(days=2)
        return tomorrow, {'year': True, 'month': True, 'day': True, 'time': False}
    elif word == 'next week':
        next_week = now + relativedelta(weeks=1)
        return next_week, {'year': False, 'month': False, 'day': False, 'time': False}
    elif word == 'next month':
        next_month = now + relativedelta(months=1)
        return next_month, {'year': True, 'month': True, 'day': False, 'time': False}
    elif word == 'next year':
        next_year = now + relativedelta(years=1)
        return next_year, {'year': True, 'month': False, 'day': False, 'time': False}
    elif word == 'end of this week':
        end_of_week = now - relativedelta(days=now.weekday()) + relativedelta(days=6)
        return end_of_week, {'year': True, 'month': True, 'day': True, 'time': False}


@celery.task
def detect_datetime(text, default_delay):
    logging.info("Celery task 'detect_datetime' is invoked, text: {}, delay: {}".format(text, default_delay))
    user_now = datetime.utcnow()
    result = user_now
    changed = False

    matches = re.finditer(in_altogether_regex, text)
    for match in matches:
        changed = True
        for word in dates_words:
            word_value = match.group(word) or match.group(word + 's')
            if word_value:
                result += relativedelta(**{word + 's': int(word_value)})
    if changed:
        return result

    match = re.search(words_pattern, text)
    if match:
        word = match.group()
        result, flags = process_word_for_date(word, result)
        changed = True
    else:
        flags = {'year': False, 'month': False, 'day': False, 'time': False}

    try:
        parsed_datetime, tokens = parse_datetime(text, default=result, dayfirst=True, fuzzy_with_tokens=True)
    except ValueError:
        if changed:
            return result
        else:
            return user_now + relativedelta(microseconds=default_delay)

    # test if parsed string contains only digits
    # dateutil.parser recognise alone digits as the part of the date
    # e.g. "catch 6 monkeys" with default=datetime(2016, 7, 29, 18, 20, 44, 667349) is parsed as datetime(2016, 7, 6, 18, 20, 44, 667349)
    parsed_string = text
    for token in tokens:
        parsed_string = parsed_string.replace(token, '')
    match = re.match(r'^[\d\d]+$', parsed_string)
    if match:
        return result

    if not flags['year']:
        result = result.replace(year=parsed_datetime.year)
    if not flags['month']:
        result = result.replace(month=parsed_datetime.month)
    if not flags['day']:
        result = result.replace(day=parsed_datetime.day)
    if not flags['time']:
        result = result.replace(hour=parsed_datetime.hour, minute=parsed_datetime.minute, second=parsed_datetime.second,
                                microsecond=parsed_datetime.microsecond)
    return result - relativedelta(hours=3)  # temporary fix for incorrect timezone


@celery.task
def remind(chat_id, send_type, content):
    logging.info("Celery task 'remind' is invoked, chat_id: {}, send_type: {}, content: {}".format(chat_id, send_type, content))
    if send_type in app.bot.message_types:
        if send_type == 'text':
            app.bot.telegram_api.send_message(chat_id, app.bot.reminder_text % 'message' + '\n' + content)
        else:
            app.bot.telegram_api.send_message(chat_id, app.bot.reminder_text % send_type)
            getattr(app.bot.telegram_api, 'send_' + send_type)(chat_id, content)
