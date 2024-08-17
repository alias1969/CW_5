from src.employer import Employer

def test_employer_init(employer):
    """ Тест инициализации класса """
    assert employer.id == '1234'
    assert employer.name == 'Марс'
    assert employer.area == 'Воронеж'
    assert employer.description == 'Очень крутая компания'
    assert employer.url == 'https://hh.ru/mars'
    assert employer.vacancies_url == 'https://hh.ru//mars/vacancy'
    assert employer.count_vacancies == 12


def test_employer_print(employer):
    """ Тест печати экземпляра класса"""
    assert f'{employer}' == """
        Компания: Марс (код 1234)
        Город: Воронеж
        Количество вакансий: 12
        Ссылка на профиль компании: https://hh.ru/mars
        Ссылка на вакансии компании: https://hh.ru//mars/vacancy
        -------------------------------------
        """

def test_new_vacancy(employer):
    """ Тест создания нового объекта класса Employer из кортежа"""
    data = ('1234', 'Марс', 'Воронеж', 'Очень крутая компания', 'https://hh.ru/mars',
            'https://hh.ru//mars/vacancy', 12)
    assert f'{Employer.new_employer(data)}' == f'{employer}'

