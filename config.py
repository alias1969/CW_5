# Параметры базы данных
PARAMS = {
    'host':'localhost',
    #'database':'Vacancies',
    'user':'postgres',
    'password':'123',
    'port':'5432'
    }

DATABASE_NAME = 'Vacancies'

# Параметры и переменные для получения данных с сайта
# id компаний, по которым будем получать вакансии
EMPLOYERS_LIST_ID = ['4307', '4787018', '4219', '5557093', '1579449', '2180', '1057', '1180', '208707', '205']
# количество страниц
PER_PAGES = 100
# получать данные только с зарплатой
ONLY_WITH_SALARY = True
