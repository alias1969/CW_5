class Vacancy:
    """ Класс для описания вакансии"""

    def __init__(self, id_vacancy, name, employer, salary_from, salary_to, currency, area, url, employment, experience, schedule,requirement, responsibility):
        self.id = id_vacancy
        self.name = name
        self.employer = employer
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.area = area
        self.url = url
        self.employment = employment
        self.experience = experience
        self.schedule = schedule
        self.requirement = requirement
        self.responsibility = responsibility

    @classmethod
    def new_vacancy(cls,  vacancy):
        """ Создание нового объекта класса Vacancy из кортежа"""
        id_vacancy, name, employer, salary_from, salary_to, currency, area, url, employment, experience, schedule, requirement, responsibility = vacancy
        return cls(id_vacancy, name, employer, salary_from, salary_to, currency, area, url,
                   employment, experience, schedule, requirement, responsibility)

    def __str__(self):
        if self.salary_to != 0:
            salary_to = f' до {self.salary_to}'
        else:
            salary_to = ''

        return f"""
        Компания: {self.employer}      
        Город: {self.area}       
        Вакансия ({self.id}): {self.name}
        Зарплата: от {self.salary_from}{salary_to} ({self.currency})
        Ссылка на вакансию: {self.url}
        Статус занятости: {self.employment}
        График работы: {self.schedule}
        Требования к опыту работы: {self.experience}
        Обязанности: {self.responsibility}
        Требования к кандидату: {self.requirement}\n-------------------------------------
        """

