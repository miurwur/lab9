class UserCurrency():
    def __init__(self, id: str, user_id: int):
        self.__id: str = id;
        self.__user_id: int = user_id;

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        if type(id) is str:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании id')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        if type(user_id) is int:
            self.__user_id = user_id
        else:
            raise ValueError('Ошибка при задании user_id')

    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join(v.__repr__() for _,v in vars(self).items())
        )