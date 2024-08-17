import psycopg2

class DBCreate:
    """ Класс для работы с данными в БД:
    - подключение к БД
    - создание таблиц
    - добавление данных
    - обновление данных
"""
    database_name: str
    params: dict


    def __init__(self, database_name, params):
        """ Инициация класса, где определяем - подключение, курсор, структуру БД, текст основного запроса"""
        self.__structure_database = {}
        self.conn = None
        self.cur = None
        self.database_name = database_name
        self.params = params
        self.connect()


    @property
    def structure_database(self):
        """ Структура таблиц базы данных: имя и поля таблицы в виде словаря"""
        return {
            'employers': 'id varchar(15)  NOT NULL, name varchar(300), description varchar, area_id varchar(15), url text, vacancies_url text',
            'areas': 'id varchar(15) NOT NULL, name varchar(50), url varchar',
            'schedules': 'id varchar(25) NOT NULL, name varchar(100)',
            'experiences': 'id varchar(50) NOT NULL, name varchar(100)',
            'employments': 'id varchar(25) NOT NULL, name varchar(100)',
            'vacancies': 'id serial PRIMARY KEY, name varchar(150) NOT NULL, employer_id varchar(15), '
                         'salary_from integer, salary_to integer, currency char(3), '
                         'area_id varchar(15), url text, employment_id varchar(25), experience_id varchar(50), schedule_id varchar(25), '
                         'requirement text, responsibility text'
        }


    def connect(self):
        """ Подключиться к БД"""
        try:
            self.conn = psycopg2.connect(host=self.params['host'],database=self.database_name,user=self.params['user'],password=self.params['password'])
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as err:
            raise f'Ошибка соединения с базой данных {self.params['database']}: {err}'


    def create_database(self):
        """ Создать базу данных"""
        try:
            # удаляем бд, если она уже есть
            self.cur.execute(f'DROP DATABASE IF EXISTS {self.database_name}')
            self.conn.commit()
            # создаем новую бд
            self.cur.execute(f'CREATE DATABASE {self.database_name}')

        except BaseException as err:
            print('Ошибка создания базы данных')
            raise err

        # delete all table, because my tables aren't deleted - sd didn't replay me about it
        try:
            self.cur.execute(f'DROP TABLE vacancies')
            self.cur.execute(f'DROP TABLE employments')
            self.cur.execute(f'DROP TABLE experiences')
            self.cur.execute(f'DROP TABLE schedules')
            self.cur.execute(f'DROP TABLE areas')
            self.cur.execute(f'DROP TABLE employers')
        except psycopg2.DatabaseError as err:
            pass

        self.cur.close()
        self.conn.close()


    def create_table(self):
        """ Создать таблицы из структуры (атрибут structure_database)"""
        # подключаемся к БД
        self.connect()

        # получим структуру таблиц из атрибута __structure_database
        self.__structure_database = self.structure_database

        for name_table,fields in self.__structure_database.items():
            self.cur.execute(f'CREATE TABLE {name_table} ({fields})')

        self.conn.commit()
        self.conn.close()


    def insert_employers(self, data: dict, related_data: dict):
        """ Записать работодателей в таблицу"""
        try:
            for item in data:
                self.cur.execute(
                    """
                        INSERT INTO employers (id, name, description, url, vacancies_url, area_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (item['id'], item['name'], item['description'], item['alternate_url'], item['vacancies_url'], item['area']['id'])
                )

                # запишем данные по area, если такой записи еще не делали
                self.insert_areas(related_data['area'], item['area']['id'], [item['area']['id'], item['area']['name'], item['area']['url']])

        except BaseException as err:
            print('Ошибка записи данных работодателей в базу данных')
            raise err

        finally:
            self.conn.commit()
            self.conn.close()


    def insert_vacancies(self, data: dict, related_data: dict):
        """ Записать вакансии в таблицу"""
        try:
            for item in data:
                # print(item)

                # проверим заполнен ли тэг по зарплате from
                if item['salary'] is None or item['salary']['from'] is None:
                    salary_from = 0
                else:
                    salary_from = int(item['salary']['from'])

                # проверим заполнен ли тэг по зарплате to
                if item['salary'] is None or item['salary']['to'] is None:
                    salary_to = 0
                else:
                    salary_to = int(item['salary']['to'])

                # проверим заполнен ли тэг по зарплате валюта
                if item['salary'] is None or item['salary']['currency'] is None:
                    currency = 'RUR'
                else:
                    currency = item['salary']['currency']

                self.cur.execute(
                    """
                    INSERT INTO vacancies (id, name, employer_id, 
                    salary_from, salary_to, currency, 
                    area_id, url, employment_id, experience_id, schedule_id, requirement, responsibility)    
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (item['id'], item['name'], item['employer']['id'],
                    salary_from, salary_to, currency,
                    item['area']['id'], item['alternate_url'],
                    item['employment']['id'], item['experience']['id'], item['schedule']['id'],
                     item['snippet']['requirement'], item['snippet']['responsibility'])
                    )

                # запишем данные по area, если такой записи еще не делали
                self.insert_areas(related_data['area'], item['area']['id'],
                                  [item['area']['id'], item['area']['name'], item['area']['url']])

                # запишем данные по employment, если такой записи еще не делали
                self.insert_employments(related_data['employment'], item['employment']['id'],
                                  [item['employment']['id'], item['employment']['name']])

                # запишем данные по experience, если такой записи еще не делали
                self.insert_experiences(related_data['experience'], item['experience']['id'],
                                  [item['experience']['id'], item['experience']['name']])

                # запишем данные по schedule, если такой записи еще не делали
                self.insert_schedules(related_data['schedule'], item['schedule']['id'],
                                  [item['schedule']['id'], item['schedule']['name']])

        except BaseException as err:
            print('Ошибка записи вакансий в базу данных')
            raise err
        finally:
            self.conn.commit()
            self.conn.close()


    def insert_areas(self, list_codes: list, key: str, items: list):
        """ Добавить данные в таблицу локаций, если данных еще нет
        в list_codes список id, которые уже добавлены"""
        if key not in list_codes:
            self.cur.execute('INSERT INTO areas (id, name, url) VALUES (%s, %s, %s)', (items[0], items[1], items[2]))
            list_codes.append(key)


    def insert_schedules(self, list_codes: list, key: str, items: list):
        """ Добавить данные в таблицу расписание, если данных еще нет
        в list_codes список id, которые уже добавлены"""
        if key not in list_codes:
            self.cur.execute('INSERT INTO schedules (id, name) VALUES (%s, %s)', (items[0], items[1]))
            list_codes.append(key)


    def insert_experiences(self, list_codes: list, key: str, items: list):
        """ Добавить данные в таблицу опыт работы, если данных еще нет
        в list_codes список id, которые уже добавлены"""
        if key not in list_codes:
            self.cur.execute('INSERT INTO experiences (id, name) VALUES (%s, %s)', (items[0], items[1]))
            list_codes.append(key)


    def insert_employments(self, list_codes: list, key: str, items: list):
        """  Добавить данные в таблицу графика работы, если данных еще нет
        в list_codes список id, которые уже добавлены"""
        if key not in list_codes:
            self.cur.execute('INSERT INTO employments (id, name) VALUES (%s, %s)', (items[0], items[1]))
            list_codes.append(key)

