import unittest
from reminder_bot import PersonalReminderBot
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TestDetectDatetime(unittest.TestCase):
    def setUp(self):
        config = {'TELEGRAM_URL': '', 'CERTIFICATE': '', 'WEBHOOK_URL': '',
                  'DEFAULT_REMINDER_TEXT': '', 'DEFAULT_MESSAGE_TYPES': '',
                  'DEFAULT_REMINDER_DELAY': 1000 * 1000 * 3600 * 24}
        self.bot = PersonalReminderBot(config)

    def test_ins(self):
        dt = datetime.now()
        detected = self.bot.detect_datetime('in 3 years remind me in 10 minutes', dt)
        self.assertEqual(detected, dt + relativedelta(years=3, minutes=10))
        detected = self.bot.detect_datetime('remind me in 3 years, 1 month, 56 weeks, 3 seconds', dt)
        self.assertEqual(detected, dt + relativedelta(years=3, months=1, weeks=56, seconds=3))
        detected = self.bot.detect_datetime('in this chat remind me in 3 years, 1 month, 56 weeks, 3 seconds', dt)
        self.assertEqual(detected, dt + relativedelta(years=3, months=1, weeks=56, seconds=3))
        detected = self.bot.detect_datetime('in 1 year, 3 seconds in 10 seconds remind me in 5 minutes', dt)
        self.assertEqual(detected, dt + relativedelta(years=1, minutes=5, seconds=13))

    def test_words(self):
        dt = datetime.now()
        detected = self.bot.detect_datetime('remind me tomorrow', dt)
        self.assertEqual(detected, dt + relativedelta(days=1))
        detected = self.bot.detect_datetime('remind me tomorrow at 8 pm', dt)
        self.assertEqual(detected, (dt + relativedelta(days=1)).replace(hour=20))
        dt = datetime(year=2016, month=7, day=30, hour=23, minute=30)
        detected = self.bot.detect_datetime('today reminder would be nice', dt)
        self.assertEqual(detected, dt.replace(hour=23, minute=59, second=59, microsecond=0))
        detected = self.bot.detect_datetime('remind me next week at sunday', dt)
        self.assertEqual(detected, dt.replace(month=8, day=7))
        detected = self.bot.detect_datetime('remind me next year at 7 Jan 17:33', dt)
        self.assertEqual(detected, dt.replace(year=2017, month=1, day=7, hour=17, minute=33))

    def test_parse(self):
        dt = datetime.now()
        detected = self.bot.detect_datetime('reminder at Thu Sep 25 10:36:28 2003', dt)
        self.assertEqual(detected, datetime(2003, 9, 25, 10, 36, 28))

if __name__ == '__main__':
    unittest.main()
