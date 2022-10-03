from utils import *
from classes import HH, Superjob, Vacancy


def main():
    while True:
        user_key = input('Привет! Введи ключевое слово на английском для поиска вакансий (например, python или java): >> ')
        print(f'Ищем вакансии по ключевому слову "{user_key}" на сайтах HH и SuperJob. Нужно немного подождать.')
        vacancy = Vacancy()
        list_of_vacancies_hh = vacancy.get_data_hh(HH, user_key)

        list_of_vacancies_to_upload = []
        list_of_vacancies_to_analyze = []

        list_up_hh, list_an_hh = make_lists_of_vacancies(list_of_vacancies_hh, vacancy)
        list_of_vacancies_to_upload.extend(list_up_hh)
        list_of_vacancies_to_analyze.extend(list_an_hh)

        list_of_vacancies_sj = vacancy.get_data_sj(Superjob, user_key)
        list_up_sj, list_an_sj = make_lists_of_vacancies(list_of_vacancies_sj, vacancy)
        list_of_vacancies_to_upload.extend(list_up_sj)
        list_of_vacancies_to_analyze.extend(list_an_sj)

        print('Нашли!')

        user_choice = input('Выбери действие и введи соответствующую цифру:\n1 - чтобы загрузить в файл 1000 вакансий по выбранному ключевому слову.\n2 - чтобы вывести топ вакансий по зарплатам.\n3 - чтобы завершить работу программы. >> ')
        if user_choice == '1':
            upload_data_to_file(list_of_vacancies_to_upload)

        elif user_choice == '2':
            num = int(input('Введите необходимое число вакансий в списке: >> '))
            get_top(list_of_vacancies_to_analyze, num)

        elif user_choice == '3':
            print('Пока!')
            break

        else:
            print('Кажется, ты ввел что-то другое. Попробуй еще раз.')


if __name__ == '__main__':
    main()
