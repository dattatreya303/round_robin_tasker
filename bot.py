import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from TaskData import TaskData
from ChatData import ChatData

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "958111367:AAFbNEDl0V6KJxKLq64P0zHf2YwWefo4Mxc"

updater = None

chat_map = dict()
num_tasks_created = 0


def add_task(update: Update, context: CallbackContext):
    global num_tasks_created

    chat_id = update.effective_chat.id
    print('chat id', chat_id)

    print('args: ', context.args)
    if len(context.args) < 2 or (',' in context.args[0]):
        help(update, context)
        return

    task_name = context.args[0].strip()
    print('task name: ', task_name)

    participant_list = context.args[1].split(',')

    new_task = TaskData(num_tasks_created + 1, task_name, participant_list)
    num_tasks_created += 1

    if chat_id not in chat_map:
        new_chat = ChatData(chat_id)
        chat_map[chat_id] = new_chat
    chat_map[chat_id].add_task(new_task)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Task: {} created!".format(task_name))


def check_task(update: Update, context: CallbackContext):
    print('args: ', context.args)
    if len(context.args) < 1:
        help(update, context)
        return
    task_name = context.args[0]

    chat_id = update.effective_chat.id
    print('chat id', chat_id)
    if chat_id not in chat_map:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No tasks exist for this chat!")
        return

    chat_data: ChatData = chat_map[chat_id]
    task_data: TaskData = chat_data.get_task_by_name(task_name)
    if task_data is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Task {} doesn't exist!".format(task_name))
        return

    next_name = task_data.who()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Task: {} - {}\'s turn!!".format(task_name, next_name))


def echo(update: Update, context: CallbackContext):
    query = update.callback_query.data
    print(query.data)
    context.bot.send_message(chat_id=update.effective_chat.id, text=query.data)


def help(update: Update, context: CallbackContext):
    help_string = "Use /add_task with args: <taskName> <participants-csv>." \
                  "\nUse /check_task with args: <taskName>."
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_string)


def main():
    global updater

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('add_task', add_task))
    updater.dispatcher.add_handler(CommandHandler('check_task', check_task))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
