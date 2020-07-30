from typing import Dict

from telegram import Update, MessageEntity
from telegram.ext import CallbackContext, Handler

from Constants import logger
from conversations.commands import MainCommands
from conversations.handlers import ADD_TASK_CONVERSATION_HANDLER, CHECK_TASK_CONVERSATION_HANDLER, \
    LIST_TASKS_CONVERSATION_HANDLER, DELETE_TASK_CONVERSATION_HANDLER
from conversations.handlers.common import ROOT_CANCEL_HANDLER, HELP_HANDLER, INVALID_COMMAND_HANDLER
from conversations.handlers.start import START_CONVERSATION_HANDLER
from entities.ChatData import ChatData

switcher_v2: Dict[str, Handler] = {
    MainCommands.START.value: START_CONVERSATION_HANDLER,
    MainCommands.ADD_TASK.value: ADD_TASK_CONVERSATION_HANDLER,
    MainCommands.CHECK_TASK.value: CHECK_TASK_CONVERSATION_HANDLER,
    MainCommands.LIST_TASKS.value: LIST_TASKS_CONVERSATION_HANDLER,
    MainCommands.DELETE_TASK.value: DELETE_TASK_CONVERSATION_HANDLER,
    MainCommands.INVALID_COMMAND.value : INVALID_COMMAND_HANDLER,
    MainCommands.HELP.value: HELP_HANDLER,
    MainCommands.CANCEL.value: ROOT_CANCEL_HANDLER,
}


def root_router_v2(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info("[root_router] Entered conv again {}".format(chat_id))
    command = update.message.text.split('@')[0].lstrip('/')
    logger.info('[root_router] command: {}'.format(command))
    handler = find_handler(command, chat_id, context.chat_data)
    check = handler.check_update(update)
    logger.info('[root_router] check: {}'.format(check))
    if check is None or check is False:
        handler = INVALID_COMMAND_HANDLER
        check = handler.check_update(update)
        logger.error('[root_router] check is false or none')
    handler.handle_update(update, context.dispatcher, check, context)


def find_handler(command: str, chat_id: int, chat_data: ChatData):
    if chat_id in chat_data:
        chat_data: ChatData = chat_data[chat_id]
        ongoing_conv: MainCommands = chat_data.ongoing_conversation
        if ongoing_conv is not None:
            logger.info('[find_handler] ongoing_conv: {}'.format(ongoing_conv.value))
            return find_in_command_switcher(ongoing_conv.value)
    logger.info('[find_handler] switcher key: {}'.format(command))
    return find_in_command_switcher(command)


def find_in_command_switcher(command):
    if command in switcher_v2:
        return switcher_v2[command]
    return switcher_v2[MainCommands.INVALID_COMMAND.value]
