from typing import List

from UserData import UserData


class TaskData(object):
    def __init__(self, task_id: int, task_name: str = None, task_participants: List[UserData] = []):
        self.__id = task_id
        self.__name = task_name
        self.__participants = task_participants
        self.__tracker = 0

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def participants(self):
        return self.__participants

    def check_participant_exists_by_name(self, user_name: str):
        for participant in self.__participants:
            if participant.user_name.lower() == user_name.lower():
                return True
        return False

    def add_participant(self, participant: str) -> bool:
        if not self.check_participant_exists_by_name(participant):
            self.__participants.append(UserData(participant))
            return True
        return False

    def add_participant_list(self, participant_list: List[str]) -> bool:
        to_add = []
        for participant in participant_list:
            if self.check_participant_exists_by_name(participant):
                return False
            to_add.append(UserData(participant))
        self.__participants.extend(to_add)
        return True

    def remove_participant(self, participant: str) -> bool:
        if self.check_participant_exists_by_name(participant):
            self.__participants.remove(UserData(participant))
            return True
        return False

    def who(self):
        if len(self.__participants) == 0:
            return None
        who = self.__tracker
        self.__tracker = (self.__tracker + 1) % len(self.__participants)
        return self.__participants[who].user_name


