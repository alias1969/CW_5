import pytest
import psycopg2


from src.utils import (get_employee_from_website, get_vacancies_from_website, insert_data,
                       insert_into_database_employers, insert_into_database_vacancies,
                       get_list_vacancy, execute_request)
from src.vacancy import Vacancy
from src.employer import Employer
from tests.conftest import related_data_code


def test_create_database(db_create):
    """ Тест создания базы данных: попытаемся сделать выборку - должна быть ошибка"""
    db_create.connect()
    with pytest.raises(psycopg2.errors.UndefinedTable) as ra:
        db_create.cur.execute('select * from employers')


def test_get_employee_from_website():
    """ Проверить получение данных о компаниях с сайта HH.ru """
    employers = get_employee_from_website()
    assert type(employers) is list
    assert len(employers) > 0
    assert type(employers[0]) is dict


def test_get_vacancies_from_website():
    """ Проверить получение данных о вакансиях с сайта HH.ru """
    vacancies = get_vacancies_from_website()
    assert type(vacancies) is list
    assert len(vacancies) > 0
    assert type(vacancies[0]) is dict


def test_insert_into_database_employers(db_create, db_manager, data_for_insert_into_employers, related_data_code):
    """ Проверить запись данных в таблицу employers"""
    # создание таблиц базы
    db_create.create_table()

    # запись в таблицу employers
    insert_into_database_employers(data_for_insert_into_employers, related_data_code)
    # проверим выборкой данных, что данные есть в таблицах
    try:
        # выборка компаний
        db_manager.cur.execute('select * from employers LIMIT 1')
        data = db_manager.cur.fetchall()
        assert type(data) is list
        assert len(data) > 0

    except psycopg2.DatabaseError as err:
        raise err

def test_insert_into_database_vacancies(db_create, db_manager, data_for_insert_vacancies, related_data_code):
    """ Проверить запись данных в таблицу vacancies"""
    # создание таблиц базы
    db_create.create_table()
    # запись в таблицу vacancies
    insert_into_database_vacancies(data_for_insert_vacancies, related_data_code)
# проверим выборкой данных, что данные есть в таблицах
    try:
        # выборка вакансий
        db_manager.cur.execute('select * from vacancies LIMIT 1')
        data = db_manager.cur.fetchall()
        assert type(data) is list
        assert len(data) > 0

    except psycopg2.DatabaseError as err:
        raise err

def test_insert_data(db_create, db_manager, data_for_insert_into_employers, data_for_insert_vacancies):
    """ Проверить запись данных в БД """
    # создание таблиц базы
    db_create.create_table()
    # запись в таблицы
    insert_data(data_for_insert_into_employers, data_for_insert_vacancies)

    # проверим выборкой данных, что данные есть в таблицах
    try:
        # выборка компаний
        db_manager.cur.execute('select * from employers LIMIT 1')
        data = db_manager.cur.fetchall()
        assert type(data) is list
        assert len(data) > 0

        # выборка вакансий
        db_manager.cur.execute('select * from vacancies LIMIT 1')
        data = db_manager.cur.fetchall()
        assert type(data) is list
        assert len(data) > 0

    except psycopg2.DatabaseError as err:
        raise err


def test_get_list_vacancy(list_for_vacancy, vacancy):
    """ Проверить получение списка элементов класса Vacancy"""
    vacancies = get_list_vacancy(list_for_vacancy)
    # результат - список и он не пустой
    assert type(vacancies) is list
    assert len(vacancies) > 0
    # элементы списка - экземпляры класса Vacancy
    assert  isinstance(vacancies[0], Vacancy)


def test_execute_request_employer(db_create, data_for_insert_into_employers, data_for_insert_vacancies):
    """ Проверить результатов запросов: вывод компаний и число их вакансий """
    # создание таблиц базы
    db_create.create_table()
    # запись в таблицы
    insert_data(data_for_insert_into_employers, data_for_insert_vacancies)
    # 1 - вывод компаний и число их вакансий
    employers = execute_request('1')
    assert type(employers) is list
    assert len(employers) > 0
    # элементы списка - экземпляры класса Vacancy
    assert isinstance(employers[0], Employer)


def test_execute_request_count_vacancies(db_create, data_for_insert_into_employers, data_for_insert_vacancies):
    """ Проверить результатов запросов: количество вакансий """
    # создание таблиц базы
    db_create.create_table()
    # запись в таблицы
    insert_data(data_for_insert_into_employers, data_for_insert_vacancies)
    # 2 - вывод количества вакансий
    result = execute_request('2')
    assert type(result) is list
    assert len(result) == 1
    # элемент списка - кортеж(целое)
    assert type(result[0]) is int


def test_execute_request_vacancies(db_create, data_for_insert_into_employers, data_for_insert_vacancies):
    """ Проверить результатов запросов: всех вакансий """
    # создание таблиц базы
    db_create.create_table()
    # запись в таблицы
    insert_data(data_for_insert_into_employers, data_for_insert_vacancies)
    # 3 - вывод всех вакансий
    vacancies = execute_request('3')
    assert type(vacancies) is list
    assert len(vacancies) > 0
    # элементы списка - экземпляры класса Vacancy
    assert isinstance(vacancies[0], Vacancy)


def test_execute_request_vacancies_with_higher_salary(db_create, data_for_insert_into_employers, data_for_insert_vacancies):
    """ Проверить результатов запросов: вакансий с зарплатой выше среднего"""
    # создание таблиц базы
    db_create.create_table()
    # запись в таблицы
    insert_data(data_for_insert_into_employers, data_for_insert_vacancies)
    # 3 - вывод всех вакансий
    vacancies = execute_request('5')
    assert type(vacancies) is list
    assert len(vacancies) > 0
    # элементы списка - экземпляры класса Vacancy
    assert isinstance(vacancies[0], Vacancy)





