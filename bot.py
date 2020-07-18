from telegram.ext import Updater, PicklePersistence

from cleanup import run_cleanup_jobs
from conversations.handlers.root_handler import ROUTER_HANDLER
from vault import set_env_vars_map, get_token, get_persistence_filename_prefix
from status_updates.chat_migration import CHAT_MIGRATION_HANDLER

updater = None


def main():
    global updater

    # Read all prod/test environment-specific runtime variables into a global map
    set_env_vars_map()

    # Create persistence manager object
    persistence_manager = PicklePersistence(filename=get_persistence_filename_prefix(),
                                            store_user_data=False,
                                            store_chat_data=True,
                                            store_bot_data=True,
                                            single_file=False,
                                            on_flush=False)

    # Create the Updater and pass it your bot's token.
    updater = Updater(get_token(), persistence=persistence_manager, use_context=True)

    # Add status update handler for chat migrations
    updater.dispatcher.add_handler(CHAT_MIGRATION_HANDLER)

    # Add root handler for routing task commands
    updater.dispatcher.add_handler(ROUTER_HANDLER)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

    run_cleanup_jobs(persistence_manager)


if __name__ == '__main__':
    main()
