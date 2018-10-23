#!/usr/bin/env python
import logging
import re

import requests
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters

import config


if config.SENTRY_DSN:
    sentry_logging = LoggingIntegration(
        level=logging.INFO,        # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send no events from log messages
    )
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        environment=config.SENTRY_ENVIRONMENT,
        integrations=[sentry_logging],
    )

logging.basicConfig(level=logging.INFO)

REGEX = None
if config.REGEX:
    REGEX = re.compile(config.REGEX)


def msg(bot, update):
    logging.info(
        'Received message from `{}`: {}'.format(update.message.chat_id, update.message.text))

    if str(update.message.chat_id) not in config.ALLOWED_CHANNELS:
        logging.warning('Ignoring message from `{}`'.format(update.message.chat_id))
        # ignoring message
        return

    match = None
    if REGEX:
        match = REGEX.match(update.message.text)
        if not match:
            logging.info('Ignoring not matching message `{}`'.format(update.message.text))
            return
        logging.debug('Matched message: {}'.format(match.groupdict()))

    if config.HANDLER:
        logging.info('Sending to handler: {}'.format(config.HANDLER))
        if match:
            requests.post(config.HANDLER, json=match.groupdict())
        else:
            requests.post(config.HANDLER, data=update.message.text)


def ping(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Pong!')


updater = Updater(token=config.TOKEN)

msg_handler = MessageHandler(Filters.text, msg)
updater.dispatcher.add_handler(msg_handler)

ping_handler = CommandHandler('ping', ping)
updater.dispatcher.add_handler(ping_handler)

updater.start_polling()
updater.idle()
