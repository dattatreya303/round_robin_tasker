[![dattatreya303](https://circleci.com/gh/dattatreya303/round_robin_tasker.svg?style=shield)](https://circleci.com/gh/dattatreya303/round_robin_tasker)

# round_robin_tasker
A telegram bot for groups to assign a task to members in a round robin manner.

## Commands supported by the bot
1. `/add_task` - Create a new task
2. `/check_task` - Check next turn for an existing task
3. `/list_tasks` - List all active tasks in this chat
4. `/delete_task` - Delete an existing task and all its data
5. `/cancel` - Terminate an ongoing command
6. `/help` - To know what each command does

The bot will consider only explicit replies to continue the conversation. 

## Contributing

### Install dependencies
- Python 3.7.2
- Create a virtual environment: `virtualenv venv && source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`

### Generate test reports for changes
- Run tests: `pytest --junitxml test-results/pytests.xml --cov=. --cov-report xml`
- Test summary: `test-results/pytests.xml`
- Coverage report: `coverage.xml`

### Starting the server
- Create a test bot using [BotFather](https://t.me/BotFather) on Telegram.
- Set secrets as environment variables by running the following script:
  ```bash
    #!/bin/sh
    export RRT_TOKEN="<test-bot-token>"
    export RRT_PERSISTENCE_PREFIX="<path-and-prefix-for-chat-data-store"
  ```
- Start server: `python bot.py`