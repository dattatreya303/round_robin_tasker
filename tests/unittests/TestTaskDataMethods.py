import pytest

from entities.TaskData import TaskData
from entities.UserData import UserData


class TestTaskDataMethods:
    @pytest.fixture(scope='module')
    def sample_user_a(self):
        return UserData('a')

    @pytest.fixture(scope='module')
    def sample_user_b(self):
        return UserData('b')

    @pytest.fixture(scope='module')
    def sample_user_c(self):
        return UserData('c')

    @pytest.fixture
    def sample_task_abc(self, sample_user_a, sample_user_b, sample_user_c):
        return TaskData(123, 'sample_task_abc', [sample_user_a, sample_user_b, sample_user_c])

    @pytest.fixture
    def sample_task_empty(self):
        return TaskData(321, 'sample_task_empty', [])

    def test_who(self, sample_task_empty, sample_task_abc, sample_user_a, sample_user_b, sample_user_c):
        assert sample_task_empty.who() is None
        assert sample_task_abc.who() == sample_user_a.user_name
        assert sample_task_abc.who() == sample_user_b.user_name
        assert sample_task_abc.who() == sample_user_c.user_name
