import datetime

TIMEOUT_DURATION = datetime.timedelta(minutes=1)

HELP_MESSAGE = "/add_task - Create a new task.\n" \
                "/check_task - Check next turn for an existing task.\n" \
                "/list_tasks - List all active tasks in this chat.\n" \
                "/delete_task - Delete an existing task and all its data.\n" \
                "/cancel - Terminate an ongoing command.\n" \
                "/help - To know what each command does.\n\n" \
                "The bot will consider only explicit replies to continue the conversation."

START_MESSAGE = 'Hi! I am your round-robin tasker bot. You can use me to create tasks, add people who have perform the' \
                ' task turn-by-turn and ask me whose turn it is!\n' \
                'Here is list of things I can do which you might find handy:\n' + HELP_MESSAGE
