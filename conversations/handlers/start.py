from telegram.ext import CommandHandler

from conversations.callbacks.start import start
from conversations.commands import MainCommands

START_CONVERSATION_HANDLER = CommandHandler(MainCommands.START.value, start)
