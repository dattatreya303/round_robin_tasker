from telegram.ext import MessageHandler, Filters, CommandHandler

from conversations.callbacks.common import conv_timeout, bot_help, conv_end, conv_invalid_command
from conversations.common import CANCEL_COMMAND

HELP_HANDLER = CommandHandler('help', bot_help)

TIMEOUT_HANDLER = MessageHandler(filters=Filters.text, callback=conv_timeout)

CANCEL_HANDLER = CommandHandler(CANCEL_COMMAND, callback=conv_end)

INVALID_COMMAND_HANDLER = MessageHandler(Filters.command, callback=conv_invalid_command)
