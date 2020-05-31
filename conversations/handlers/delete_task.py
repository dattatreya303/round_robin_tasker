from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from conversations.callbacks.delete_task import delete_task_conv_start, delete_task_conv_ask_name
from conversations.common import TIMEOUT_DURATION
from conversations.handlers.common import TIMEOUT_HANDLER, CANCEL_HANDLER, INVALID_COMMAND_HANDLER
from conversations.states import DeleteTaskConvState

DELETE_TASK_START_HANDLER = CommandHandler('delete_task', delete_task_conv_start)

DELETE_TASK_ASK_NAME_HANDLER = MessageHandler(filters=Filters.text & ~Filters.command,
                                              callback=delete_task_conv_ask_name)

DELETE_TASK_CONVERSATION_HANDLER = ConversationHandler(
    name='delete_task_conv',
    entry_points=[DELETE_TASK_START_HANDLER],
    states={
        DeleteTaskConvState.ASK_NAME: [DELETE_TASK_ASK_NAME_HANDLER],
        ConversationHandler.TIMEOUT: [TIMEOUT_HANDLER]
    },
    fallbacks=[CANCEL_HANDLER, INVALID_COMMAND_HANDLER],
    per_chat=True,
    per_user=False,
    conversation_timeout=TIMEOUT_DURATION
)
