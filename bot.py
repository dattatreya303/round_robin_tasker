import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, PicklePersistence

from TaskData import TaskData
from ChatData import ChatData
from constants import NUM_TASKS_CREATED_DATA_KEY, FILENAME_PKL, TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

updater = None


def add_task(update: Update, context: CallbackContext):

    chat_id = update.effective_chat.id
    print('chat id', chat_id)

    print('args: ', context.args)
    if len(context.args) < 2 or (',' in context.args[0]):
        help(update, context)
        return

    task_name = context.args[0].strip()
    print('task name: ', task_name)

    participant_list = context.args[1].split(',')

    if NUM_TASKS_CREATED_DATA_KEY not in context.bot_data:
        context.bot_data[NUM_TASKS_CREATED_DATA_KEY] = 0
    num_tasks_created = context.bot_data[NUM_TASKS_CREATED_DATA_KEY]

    num_tasks_created += 1
    context.bot_data[NUM_TASKS_CREATED_DATA_KEY] = num_tasks_created

    new_task = TaskData(num_tasks_created, task_name, participant_list)

    if chat_id not in context.chat_data:
        context.chat_data[chat_id] = ChatData(chat_id)
    context.chat_data[chat_id].add_task(new_task)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Task: {} created!".format(task_name))


def check_task(update: Update, context: CallbackContext):
    print('args: ', context.args)
    if len(context.args) < 1:
        help(update, context)
        return
    task_name = context.args[0]

    chat_id = update.effective_chat.id
    print('chat id', chat_id)
    if chat_id not in context.chat_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No tasks exist for this chat!")
        return

    chat_data: ChatData = context.chat_data[chat_id]
    task_data: TaskData = chat_data.get_task_by_name(task_name)
    if task_data is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Task {} doesn't exist!".format(task_name))
        return

    next_name = task_data.who()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Task: {} - {}\'s turn!!".format(task_name, next_name))


def help(update: Update, context: CallbackContext):
    help_string = "Use /add_task with args: <taskName> <participants-csv>." \
                  "\nUse /check_task with args: <taskName>."
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
    updater = Updater(TOKEN, persistence=persistence_manager, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('add_task', add_task))
    updater.dispatcher.add_handler(CommandHandler('check_task', check_task))
    updater.dispatcher.add_handler(CommandHandler('help', help))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
