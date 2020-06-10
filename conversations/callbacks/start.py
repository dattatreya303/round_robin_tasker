from telegram import Update
from telegram.ext import CallbackContext

from conversations.common import START_MESSAGE


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=START_MESSAGE)
