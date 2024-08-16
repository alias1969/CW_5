from src.utils import (create_database, get_employee_from_website, get_vacancies_from_website,
                       insert_data, execute_request)


def main():

    # создаем базу данных и ее таблицы
    create_database()

    # получим данные с сайта по компаниям и вакансиям
    employee = get_employee_from_website()
    vacancies = get_vacancies_from_website()

    # запишем полученные с сайта данные в бд
    insert_data(employee, vacancies)

    # режимы работы с базой данных
    mode_dict = {
        '1' : 'Компании-работодатели и их вакансии',
        '2' : 'Количество вакансий',
        '3' : 'Все вакансии',
        '4' : 'Список всех вакансий по ключевым словам',
        '5' : 'Список вакансий с зарплатой выше среднего',
        '6' : 'Средняя зарплата всех вакансий',
        '7' : 'ТОП-10 вакансий с самыми высокими зарплатами',
        '8' : 'Выборка по региону',
        '0' : 'Выход из программы'
    }
    print(f'Выберите запрос: \n')
    [print(f'{key} - {value}') for key, value in mode_dict.items()]

    while True:
        keyword = ''
        # пользователь должен выбрать режим вывода данных
        user_input = input('Введите номер запроса\n').strip()
        # если пользователь ввел 0, то выходим
        if user_input == '0':
            break
        elif mode_dict.get(user_input, 0) == 0:
            print('Введен некорректный ключ')
            continue
        elif user_input == '4':
            keyword = input('Введите название вакансии')
            if not keyword:
                print("Вы не ввели ключевое слово")
                continue

        elif user_input == '8':
            keyword = input('Введите название региона')
            if not keyword:
                print("Вы не ввели название региона")
                continue

        result_request = execute_request(user_input, keyword)

        if len(result_request) == 0:
            print(f'{mode_dict[user_input]}: нет данных')
        else:
            print(f'{mode_dict[user_input]}:')
            for item in result_request:
                print(item)


if __name__ == '__main__':
    main()

