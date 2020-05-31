from telegram.ext import CommandHandler

from conversations.callbacks.list_tasks import list_tasks

LIST_TASKS_CONVERSATION_HANDLER = CommandHandler('list_tasks', list_tasks)
