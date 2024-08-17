from src.vacancy import Vacancy

def test_vacancy_init(vacancy):
    """ Тест инициализации класса """

    assert vacancy.id == '1234'
    assert vacancy.name == 'Менеджер по работе с клиентами'
    assert vacancy.employer == 'Марс'
    assert vacancy.area == 'Воронеж'
    assert vacancy.url == 'https://hh.ru/vacancy/101709979'
    assert vacancy.salary_from == 40000
    assert vacancy.salary_to == 70000
    assert vacancy.currency == 'RUR'
    assert vacancy.requirement == 'Опыт работы в продажах обязателен'
    assert vacancy.responsibility == 'Консультирование клиентов'
    assert vacancy.employment == 'Полная занятость'
    assert vacancy.schedule == 'Полный день'
    assert vacancy.experience == 'От 1 года до 3 лет'


def test_vacancy_print(vacancy):
    """ Тест печати экземпляра класса"""
    assert f'{vacancy}' == """
        Компания: Марс      
        Город: Воронеж       
        Вакансия (1234): Менеджер по работе с клиентами
        Зарплата: от 40000 до 70000 (RUR)
        Ссылка на вакансию: https://hh.ru/vacancy/101709979
        Статус занятости: Полная занятость
        График работы: Полный день
        Требования к опыту работы: От 1 года до 3 лет
        Обязанности: Консультирование клиентов
        Требования к кандидату: Опыт работы в продажах обязателен
        -------------------------------------
        """

def test_new_vacancy(vacancy):
    """ Тест создания нового объекта класса Vacancy из кортежа"""
    data = ('1234', 'Менеджер по работе с клиентами', 'Марс', 40000, 70000, 'RUR', 'Воронеж',
            'https://hh.ru/vacancy/101709979', 'Полная занятость', 'От 1 года до 3 лет', 'Полный день',
            'Опыт работы в продажах обязателен', 'Консультирование клиентов')
    assert f'{Vacancy.new_vacancy(data)}' == f'{vacancy}'

