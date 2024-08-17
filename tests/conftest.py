import pytest

from src.vacancy import Vacancy
from src.employer import Employer
from src.api_hh import APIHeadHunter
from config import PARAMS, DATABASE_NAME
from src.db_manager import DBManager
from src.db_create import DBCreate
from src.utils import delete_create_database, insert_data, create_database


def get_data_for_insert_employers():
    """ Список словаря для записи в таблицу emplouer"""
    return [{'id': '4307', 'name': 'Московская Биржа', 'description': 'Очень крутая компания',
                                  'alternate_url': 'https://hh.ru/employer/1057',
                                  'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=1057',
                                  'area': {'id': '26', 'name': 'Воронеж', 'url': 'https://api.hh.ru/areas/26'}}]


def get_data_for_insert_vacancies():
    """ Список словаря для записи в таблицу vacacies"""
    return [{'id': '105537264',
                                  'name': 'Оператор call-центра',
                                  'area': {'id': '26', 'name': 'Воронеж', 'url': 'https://api.hh.ru/areas/26'},
                                  'salary': {'from': 50000, 'to': None, 'currency': 'RUR', 'gross': True},
                                  'alternate_url': 'https://hh.ru/vacancy/105537264',
                                  'employer': {'id': '4307', 'name': 'Московская Биржа',
                                               'url': 'https://api.hh.ru/employers/4307',
                                               'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=4307'},
                                  'snippet': {
                                      'requirement': 'Готовы к удаленной работе — это ответственно, но еще и удобно. Умеете и уже работали с большими объёмами информации. ',
                                      'responsibility': 'Звонить клиентам Финуслуг по телефону (не холодная база, клиенты о нас уже знают). Презентовать им продукты и услуги, которые мы...'},
                                  'schedule': {'id': 'remote', 'name': 'Удаленная работа'},
                                  'experience': {'id': 'noExperience', 'name': 'Нет опыта'},
                                  'employment': {'id': 'full', 'name': 'Полная занятость'},
                                  },
                                 {'id': '105537269',
                                  'name': 'Менеджер по продажам',
                                  'area': {'id': '26', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/26'},
                                  'salary': {'from': 70000, 'to': 80000, 'currency': 'RUR', 'gross': True},
                                  'alternate_url': 'https://hh.ru/vacancy/105537264',
                                  'employer': {'id': '4307', 'name': 'Московская Биржа',
                                               'url': 'https://api.hh.ru/employers/4307',
                                               'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=4307'},
                                  'snippet': {
                                      'requirement': 'Готовы к удаленной работе — это ответственно, но еще и удобно. Умеете и уже работали с большими объёмами информации. ',
                                      'responsibility': 'Звонить клиентам Финуслуг по телефону (не холодная база, клиенты о нас уже знают). Презентовать им продукты и услуги, которые мы...'},
                                  'schedule': {'id': 'remote', 'name': 'Удаленная работа'},
                                  'experience': {'id': 'noExperience', 'name': 'Нет опыта'},
                                  'employment': {'id': 'full', 'name': 'Полная занятость'},
                                  }
                                 ]


@pytest.fixture
def vacancy():
    """ Фикстура для работы с классом Vacancy """
    return Vacancy("1234",
                   "Менеджер по работе с клиентами",
                   "Марс", 40000, 70000, 'RUR',
                   "Воронеж",
                   "https://hh.ru/vacancy/101709979",
                   "Полная занятость", "От 1 года до 3 лет",
                   "Полный день", "Опыт работы в продажах обязателен",
                   "Консультирование клиентов")


@pytest.fixture
def list_for_vacancy():
    """ Фикстура для списка кортежей, из которых будет создан класс Vacancy """
    return [
        ('1234', 'Менеджер по работе с клиентами', 'Марс', 40000, 70000, 'RUR',
            'Воронеж', 'https://hh.ru/vacancy/101709979', 'Полная занятость', 'От 1 года до 3 лет',
            'Полный день', 'Опыт работы в продажах обязателен', 'Консультирование клиентов') ,
            ('1235', 'Оператор call-центра', 'Марс', 30000, 40000, 'RUR',
             'Москва', 'https://hh.ru/vacancy/101709980', 'Удаленка', 'Без опыта',
             'Полный день', 'Без опыта', 'Консультирование клиентов')
            ]


@pytest.fixture
def employer():
    """ Фикстура для работы с классом Employer """
    return Employer("1234",
                   "Марс",
                   "Воронеж", "Очень крутая компания",
                    "https://hh.ru/mars", "https://hh.ru//mars/vacancy",
                   12)


@pytest.fixture
def api_hh():
    """ Фикстура для работы с классом APIHeadHunter """
    api_hh_ = APIHeadHunter(f"https://api.hh.ru/vacancies?employer_id=4307")
    return api_hh_.get_data()


@pytest.fixture
def list_fk_for_vacancies():
    """ Фикстура зависимостей таблиц для vacancies"""
    return {'vacancies' : ['fk_vacancies_area', 'fk_vacancies_schedule', 'fk_vacancies_employment',
            'fk_vacancies_experience']}#, 'fk_vacancies_employer']}


@pytest.fixture
def list_fk_for_employers():
    """ Фикстура зависимостей таблиц для employers"""
    return {'employers' : ['fk_employers_area'],'vacancies' : ['fk_vacancies_employer']}


@pytest.fixture
def list_fk_for_areas():
    """ Фикстура зависимостей таблиц для areas"""
    return {'employers' : ['fk_employers_area'], 'vacancies' : ['fk_vacancies_area']}


@pytest.fixture
def data_for_insert_vacancies():
    """ Список словарей для заполнения таблицы вакансий"""
    return get_data_for_insert_vacancies()
    return [{'id': '105537264',
            'name': 'Оператор call-центра',
            'area': {'id': '26', 'name': 'Воронеж', 'url': 'https://api.hh.ru/areas/26'},
            'salary': {'from': 50000, 'to': None, 'currency': 'RUR', 'gross': True},
            'alternate_url': 'https://hh.ru/vacancy/105537264',
            'employer': {'id': '4307', 'name': 'Московская Биржа', 'url': 'https://api.hh.ru/employers/4307', 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=4307'},
            'snippet': {'requirement': 'Готовы к удаленной работе — это ответственно, но еще и удобно. Умеете и уже работали с большими объёмами информации. ',
                        'responsibility': 'Звонить клиентам Финуслуг по телефону (не холодная база, клиенты о нас уже знают). Презентовать им продукты и услуги, которые мы...'},
            'schedule': {'id': 'remote', 'name': 'Удаленная работа'}, 'experience': {'id': 'noExperience', 'name': 'Нет опыта'},
            'employment': {'id': 'full', 'name': 'Полная занятость'},
            },
            {'id': '105537269',
             'name': 'Менеджер по продажам',
             'area': {'id': '26', 'name': 'Воронеж', 'url': 'https://api.hh.ru/areas/26'},
             'salary': {'from': 70000, 'to': 80000, 'currency': 'RUR', 'gross': True},
             'alternate_url': 'https://hh.ru/vacancy/105537264',
             'employer': {'id': '4307', 'name': 'Московская Биржа', 'url': 'https://api.hh.ru/employers/4307',
                          'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=4307'},
             'snippet': {
                 'requirement': 'Готовы к удаленной работе — это ответственно, но еще и удобно. Умеете и уже работали с большими объёмами информации. ',
                 'responsibility': 'Звонить клиентам Финуслуг по телефону (не холодная база, клиенты о нас уже знают). Презентовать им продукты и услуги, которые мы...'},
             'schedule': {'id': 'remote', 'name': 'Удаленная работа'},
             'experience': {'id': 'noExperience', 'name': 'Нет опыта'},
             'employment': {'id': 'full', 'name': 'Полная занятость'},
             }
            ]


@pytest.fixture
def data_for_insert_into_employers():
    """ Список словарей для заполнения таблицы вакансий"""
    return get_data_for_insert_employers()
    return [{'id': '4307',  'name': 'Московская Биржа', 'description': 'Очень крутая компания',
            'alternate_url': 'https://hh.ru/employer/1057', 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=1057',
            'area': {'id': '26', 'name': 'Воронеж', 'url': 'https://api.hh.ru/areas/26'}}]


@pytest.fixture
def related_data_code():
    """ Словарь списка кодов вспомогательных таблиц"""
    return {'area':[],
            'employment': [],
            'experience': [],
            'schedule': [],
            }


@pytest.fixture
def db_create():
    """ Фикстура для работы с классом DBCreate"""
    # удалим базу данных
    delete_create_database(DATABASE_NAME, PARAMS)
    db_create_ = DBCreate(DATABASE_NAME, PARAMS)
    db_create_.create_table()
    db_create_.connect()
    # получаем экземпляр класса уже созданной БД
    return db_create_


@pytest.fixture
def db_manager():
    """ Фикстура для работы с классом DBManager"""

    # Для тестирования выборки, нужно создать и наполнить базу данных
    create_database()
    data_for_insert_employers = get_data_for_insert_employers()

    data_for_insert_vacancies = get_data_for_insert_vacancies()

    insert_data(data_for_insert_employers, data_for_insert_vacancies)

    return DBManager(DATABASE_NAME, PARAMS)