from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from Constants import logger, CANCEL_CONV_PROMPT
from conversations.states import DeleteTaskConvState
from entities import ChatData


def delete_task_conv_start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info('[bot][delete_task_conv_start] chat id - {}'.format(chat_id))
    uid = update.message.from_user
    logger.info('[bot][delete_task_conv_start] from user - {}'.format(uid))

    if len(context.chat_data[chat_id].task_list) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No tasks exist for this chat!")
        return ConversationHandler.END

    context.bot.send_message(chat_id=update.effective_chat.id, text="Enter task name.\n{}".format(CANCEL_CONV_PROMPT))

    return DeleteTaskConvState.ASK_NAME


def delete_task_conv_ask_name(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    chat_data: ChatData = context.chat_data[chat_id]

    task_name = update.message.text.strip()

    if len(task_name) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please enter a non-empty task_name.\n{}".format(CANCEL_CONV_PROMPT))
        return DeleteTaskConvState.ASK_NAME

    if not chat_data.remove_task_by_name(task_name):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Task {} doesn't exist!".format(task_name))
        return ConversationHandler.END

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Task: {} deleted!".format(task_name))

    return ConversationHandler.END
