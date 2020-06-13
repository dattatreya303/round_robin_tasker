from entities.TaskData import TaskData
from entities.UserData import UserData


class TestTaskDataMethods:
    def test_who(self):
        user_a = UserData('a')
        user_b = UserData('b')
        user_c = UserData('c')
        task_data = TaskData(123, 'test_task', [user_a, user_b, user_c])
        assert task_data.who() == user_a.user_name
        assert task_data.who() == user_b.user_name
        assert task_data.who() == user_c.user_name
