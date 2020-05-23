from UserData import UserData


class TaskData(object):
    def __init__(self, task_id, task_name=None, task_participants: list = []):
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
            if participant.user_name == user_name:
                return True
        return False

    def add_participant(self, participant: UserData):
        self.__participants.add(participant)

    def remove_participant(self, participant: UserData):
        self.__participants.remove(participant)

    def who(self):
        who = self.__tracker
        self.__tracker = (self.__tracker + 1) % len(self.__participants)
        return self.__participants[who]


