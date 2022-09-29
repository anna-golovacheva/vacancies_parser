from utils import *
from classes import HH, Superjob, Vacancy


def main():
    while True:

        user_choice = input('Привет! Выбери действие и введи соответствующую цифру:\n1 - чтобы загрузить в файл 1000 вакансий по ключевому слову Python.\n2 - чтобы вывести топ вакансий по зарплатам.\n3 - чтобы закончить работу программы. >> ')
        if user_choice == '1':
            print('Придется немного подождать, пока файл загрузится.')
            vacancy_list_hh = upload_vacancies_hh(HH, Vacancy)
            vacancy_list_sj = upload_vacancies_sj(Superjob, Vacancy)

            print('Файл загружен')

        elif user_choice == '2':
            user_num = int(input('Введите необходимое количество вакансий: >> '))
            print('Сейчас сформируем список.')
            vacancy_list_hh = upload_vacancies_hh(HH, Vacancy)
            vacancy_list_sj = upload_vacancies_sj(Superjob, Vacancy)
            all_vacancies_list = vacancy_list_hh + vacancy_list_sj

            get_top(all_vacancies_list, user_num)

        elif user_choice == '3':
            print('Пока!')
            break

        else:
            print('Кажется, ты ввел что-то другое. Попробуй еще раз.')


if __name__ == '__main__':
    main()
