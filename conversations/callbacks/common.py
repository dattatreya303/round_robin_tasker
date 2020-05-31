from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


def bot_help(update: Update, context: CallbackContext):
    help_string = "/add_task - Create a new task.\n" \
                  "/check_task - Check next turn for an existing task.\n" \
                  "/list_tasks - List all active tasks in this chat.\n" \
                  "/delete_task - Delete an existing task and all its data.\n" \
                  "/cancel - Terminate an ongoing command.\n" \
                  "/help - To know what each command does.\n\n" \
                  "The bot will consider only explicit replies to continue the conversation."
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_string)


def conv_invalid_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid response. Command terminated.")
    return ConversationHandler.END


def conv_timeout(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Conversation timed out.")
    return ConversationHandler.END


def conv_end(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Command terminated.")
    return ConversationHandler.END
