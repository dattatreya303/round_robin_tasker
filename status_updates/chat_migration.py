from telegram import Update
from telegram.ext import MessageHandler, Filters, CallbackContext


def chat_migration_callback(update: Update, context: CallbackContext):
    update_message = update.message
    dp = context.dispatcher  # available since version 12.4

    # Get old and new chat ids
    old_id = update_message.migrate_from_chat_id or update_message.chat_id
    new_id = update_message.migrate_to_chat_id or update_message.chat_id

    # transfer data, if old data is still present
    if old_id in dp.chat_data:
        dp.chat_data[new_id].update(dp.chat_data.get(old_id))
        del dp.chat_data[old_id]


CHAT_MIGRATION_HANDLER = MessageHandler(Filters.status_update.migrate, chat_migration_callback)
