import enum


class MainCommands(enum.Enum):
    ADD_TASK = 'add_task'
    CHECK_TASK = 'check_task'
    DELETE_TASK = 'delete_task'
    LIST_TASKS = 'list_tasks'
    HELP = 'help'
    CANCEL = 'cancel'
