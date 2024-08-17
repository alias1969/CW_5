import psycopg2

from .api_hh import APIHeadHunter
from .db_manager import DBManager
from .db_create import DBCreate
from .vacancy import Vacancy
from .employer import Employer

from config import EMPLOYERS_LIST_ID, PARAMS, DATABASE_NAME

def delete_create_database(database_name, params):
    """ Удалить базу данных и создать ее заново"""
    try:
        # закроем все соединения с базой данных
        conn = psycopg2.connect(database=database_name, **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"""SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = '{database_name}'
                    AND pid <> pg_backend_pid()""")

        conn.close()

        # удалим базу данных и создадим заново
        conn = psycopg2.connect(database=database_name, **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
        # создаем новую бд
        cur.execute(f'CREATE DATABASE {database_name}')

    except psycopg2.errors.ConnectionDoesNotExist as err:
        raise f'Не найдена база данных {database_name}: {err}'

    except psycopg2.errors.UndefinedTable as err:
        print(err.pgcode)
        raise f'Ошибка соединения с базой данных {database_name}: {err}'

    finally:
        conn.close()

    # удалим таблицы, так как у меня они остаются, несмотря ни на что
    try:
        conn = psycopg2.connect(database=database_name, **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute('DROP TABLE vacancies')
        cur.execute('DROP TABLE employers')
        cur.execute('DROP TABLE experiences')
        cur.execute('DROP TABLE areas')
        cur.execute('DROP TABLE employments')
        cur.execute('DROP TABLE schedules')

    except psycopg2.errors.UndefinedTable:
        pass


def create_database():
    """ Создание базы данных и ее таблиц"""

    # удаление/создание базы данных
    delete_create_database(DATABASE_NAME, PARAMS)

    # класс для создания таблиц базы данных
    db_create = DBCreate(DATABASE_NAME, PARAMS)
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
        print(keyword)
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


