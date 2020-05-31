from telegram.ext import MessageHandler, Filters, CommandHandler

from conversations.callbacks.common import conv_timeout, bot_help

TIMEOUT_HANDLER = MessageHandler(filters=Filters.text, callback=conv_timeout)

HELP_HANDLER = CommandHandler('help', bot_help)
