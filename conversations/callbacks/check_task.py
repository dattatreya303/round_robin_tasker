from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from Constants import logger, CANCEL_CONV_PROMPT
from entities import ChatData, TaskData


def check_task_conv_start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info('[bot][check_task_conv_start] chat id - {}'.format(chat_id))
    uid = update.message.from_user
    print('[bot][add_task_conv_start] from user - {}'.format(uid))

    if len(context.chat_data[chat_id].task_list) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No tasks exist for this chat!")
        return ConversationHandler.END

    context.bot.send_message(chat_id=update.effective_chat.id, text="Enter task name.\n{}".format(CANCEL_CONV_PROMPT))

    return CheckTaskConvState.ASK_NAME


def check_task_conv_ask_name(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    chat_data: ChatData = context.chat_data[chat_id]
    task_name = update.message.text.strip()

    if len(task_name) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please enter a non-empty task_name.\n{}".format(CANCEL_CONV_PROMPT))
        return CheckTaskConvState.ASK_NAME

    task_data: TaskData = chat_data.get_task_by_name(task_name=task_name)

    if task_data is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Task {} doesn't exist!".format(task_name))
        return ConversationHandler.END

    next_name = task_data.who()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Task: {} - {}\'s turn!!".format(task_name, next_name))

    return ConversationHandler.END
