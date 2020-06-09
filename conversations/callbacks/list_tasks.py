from typing import List

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from Constants import logger
from entities.TaskData import TaskData


def list_tasks(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info('[bot][list_tasks_conv_start] chat id - {}'.format(chat_id))
    uid = update.message.from_user
    logger.info('[bot][list_tasks_conv_start] from user - {}'.format(uid))
    if chat_id not in context.chat_data or len(context.chat_data[chat_id].task_list) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No tasks exist for this chat!")
        return
    task_list: List[TaskData] = context.chat_data[chat_id].task_list
    task_list_str = '\n\n'.join(['Task: `{}`, Members: {}'.format(task_data.name, ', '.join(
        map(lambda x: x.user_name, task_data.participants))) for task_data in task_list])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Tasks in this chat:\n{}".format(task_list_str),
                             parse_mode=ParseMode.MARKDOWN_V2)
