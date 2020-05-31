import enum
import datetime
import re
from typing import List

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, PicklePersistence, ConversationHandler, \
    MessageHandler, Filters, CallbackQueryHandler

from TaskData import TaskData
from ChatData import ChatData
from Constants import NUM_TASKS_CREATED_DATA_KEY, FILENAME_PKL, TOKEN, CANCEL_CONV_PROMPT, TOKEN_TEST, logger

updater = None


class AddTaskConvState(enum.Enum):
    ASK_NAME = enum.auto(),
    ASK_PARTICIPANTS = enum.auto()


class CheckTaskConvState(enum.Enum):
    ASK_NAME = enum.auto()


def add_task_conv_start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info('[bot][add_task_conv_start] chat id - {}'.format(chat_id))
    uid = update.message.from_user
    print('[bot][add_task_conv_start] from user - {}'.format(uid))
    if chat_id not in context.chat_data:
        context.chat_data[chat_id] = ChatData(chat_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Enter new task name.\n{}".format(CANCEL_CONV_PROMPT))
    return AddTaskConvState.ASK_NAME


def add_task_conv_ask_name(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info('[bot][add_task_conv_ask_name] chat id - {}'.format(chat_id))

    task_name: str = re.sub('\s+', ' ', update.message.text.strip())
    logger.info('[bot][add_task_conv_ask_name] task name - {}'.format(task_name))

    if task_name == '':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Enter a non empty task name.\n{}".format(CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_NAME

    if NUM_TASKS_CREATED_DATA_KEY not in context.bot_data:
        context.bot_data[NUM_TASKS_CREATED_DATA_KEY] = 0
    num_tasks_created = context.bot_data[NUM_TASKS_CREATED_DATA_KEY] + 1

    new_task = TaskData(num_tasks_created, task_name)
    if not context.chat_data[chat_id].set_transit_task(new_task):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Task already exists! Enter a different name.\n{}".format(CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_NAME

    context.bot_data[NUM_TASKS_CREATED_DATA_KEY] = num_tasks_created

    context.bot.send_message(chat_id=update.effective_chat.id, text="Enter comma-separated list of task participants.\n{}".format(CANCEL_CONV_PROMPT))

    return AddTaskConvState.ASK_PARTICIPANTS


def add_task_conv_ask_participants(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info('[bot][add_task_conv_ask_participants] chat id - {}'.format(chat_id))

    participant_list: List[str] = list(map(lambda x: re.sub('\s+', ' ', x.strip()), update.message.text.strip().split(',')))
    logger.info('[bot][add_task_conv_ask_participants] participant list - {}'.format(participant_list))

    if len(participant_list) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please enter a non-empty participant list.\n{}".format(CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_PARTICIPANTS

    transit_task: TaskData = context.chat_data[chat_id].transit_task

    if not transit_task.add_participant_list(participant_list):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="One of the names already exists in the participant list. Enter a valid list\n{}".format(CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_PARTICIPANTS

    if not context.chat_data[chat_id].add_task(transit_task):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Task already exists! Enter a different name.\n{}".format(CANCEL_CONV_PROMPT))
        return AddTaskConvState.ASK_NAME

    context.chat_data[chat_id].remove_transit_task()

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Task: {} created!".format(transit_task.name))

    return ConversationHandler.END


def conv_timeout(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Conversation timed out.")
    return ConversationHandler.END


def add_task_conv_end(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Command terminated.")
    return ConversationHandler.END


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


def bot_help(update: Update, context: CallbackContext):
    help_string = "/add_task - Create a new task.\n" \
                  "/check_task - Check updates on an existing task.\n" \
                  "/cancel - Terminate an ongoing command.\n" \
                  "/help - To know what each command does.\n\n" \
                  "The bot will consider only explicit replies to continue the conversation."
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_string)


def main():
    global updater

    # Create persistence manager object
    persistence_manager = PicklePersistence(filename=FILENAME_PKL,
                                            store_user_data=False,
                                            store_chat_data=True,
                                            store_bot_data=True,
                                            single_file=False,
                                            on_flush=False)

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN_TEST, persistence=persistence_manager, use_context=True)

    updater.dispatcher.add_handler(ConversationHandler(
        name='add_task_conv',
        entry_points=[CommandHandler('add_task', add_task_conv_start)],
        states={
            AddTaskConvState.ASK_NAME: [
                MessageHandler(filters=Filters.text & ~Filters.command, callback=add_task_conv_ask_name)],
            AddTaskConvState.ASK_PARTICIPANTS: [
                MessageHandler(filters=Filters.text & ~Filters.command, callback=add_task_conv_ask_participants)],
            ConversationHandler.TIMEOUT: [MessageHandler(filters=Filters.text, callback=conv_timeout)]
        },
        fallbacks=[CommandHandler('cancel', add_task_conv_end)],
        per_chat=True,
        per_user=False,
        conversation_timeout=datetime.timedelta(minutes=1)
    ))

    # updater.dispatcher.add_handler(CommandHandler('check_task', check_task))
    updater.dispatcher.add_handler(ConversationHandler(
        name='check_task_conv',
        entry_points=[CommandHandler('check_task', check_task_conv_start)],
        states={
            CheckTaskConvState.ASK_NAME: [
                MessageHandler(filters=Filters.text & ~Filters.command, callback=check_task_conv_ask_name)],
            ConversationHandler.TIMEOUT: [MessageHandler(filters=Filters.text, callback=conv_timeout)]
        },
        fallbacks=[CommandHandler('cancel', add_task_conv_end)],
        per_chat=True,
        per_user=False,
        conversation_timeout=datetime.timedelta(minutes=1)
    ))

    updater.dispatcher.add_handler(CommandHandler('help', bot_help))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
