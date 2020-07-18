import enum


class MainCommands(enum.Enum):
    START = 'start'
    ADD_TASK = 'add_task'
    CHECK_TASK = 'check_task'
    DELETE_TASK = 'delete_task'
    LIST_TASKS = 'list_tasks'
    HELP = 'help'
    CANCEL = 'cancel'
    INVALID_COMMAND = 'invalid_command'
