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

    @pytest.fixture(scope='module')
    def sample_user_d(self):
        return UserData('d')

    @pytest.fixture(scope='module')
    def sample_task_abc(self, sample_user_a, sample_user_b, sample_user_c):
        return TaskData(123, 'sample_task_abc', [sample_user_a, sample_user_b, sample_user_c])

    @pytest.fixture()
    def sample_task_empty(self):
        return TaskData(321, 'sample_task_empty', [])

    def test_add_participant(self, sample_task_empty, sample_user_d):
        assert len(sample_task_empty.participants) == 0
        sample_task_empty.add_participant(sample_user_d.user_name)
        assert len(sample_task_empty.participants) == 1
        assert sample_task_empty.participants[0].user_name == sample_user_d.user_name

    def test_check_participant_exists_by_name(self, sample_task_empty, sample_task_abc, sample_user_a, sample_user_b,
                                              sample_user_c, sample_user_d):
        assert sample_task_empty.check_participant_exists_by_name(sample_user_a.user_name) is False
        assert sample_task_abc.check_participant_exists_by_name(sample_user_a.user_name) is True
        assert sample_task_abc.check_participant_exists_by_name(sample_user_b.user_name) is True
        assert sample_task_abc.check_participant_exists_by_name(sample_user_c.user_name) is True
        assert sample_task_abc.check_participant_exists_by_name(sample_user_d.user_name) is False

    def test_who(self, sample_task_empty, sample_task_abc, sample_user_a, sample_user_b, sample_user_c):
        assert sample_task_empty.who() is None
        assert sample_task_abc.who() == sample_user_a.user_name
        assert sample_task_abc.who() == sample_user_b.user_name
        assert sample_task_abc.who() == sample_user_c.user_name
