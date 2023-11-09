#!/usr/bin/env python3

from utils import *
from classes import SJVacancy, HHVacancy
from settings import HH_FILE, SJ_FILE


def main():
    while True:

        user_key = input('Привет! Введите ключевое слово на английском ' \
                         'языке для поиска вакансий, например, python ' \
                         'или java (чтобы остановить работу программы, ' \
                         'введите stop): >> ')
        if user_key.lower() == 'stop':
            break
        
        print(f'Ищем вакансии по ключевому слову "{user_key}" на сайтах ' \
              f'HH и SuperJob. Нужно немного подождать.')

        for file in (HH_FILE, SJ_FILE):
            remove_file(file)

        file_1 = collect_data(HHVacancy, user_key)
        if file_1 is None:
            print('На HH по вашему запросу ничего не нашлось :(')

        file_2 = collect_data(SJVacancy, user_key)
        if file_2 is None:
            print('На SuperJob по вашему запросу ничего не нашлось :(')

        if file_1 is None and file_2 is None:
            print('Попробуйте переформулировать запрос')
            continue

        all_data = upload_data_to_file(file_1, file_2)

        print('Нашли!')

        user_choice = input('Выберите действие и введите соответствующую ' \
                            'цифру:\n1 - чтобы загрузить в файл 1000 ' \
                            'вакансий по выбранному ключевому слову.\n2 - ' \
                            'чтобы загрузить в файл топ вакансий по ' \
                            'зарплатам.\n3 - чтобы загрузить в файл ' \
                            'вакансии по выбранному ключевому слову с ' \
                            'дополнительным параметром.\n4 - завершить ' \
                            'работу программы. >> ')
        if user_choice == '1':
            print(upload_1000(all_data))

        elif user_choice == '2':
            num = int(input('Введите необходимое число вакансий в списке: ' \
                            '>> '))
            sorted_data = sorting(all_data)
            print(get_top(sorted_data, num))

        elif user_choice == '3':
            num_key = input('Введите параметр, который хотите задать: ' \
                            '1 - название, 2 - описание или 3 - зарплата. ' \
                            '>> ')
            strong = True

            if num_key not in ['1', '2', '3']:
                print('По такому параметру поиск невозможен.')

            elif num_key == '1':
                key = 'name'
                value = input('Введите ключевое слово, которое должно ' \
                              'содержаться в названии вакансии на сайте. >> ')

            elif num_key == '2':
                key = 'description'
                value = input('Введите ключевое слово, которое должно ' \
                              'содержаться в описании вакансии на сайте. >> ')

            elif num_key == '3':
                while True:
                    key = 'salary'
                    value = input('Введите число. >> ')
                    if not value.isdigit():
                        print('Необходимо ввести число.')
                    else:
                        value = int(value)
                        break

            print(select_data_from_all_data(all_data,
                                            {key: value},
                                            strong=strong))

        elif user_choice == '4':
            print('Пока!')
            break

        else:
            print('Кажется, вы ввели что-то другое. Попробуйте еще раз.')


if __name__ == '__main__':
    main()
