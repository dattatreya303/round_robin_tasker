from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from conversations.callbacks.add_task import add_task_conv_start, add_task_conv_ask_name, \
    add_task_conv_ask_participants, add_task_conv_end
from conversations.common import CANCEL_COMMAND, TIMEOUT_DURATION
from conversations.handlers.common import TIMEOUT_HANDLER
from conversations.states import AddTaskConvState

ADD_TASK_START_HANDLER = CommandHandler('add_task', add_task_conv_start)

ADD_TASK_ASK_NAME_HANDLER = MessageHandler(filters=Filters.text & ~Filters.command, callback=add_task_conv_ask_name)

ADD_TASK_ASK_PARTICIPANTS_HANDLER = MessageHandler(filters=Filters.text & ~Filters.command, callback=add_task_conv_ask_participants)

ADD_TASK_CANCEL_HANDLER = CommandHandler(CANCEL_COMMAND, add_task_conv_end)

ADD_TASK_CONVERSATION_HANDLER = ConversationHandler(
    name='add_task_conv',
    entry_points=[ADD_TASK_START_HANDLER],
    states={
        AddTaskConvState.ASK_NAME: [ADD_TASK_ASK_NAME_HANDLER],
        AddTaskConvState.ASK_PARTICIPANTS: [ADD_TASK_ASK_PARTICIPANTS_HANDLER],
        ConversationHandler.TIMEOUT: [TIMEOUT_HANDLER]
    },
    fallbacks=[ADD_TASK_CANCEL_HANDLER],
    per_chat=True,
    per_user=False,
    conversation_timeout=TIMEOUT_DURATION
)
