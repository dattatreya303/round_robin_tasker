from collections import defaultdict

from telegram.ext import PicklePersistence


def run_cleanup_jobs(persistence_manager: PicklePersistence):
    unset_ongoing_conversations(persistence_manager)


def unset_ongoing_conversations(persistence_manager: PicklePersistence):
    all_chat_data: defaultdict = persistence_manager.get_chat_data()
    for chat_id, chat_data in all_chat_data.items():
        if chat_id in chat_data and chat_data[chat_id].ongoing_conversation is not None:
            chat_data[chat_id].set_ongoing_conversation(None)
            persistence_manager.update_chat_data(chat_id, chat_data)
