from conversations.handlers.add_task import ADD_TASK_CONVERSATION_HANDLER
from conversations.handlers.check_task import CHECK_TASK_CONVERSATION_HANDLER
from conversations.handlers.common import HELP_HANDLER
from conversations.handlers.delete_task import DELETE_TASK_CONVERSATION_HANDLER
from conversations.handlers.list_tasks import LIST_TASKS_CONVERSATION_HANDLER

MAIN_HANDLER_LIST = [
    ADD_TASK_CONVERSATION_HANDLER,
    CHECK_TASK_CONVERSATION_HANDLER,
    DELETE_TASK_CONVERSATION_HANDLER,
    LIST_TASKS_CONVERSATION_HANDLER,
    HELP_HANDLER
]
