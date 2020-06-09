from telegram.ext import Updater, PicklePersistence

from Constants import FILENAME_PKL, TOKEN_TEST
from cleanup import run_cleanup_jobs
from conversations.handlers.root_handler import ROUTER_HANDLER

updater = None


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

    updater.dispatcher.add_handler(ROUTER_HANDLER)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

    run_cleanup_jobs(persistence_manager)


if __name__ == '__main__':
    main()
