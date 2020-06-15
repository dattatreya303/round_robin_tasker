class UserData(object):
    def __init__(self, user_name):
        self.__user_name = user_name

    @property
    def user_name(self):
        return self.__user_name

    def __eq__(self, other):
        if self.__user_name == other.__user_name:
            return True
        return False
