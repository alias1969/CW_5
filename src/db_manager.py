from .db_create import DBCreate


class DBManager(DBCreate):
    """ Класс для работы с данными в БД: выборка данных"""
    database_name: str
    text_vacancies: str


    def __init__(self, database_name, params):
        """ Инициация класса, где определяем - подключение, курсор, структуру БД, текст основного запроса"""
        super().__init__(database_name, params)
        #Текст основного запроса по вакансиям
        self.text_vacancies = """
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


    def get_companies_and_vacancies_count(self):
        """ Получить работодателей"""
        self.cur.execute("""
        SELECT employers.id, employers.name, areas.name as area, description, employers.url, vacancies_url, count(vacancies.id) as count_vacancies FROM employers
        JOIN areas ON employers.area_id = areas.id
        JOIN vacancies ON employers.id = vacancies.employer_id
        GROUP BY employers.id, employers.name, areas.name, description, employers.url, vacancies_url
        ORDER BY count_vacancies DESC
        """)
        return self.cur.fetchall()


    def get_all_vacancies(self):
        """ Получить данные по всем вакансиям"""
        self.cur.execute(self.text_vacancies)
        return self.cur.fetchall()


    def get_vacancies_with_keyword(self, keyword:str):
        """ Получить вакансии по ключевым словам"""
       # добавим к основному тексту запроса условие отбора по названию вакансии, если указаны ключевые слова keyword
        print(keyword)
        text = ''
        # Если слова несколько, то добавим несколько условий в логике И. Для этого поместим несколько слов в список
        list_words = keyword.strip().split(' ')
        for word in list_words:
            if text:
                text = f'{text} AND '
            text += f" LOWER(vacancies.name) LIKE '%{word.lower()}%'"

        if text:
            text = f'\nWHERE {text}'

        self.cur.execute(f'{self.text_vacancies}{text}')
        return self.cur.fetchall()


    def get_vacancies_with_area(self, keyword: str):
        """ Получить данные по вакансиям с отбором по региону"""
        # добавим к основному тексту запроса условие отбора по названию региона
        #self.cur.execute(f"{self.__text_vacancies}\nWHERE areas.name LIKE '{keyword.strip()}'")
        self.cur.execute(f"{self.text_vacancies}\nWHERE areas.name = '{keyword.strip()}'")
        return self.cur.fetchall()


    def get_count_vacancies(self):
        """ Получить количество вакансий"""
        self.cur.execute(f'SELECT count(*) FROM vacancies')
        return self.cur.fetchall()


    def get_vacancies_with_higher_salary(self):
        """ Получить вакансии, у которых зарплата выше среднего """
        self.cur.execute(f'{self.text_vacancies}\n WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)\n'
                         f'ORDER BY salary_from')
        return self.cur.fetchall()


    def get_avg_salary(self):
        """ Получить среднюю зарплату"""
        self.cur.execute(f'SELECT avg(salary_from) FROM vacancies')
        return self.cur.fetchall()


    def get_top_salaries(self):
        """ Получить 10 вакансий с наивысшими зарплатами"""
        self.cur.execute(f'{self.text_vacancies} order by salary_from DESC LIMIT 10')
        return self.cur.fetchall()


