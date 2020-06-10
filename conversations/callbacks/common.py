from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from Constants import logger
from conversations.common import HELP_MESSAGE


def bot_help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_MESSAGE)


def conv_invalid_response(update: Update, context: CallbackContext):
    logger.info('[conv_invalid_response] message text: {}'.format(update.message.text))
    chat_id = update.effective_chat.id
    if chat_id in context.chat_data:
        context.chat_data[chat_id].set_ongoing_conversation(None)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid response. Command terminated.")
    return ConversationHandler.END


def conv_timeout(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in context.chat_data:
        context.chat_data[chat_id].set_ongoing_conversation(None)
    context.bot.send_message(chat_id=chat_id, text="Conversation timed out.")
    return ConversationHandler.END


def root_conv_end(update: Update, context: CallbackContext):
    logger.info('[root_conv_end]')
    chat_id = update.effective_chat.id
    if chat_id in context.chat_data:
        context.chat_data[chat_id].set_ongoing_conversation(None)
    return ConversationHandler.END


def conv_end(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in context.chat_data:
        context.chat_data[chat_id].set_ongoing_conversation(None)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Command terminated.")
    return ConversationHandler.END
