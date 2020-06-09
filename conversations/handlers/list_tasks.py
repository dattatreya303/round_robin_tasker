from telegram.ext import CommandHandler

from conversations.callbacks.list_tasks import list_tasks
from conversations.commands import MainCommands

LIST_TASKS_CONVERSATION_HANDLER = CommandHandler(MainCommands.LIST_TASKS.value, list_tasks)
