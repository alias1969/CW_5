import psycopg2
import pytest

from tests.conftest import list_fk_for_areas, list_fk_for_vacancies, list_fk_for_employers


def test_db_create_init(db_create):
    """ Тест инициализации класса DBCreate и подключения в базе данных """
    # проверяем имя базы данных
    assert db_create.database_name == 'Vacancies'

    # проверяем свойство соединения
    assert db_create.conn.autocommit == True


def test_delete_table_vacancies(db_create, list_fk_for_vacancies):
    """ Проверить удаление таблицы vacancies"""
    try:
        db_create.delete_table('vacancies', list_fk_for_vacancies)
        assert True
    except psycopg2.errors.UndefinedObject:
        assert False


def test_delete_table_employers(db_create, list_fk_for_employers):
    """ Проверить удаление таблицы employers"""
    try:
        db_create.delete_table('employers', list_fk_for_employers)
        db_create.conn.commit()
        assert True
    except psycopg2.errors.UndefinedObject:
        assert False

def test_delete_table_areas(db_create, list_fk_for_areas):
    """ Проверить удаление таблицы areas"""
    try:
        db_create.delete_table('areas', list_fk_for_areas)
        db_create.conn.commit()
        assert True
    except psycopg2.errors.UndefinedObject:
        assert False


def test_create_table_employers(db_create):
    """ Тест создания таблицы employers - после выполнения функции выборка по таблице - ошибки быть не должно записей 0"""
    #db_create.create_table()
    #db_create.connect()
    try:
        db_create.cur.execute('select * from employers')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

    except psycopg2.DatabaseError as err:
        raise err


def test_create_table_vacancies(db_create):
    """ Тест создания таблицы vacancies - после выполнения функции выборка по таблице - ошибки быть не должно записей 0"""
    try:
        db_create.cur.execute('select * from vacancies')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

    except psycopg2.DatabaseError as err:
        raise err


def test_create_table_employments(db_create):
    """ Тест создания таблицы employments - после выполнения функции выборка по таблице - ошибки быть не должно записей 0"""
    try:
        db_create.cur.execute('select * from employments')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

        # проверяем таблицу experiences
        db_create.cur.execute('select * from experiences')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

        # проверяем таблицу schedules
        db_create.cur.execute('select * from schedules')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

        # проверяем таблицу areas
        db_create.cur.execute('select * from areas')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

    except psycopg2.DatabaseError as err:
        raise err

def test_create_table_experiences(db_create):
    """ Тест создания таблицы experiences - после выполнения функции выборка по таблице - ошибки быть не должно записей 0"""
    try:
        db_create.cur.execute('select * from experiences')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

    except psycopg2.DatabaseError as err:
        raise err

def test_create_table_schedules(db_create):
    """ Тест создания таблицы schedules - после выполнения функции выборка по таблице - ошибки быть не должно записей 0"""
    try:
        db_create.cur.execute('select * from schedules')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

        # проверяем таблицу areas
        db_create.cur.execute('select * from areas')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

    except psycopg2.DatabaseError as err:
        raise err

def test_create_table_areas(db_create):
    """ Тест создания таблицы areas - после выполнения функции выборка по таблице - ошибки быть не должно записей 0"""
    try:
        db_create.cur.execute('select * from areas')
        result = db_create.cur.fetchall()
        # В таблице нет данных
        assert len(result) == 0

    except psycopg2.DatabaseError as err:
        raise err


def test_insert_employers(db_create, data_for_insert_into_employers, related_data_code,
                          list_fk_for_vacancies, list_fk_for_employers, list_fk_for_areas):
    """ Тест функции вставки данных в таблицу employers """
    try:
        # удалим данные таблиц, чтобы не было дублей
        db_create.delete_table('vacancies', list_fk_for_vacancies)
        db_create.delete_table('employers', list_fk_for_employers)
        db_create.delete_table('areas')
        # вставим 1 строку
        db_create.insert_employers(data_for_insert_into_employers, related_data_code)

        # получим выборку - должна быть 1 строка
        db_create.connect()
        db_create.cur.execute('select * from employers')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) == 1

    except psycopg2.DatabaseError as err:
        assert False


def test_insert_insert_vacancies(db_create, data_for_insert_into_employers, data_for_insert_vacancies,
                                 related_data_code, list_fk_for_vacancies, list_fk_for_employers):
    """ Тест функции вставки данных в таблицу vacancies """
    try:
        # удалим данные таблиц, чтобы не было дублей
        db_create.delete_table('vacancies', list_fk_for_vacancies)
        db_create.delete_table('employers', list_fk_for_employers)
        db_create.delete_table('areas')
        # вставим 1 строку
        db_create.insert_employers(data_for_insert_into_employers, related_data_code)
        db_create.connect()
        db_create.insert_vacancies(data_for_insert_vacancies, related_data_code)

        # получим выборку - должна быть 1 строка
        db_create.connect()
        db_create.cur.execute('select * from vacancies')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) > 0

    except psycopg2.DatabaseError as err:
        raise err


def test_insert_schedules(db_create, related_data_code):
    """ Тест функции вставки данных в таблицу schedules """
    try:
        #список для записи в таблицу
        related_data = ['fullDay', 'Полный день']
        # вставим 1 строку
        db_create.insert_schedules(related_data_code['schedule'], '1', related_data)

        # получим выборку - должна быть 1 строка
        db_create.connect()
        db_create.cur.execute('select * from schedules')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) == 1

        # повторим вставку - ничего не должно добавиться
        db_create.insert_schedules(related_data_code['schedule'], '1', related_data)

        # выборка должна остаться без изменения
        db_create.cur.execute('select * from schedules')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) == 1

    except psycopg2.DatabaseError as err:
        raise err


def test_insert_areas(db_create, related_data_code):
    """ Тест функции вставки данных в таблицу areas """
    try:
        #список для записи в таблицу
        related_data = ['26', 'Воронеж', 'test_url']
        # вставим 1 строку
        db_create.insert_areas(related_data_code['area'], '1', related_data)

        # получим выборку - должна быть 1 строка
        db_create.connect()
        db_create.cur.execute('select * from areas')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) == 1

        # повторим вставку - ничего не должно добавиться
        db_create.insert_areas(related_data_code['area'], '1', related_data)

        # выборка должна остаться без изменения
        db_create.cur.execute('select * from areas')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) == 1

    except psycopg2.DatabaseError as err:
        raise err


def test_insert_employments(db_create, related_data_code):
    """ Тест функции вставки данных в таблицу employments """
    try:
        #список для записи в таблицу
        related_data = ['full', 'Полная занятость']
        # вставим 1 строку
        db_create.insert_employments(related_data_code['employment'], '1', related_data)

        # получим выборку - должна быть 1 строка
        db_create.connect()
        db_create.cur.execute('select * from employments')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) == 1

        # повторим вставку - ничего не должно добавиться
        db_create.insert_employments(related_data_code['employment'], '1', related_data)

        # выборка должна остаться без изменения
        db_create.cur.execute('select * from employments')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) == 1

    except psycopg2.DatabaseError as err:
        raise err


def test_insert_experiences(db_create, related_data_code):
    """ Тест функции вставки данных в таблицу experiences """
    try:
        #список для записи в таблицу
        related_data = ['NoExperience', 'Нет опыта']
        # вставим 1 строку
        db_create.insert_experiences(related_data_code['experience'], '1', related_data)

        # получим выборку - должна быть 1 строка
        db_create.connect()
        db_create.cur.execute('select * from experiences')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) == 1

        # повторим вставку - ничего не должно добавиться
        db_create.insert_experiences(related_data_code['experience'], '1', related_data)

        # выборка должна остаться без изменения
        db_create.cur.execute('select * from experiences')
        data = db_create.cur.fetchall()
        assert type(data) is list
        assert len(data) == 1

    except psycopg2.DatabaseError as err:
        raise err


