import re
from typing import List

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from Constants import logger, NUM_TASKS_CREATED_DATA_KEY, CANCEL_CONV_PROMPT
from conversations.commands import MainCommands
from conversations.states import AddTaskConvState
from entities.ChatData import ChatData
from entities.TaskData import TaskData


def add_task_conv_start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info('[bot][add_task_conv_start] chat id - {}'.format(chat_id))
    uid = update.message.from_user
    logger.info('[bot][add_task_conv_start] from user - {}'.format(uid))
    if chat_id not in context.chat_data:
        context.chat_data[chat_id] = ChatData(chat_id)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Enter new task name.\n{}".format(CANCEL_CONV_PROMPT))
    context.chat_data[chat_id].set_ongoing_conversation(MainCommands.ADD_TASK)
    return AddTaskConvState.ASK_NAME


def add_task_conv_ask_name(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info('[bot][add_task_conv_ask_name] chat id - {}'.format(chat_id))

    task_name: str = re.sub('\s+', ' ', update.message.text.strip())
    logger.info('[bot][add_task_conv_ask_name] task name - {}'.format(task_name))

    if task_name == '':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Enter a non empty task name.\n{}".format(CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_NAME

    if NUM_TASKS_CREATED_DATA_KEY not in context.bot_data:
        context.bot_data[NUM_TASKS_CREATED_DATA_KEY] = 0
    num_tasks_created = context.bot_data[NUM_TASKS_CREATED_DATA_KEY] + 1

    new_task = TaskData(num_tasks_created, task_name)
    if not context.chat_data[chat_id].set_transit_task(new_task):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Task already exists! Enter a different name.\n{}".format(CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_NAME

    context.bot_data[NUM_TASKS_CREATED_DATA_KEY] = num_tasks_created

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Enter comma-separated list of task participants.\n{}".format(CANCEL_CONV_PROMPT))

    return AddTaskConvState.ASK_PARTICIPANTS


def add_task_conv_ask_participants(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info('[bot][add_task_conv_ask_participants] chat id - {}'.format(chat_id))
    participant_list: List[str] = list(
        map(lambda x: re.sub('\s+', ' ', x.strip()), update.message.text.strip().split(',')))
    logger.info('[bot][add_task_conv_ask_participants] participant list - {}'.format(participant_list))
    if len(participant_list) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please enter a non-empty participant list.\n{}".format(CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_PARTICIPANTS
    transit_task: TaskData = context.chat_data[chat_id].transit_task
    if not transit_task.add_participant_list(participant_list):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="One of the names already exists in the participant list. Enter a valid list\n{}".format(
                                     CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_PARTICIPANTS
    if not context.chat_data[chat_id].add_task(transit_task):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Task already exists! Enter a different name.\n{}".format(CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_NAME
    context.chat_data[chat_id].remove_transit_task()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Task: {} created!".format(transit_task.name))
    context.chat_data[chat_id].set_ongoing_conversation(None)
    return ConversationHandler.END
