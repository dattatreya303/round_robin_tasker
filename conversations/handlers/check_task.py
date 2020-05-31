from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from conversations.callbacks.check_task import check_task_conv_start, check_task_conv_ask_name
from conversations.common import TIMEOUT_DURATION
from conversations.handlers.common import TIMEOUT_HANDLER, CANCEL_HANDLER, INVALID_COMMAND_HANDLER
from conversations.states import CheckTaskConvState

CHECK_TASK_START_HANDLER = CommandHandler('check_task', check_task_conv_start)

CHECK_TASK_ASK_NAME_HANDLER = MessageHandler(filters=Filters.text & ~Filters.command, callback=check_task_conv_ask_name)

CHECK_TASK_CONVERSATION_HANDLER = ConversationHandler(
    name='check_task_conv',
    entry_points=[CHECK_TASK_START_HANDLER],
    states={
        CheckTaskConvState.ASK_NAME: [CHECK_TASK_ASK_NAME_HANDLER],
        ConversationHandler.TIMEOUT: [TIMEOUT_HANDLER]
    },
    fallbacks=[CANCEL_HANDLER, INVALID_COMMAND_HANDLER],
    per_chat=True,
    per_user=False,
    conversation_timeout=TIMEOUT_DURATION
)
