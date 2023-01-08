from utils import *
from vacancies_project.classes import HH, SJVacancy, Vacancy, HHVacancy


def main():
    while True:
        user_key = input('Привет! Введи ключевое слово на английском для поиска вакансий (например, python или java): >> ')
        print(f'Ищем вакансии по ключевому слову "{user_key}" на сайтах HH и SuperJob. Нужно немного подождать.')

        hh_vac = HHVacancy(None, None, None, None)
        file_1 = hh_vac.get_data(user_key)
        dff = hh_vac.get_count_of_vacancy

        sj_vac = SJVacancy(None, None, None, None)
        file_2 = sj_vac.get_data(user_key)

        upload_data_to_file(file_1, file_2)


        print('Нашли!')

        user_choice = input('Выбери действие и введи соответствующую цифру:\n1 - чтобы загрузить в файл 1000 вакансий по выбранному ключевому слову.\n2 - чтобы вывести топ вакансий по зарплатам.\n3 - чтобы завершить работу программы. >> ')
        if user_choice == '1':
            upload_data_to_file(list_of_vacancies_to_upload)

        elif user_choice == '2':
            num = int(input('Введите необходимое число вакансий в списке: >> '))
            get_ttop(list_of_vacancies_to_analyze, num)

        elif user_choice == '3':
            print('Пока!')
            break

        else:
            print('Кажется, ты ввел что-то другое. Попробуй еще раз.')


if __name__ == '__main__':
    main()
