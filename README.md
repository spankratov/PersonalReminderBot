# Personal Reminder Bot
A simple Telegram bot you could send all your notes to. When you give him an input he will remind you about them later.

Right now this bot is able to:

1. Resend your notes to your in time you specified in your note in arbitary format (like "remind me tomorrow" or "send me this note in 1 hour, 30 minutes". If date and time are not specified, the bot will remind you in the default time (one day).

2. Resend your photos, audios, documents, voice messages and videos in default time (one day).

The bot is written in Python 2.7, it uses Flask, mongodb, celery and rabbitmq. It's still under development, other features and documentation are coming soon.

You are welcome to visit the bot [here](http://telegram.me/PersonalReminderBot)

This project is licensed under the terms of the MIT license.
