from src.db_create import DBCreate
from src.utils import insert_data
from config import PARAMS, DATABASE_NAME
from src.db_manager import DBManager

def test_init_(db_manager, data_for_insert_into_employers, data_for_insert_vacancies):
    """  Тест инициации класса DBManager"""
    assert db_manager.database_name == 'Vacancies'
    assert db_manager.text_vacancies == """
        SELECT vacancies.id, vacancies.name as vacancy, employers.name as company, vacancies.salary_from, vacancies.salary_to, vacancies.currency,
        areas.name as area, vacancies.url, employments.name as employment, experiences.name as experience, schedules.name as schedule,
        requirement, responsibility
        FROM vacancies
        LEFT JOIN employers on vacancies.employer_id = employers.id
        LEFT JOIN schedules on vacancies.schedule_id = schedules.id
        LEFT JOIN employments on vacancies.employment_id = employments.id
        LEFT JOIN experiences on vacancies.experience_id = experiences.id
        LEFT JOIN areas on vacancies.area_id = areas.id
        """

def test_get_companies_and_vacancies_count(db_manager):
    """ Проверить выборку данных работодателей"""
    result_request = db_manager.get_companies_and_vacancies_count()
    assert type(result_request) is list
    assert len(result_request) > 0
    assert type(result_request[0]) is tuple

def test_get_all_vacancies(db_manager):
    """ Проверить выборку данных по всем вакансиям"""
    result_request = db_manager.get_all_vacancies()
    assert type(result_request) is list
    assert len(result_request) > 0
    assert type(result_request[0]) is tuple

def test_get_vacancies_with_keyword(db_manager):
    """ Проверить выборку данных по вакансиям с отбором по ключевому слову"""
    result_request = db_manager.get_vacancies_with_keyword('енеджер')
    assert type(result_request) is list
    assert len(result_request) > 0
    assert type(result_request[0]) is tuple


def test_get_vacancies_with_area(db_manager):
    """ Проверить выборку данных вакансиям с отбором по региону """
    result_request = db_manager.get_vacancies_with_area('Воронеж')
    assert type(result_request) is list
    assert len(result_request) > 0
    assert type(result_request[0]) is tuple

def test_get_count_vacancies(db_manager):
    """ Проверить выборку данных: количество вакансий"""
    result_request = db_manager.get_count_vacancies()
    assert type(result_request) is list
    assert len(result_request) > 0
    assert type(result_request[0]) is tuple

def test_get_vacancies_with_higher_salary(db_manager):
    """ Проверить выборку данных: вакансии, у которых зарплата выше среднего """
    result_request = db_manager.get_vacancies_with_higher_salary()
    assert type(result_request) is list
    assert len(result_request) > 0
    assert type(result_request[0]) is tuple


def test_get_avg_salary(db_manager):
    """ Проверить выборку данных: среднюю зарплату """
    result_request = db_manager.get_avg_salary()
    assert type(result_request) is list
    assert len(result_request) > 0
    assert type(result_request[0]) is tuple


def test_get_top_salaries(db_manager):
    """ Проверить выборку данных: 10 вакансий с наивысшими зарплатами """
    result_request = db_manager.get_top_salaries()
    assert type(result_request) is list
    assert len(result_request) > 1
    assert type(result_request[0]) is tuple

def create_database():
    """ Для тестирования выборки, нужно создать и наполнить базу данных"""
    data_for_insert_employers = [{'id': '4307', 'name': 'Московская Биржа', 'description': 'Очень крутая компания',
            'alternate_url': 'https://hh.ru/employer/1057', 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=1057',
            'area': {'id': '26', 'name': 'Воронеж', 'url': 'https://api.hh.ru/areas/26'}}]
    data_for_insert_vacancies = [{'id': '105537264',
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
             'area': {'id': '26', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/26'},
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

    db_create = DBCreate(DATABASE_NAME, PARAMS)
    db_create.create_database()
    db_create.create_table()
    insert_data(data_for_insert_employers, data_for_insert_vacancies)

create_database()
db_manager = DBManager(DATABASE_NAME, PARAMS)