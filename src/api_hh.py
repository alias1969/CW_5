import requests
from requests import Response

from src.api import APIGetData
from config import PER_PAGES, ONLY_WITH_SALARY


class APIHeadHunter(APIGetData):
    """ Класс для API c hh.ru """

    def __init__(self, url) -> object:
        """ Инициация класса - ввод параметров подключения к сайту вакансий hh.ru"""
        self.url = url
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {'page': 0, 'per_page': PER_PAGES, "only_with_salary": ONLY_WITH_SALARY}


    def get_response(self) -> Response:
        """ Отправить запрос на сайт """
        self.url = self.url

        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise f'Не удалось прочитать данные с сайта: код ошибки {response.status_code}'

        return response


    def get_data(self):
        """ Получить данные по вакансиям с сайта """
        try:
            return self.get_response().json()
        except:
            raise 'Не удалось обработать данные с сайта'

