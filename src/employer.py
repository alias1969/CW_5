class Employer:
    """ Класс для описания компаний-работодателей"""

    def __init__(self, id, name, area, description, url, vacancies_url, count_vacancies):
        self.id = id
        self.name = name
        self.description = description
        self.area = area
        self.url = url
        self.vacancies_url = vacancies_url
        self.count_vacancies = count_vacancies

    @classmethod
    def new_employer(cls,  employer):
        """ Создание нового объекта класса Employer из списка"""
        id_employer, name, area,  description, url, vacancies_url, count_vacancies = employer
        return cls(id_employer, name, area,  description, url, vacancies_url, count_vacancies)

    def __str__(self):
        return f"""
        Компания: {self.name} (код {self.id})
        Город: {self.area}
        Количество вакансий: {self.count_vacancies}
        Ссылка на профиль компании: {self.url}
        Ссылка на вакансии компании: {self.vacancies_url} 
        -------------------------------------
        """

