from telegram.ext import Updater, PicklePersistence

from conversations.handlers import MAIN_HANDLER_LIST
from Constants import FILENAME_PKL, TOKEN_TEST

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

    for handler in MAIN_HANDLER_LIST:
        updater.dispatcher.add_handler(handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
