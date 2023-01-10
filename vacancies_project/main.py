from utils import *
from vacancies_project.classes import SJVacancy, HHVacancy


def main():
    while True:
        user_key = input('Привет! Введите ключевое слово на английском языке для поиска вакансий (например, python или java): >> ')
        print(f'Ищем вакансии по ключевому слову "{user_key}" на сайтах HH и SuperJob. Нужно немного подождать.')

        file_1 = collect_data(HHVacancy, user_key)
        file_2 = collect_data(SJVacancy, user_key)

        upload_data_to_file(file_1, file_2)

        print('Нашли!')

        user_choice = input('Выберите действие и введи соответствующую цифру:\n1 - чтобы загрузить в файл 1000 вакансий по выбранному ключевому слову.\n2 - чтобы вывести топ вакансий по зарплатам.\n3 - чтобы завершить работу программы. >> ')
        if user_choice == '1':
            upload_1000()

        elif user_choice == '2':
            num = int(input('Введите необходимое число вакансий в списке: >> '))
            sorted_df = sorting()
            get_top(sorted_df, num)

        elif user_choice == '3':
            print('Пока!')
            break

        else:
            print('Кажется, вы ввели что-то другое. Попробуйте еще раз.')


if __name__ == '__main__':
    main()
