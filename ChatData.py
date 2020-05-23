from TaskData import TaskData


class ChatData(object):
    def __init__(self, chat_id, task_list: list = []):
        self.__id = chat_id
        self.__task_list = task_list

    @property
    def id(self):
        return self.__id

    @property
    def task_list(self):
        return self.__task_list

    def check_task_exists_by_id(self, task_id: int):
        for task_data in self.__task_list:
            if task_data.id == task_id:
                return True
        return False

    def check_task_exists_by_name(self, task_name: str):
        for task_data in self.__task_list:
            if task_data.name == task_name:
                return True
        return False

    def add_task(self, task_data: TaskData):
        if not self.check_task_exists_by_name(task_data.name):
            self.__task_list.append(task_data)

    def get_task_by_name(self, task_name):
        for task_data in self.__task_list:
            if task_name == task_data.name:
                return task_data
        return None
