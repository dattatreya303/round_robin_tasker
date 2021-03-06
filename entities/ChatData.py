from conversations.commands import MainCommands
from entities.TaskData import TaskData


class ChatData(object):
    def __init__(self, chat_id: int, task_list: list = []):
        self.__id = chat_id
        self.__task_list = task_list
        # TODO: In-memory cache
        self.__ongoing_conversation: MainCommands = None
        # TODO: In-memory cache
        self.__transit_task: TaskData = None

    @property
    def id(self):
        return self.__id

    @property
    def task_list(self):
        return self.__task_list

    @property
    def transit_task(self):
        return self.__transit_task

    @property
    def ongoing_conversation(self):
        return self.__ongoing_conversation

    def check_task_exists_by_id(self, task_id: int) -> bool:
        for task_data in self.__task_list:
            if task_data.id == task_id:
                return True
        return False

    def check_task_exists_by_name(self, task_name: str) -> bool:
        for task_data in self.__task_list:
            if task_data.name.lower() == task_name.lower():
                return True
        return False

    def set_transit_task(self, task_data: TaskData) -> int:
        if not self.check_task_exists_by_name(task_data.name):
            self.__transit_task = task_data
            return 1
        return 0

    def remove_transit_task(self):
        self.__transit_task = None

    def add_task(self, task_data: TaskData) -> int:
        if not self.check_task_exists_by_name(task_data.name):
            self.__task_list.append(task_data)
            return 1
        return 0

    def get_task_by_name(self, task_name: str) -> TaskData:
        for task_data in self.__task_list:
            if task_name.lower() == task_data.name.lower():
                return task_data
        return None

    def remove_task_by_name(self, task_name: str) -> bool:
        for i, task_data in enumerate(self.__task_list):
            if task_name.lower() == task_data.name.lower():
                del self.__task_list[i]
                return True
        return False

    def set_ongoing_conversation(self, ongoing_conversation_state: MainCommands):
        self.__ongoing_conversation = ongoing_conversation_state
