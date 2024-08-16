from abc import ABC, abstractmethod


class APIGetData(ABC):
    """Класс для работы с json"""

    @abstractmethod
    def get_response(self):
        """ Отправить запрос на сайт"""
        pass

    @abstractmethod
    def get_data(self):
        """ Получить данные """
        pass
