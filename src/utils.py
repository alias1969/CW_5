from .api_hh import APIHeadHunter
from .db_manager import DBManager
from .db_create import DBCreate
from .vacancy import Vacancy
from .employer import Employer

from config import EMPLOYERS_LIST_ID, PARAMS, DATABASE_NAME


def create_database():
    """ Создание базы данных и ее таблиц"""
    db_create = DBCreate(DATABASE_NAME, PARAMS)
    ## создание базы данных
    db_create.create_database()
    # создание таблиц базы
    db_create.create_table()

def get_employee_from_website() -> list:
    """ Получить данные о компаниях с сайта HH.ru """
    employers = []
    for employer_id in EMPLOYERS_LIST_ID:
        url_employer = f"https://api.hh.ru/employers/{employer_id}"
        hh_api = APIHeadHunter(url_employer)

        employers_data = hh_api.get_data()
        employers.append(employers_data)

    return employers


def get_vacancies_from_website() -> list:
    """ Получить данные о вакансиях компаний с сайта HH.ru """
    vacancies = []
    for employer_id in EMPLOYERS_LIST_ID:
        # ссылка на вакансии компании
        url_employer = f"https://api.hh.ru/vacancies?employer_id={employer_id}"

        hh_api = APIHeadHunter(url_employer)
        # получим данные с сайта
        vacancies_data = hh_api.get_data()

        vacancies.extend(vacancies_data['items'])

    return vacancies


def insert_data(data_employers: list[dict], data_vacancies: list[dict]):
    """ Общая функция записи данных в БД"""
    # создадим словарь списков кодов вспомогательных таблиц, чтобы знать, какие данные уже добавлены
    related_data = {'area':[],
                    'employment': [],
                    'experience': [],
                    'schedule': [],
                    }
    insert_into_database_employers(data_employers, related_data)
    insert_into_database_vacancies(data_vacancies, related_data)


def insert_into_database_employers(data, related_data: dict):
    """Записать данные о компаниях"""
    db_create = DBCreate(DATABASE_NAME, PARAMS)
    db_create.insert_employers(data, related_data)


def insert_into_database_vacancies(data, related_data: dict):
    """ Записать данные о вакансиях  """
    db_create = DBCreate(DATABASE_NAME, PARAMS)
    db_create.insert_vacancies(data, related_data)


def get_list_vacancy(result_request:list)->list:
    """ Получить из результата запроса список элементов класса Vacancy"""
    vacancies = []
    for item in result_request:
        vacancies.append(Vacancy.new_vacancy(item))

    return vacancies


def execute_request(mode, keyword:str = ''):
    """ Выбрать данные из базы данных в соответствии с выбранным режимом"""

    # для выборки данных используем класс DBManager
    db_manager = DBManager(DATABASE_NAME, PARAMS)

    # вывод компаний и число их вакансий
    if mode == '1':
        result_request = db_manager.get_companies_and_vacancies_count()
        employers = []
        for item in result_request:
            employers.append(Employer.new_employer(item))
        return employers

    # вывод количества всех вакансий
    elif mode == '2':
        result_request = db_manager.get_count_vacancies()[0][0]
        return [result_request]

    # вывод всех вакансий
    elif mode == '3':
        result_request = db_manager.get_all_vacancies()
        return get_list_vacancy(result_request)

    # вывод вакансий по ключевым словам
    elif mode == '4':
        result_request = db_manager.get_vacancies_with_keyword(keyword)
        return get_list_vacancy(result_request)

    # вывод вакансий, у которых зарплата выше среднего
    elif mode == '5':
        result_request = db_manager.get_vacancies_with_higher_salary()
        return get_list_vacancy(result_request)

    # вывод средней зарплаты в вакансиях
    elif mode == '6':
        result_request = db_manager.get_avg_salary()[0][0]
        return [result_request]

    # вывод ТОП-10 вакансий с самой высокой зарплатой
    elif mode == '7':
        result_request = db_manager.get_top_salaries()
        return get_list_vacancy(result_request)

    # вывод компаний по регионам
    elif mode == '8':
        result_request = db_manager.get_vacancies_with_area(keyword)
        return get_list_vacancy(result_request)


