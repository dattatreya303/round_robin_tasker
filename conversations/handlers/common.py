from telegram.ext import MessageHandler, Filters, CommandHandler

from conversations.callbacks.common import conv_timeout, bot_help, conv_end, conv_invalid_response, root_conv_end
from conversations.commands import MainCommands

HELP_HANDLER = CommandHandler(MainCommands.HELP.value, bot_help)

TIMEOUT_HANDLER = MessageHandler(filters=Filters.text, callback=conv_timeout)

CANCEL_HANDLER = CommandHandler(MainCommands.CANCEL.value, callback=conv_end)

ROOT_CANCEL_HANDLER = CommandHandler(MainCommands.CANCEL.value, callback=root_conv_end)

INVALID_COMMAND_HANDLER = MessageHandler(Filters.command | Filters.text, callback=conv_invalid_response)
