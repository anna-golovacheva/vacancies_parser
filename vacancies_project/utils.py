import json
import re
import pandas as pd
from vacancies_project.classes import Connector


def refactor_salary(s) -> int:
    """
    Приводит данные о зарплате к одному виду - числовому представалению.
    """
    money = s
    if type(money) is int:
        return money
    elif type(
            money) is str and 'По договорённости' not in money and 'не указано' not in money and 'None' not in money:
        regexp = re.compile(r'(^\d{4,6})|[а-я]{2}(\d{4,6})')
        m = regexp.match(money)
        if m.group(1):
            return int(m.group(1))
        elif m.group(2):
            return int(m.group(2))
    else:
        return 0


def create_data_frame(file):
    df = pd.read_json(file)
    df['refactored_salary'] = df['salary'].apply(refactor_salary)
    return df


def upload_data_to_file(file_list_1, file_list_2) -> None:
    df_1, df_2 = create_data_frame(file_list_1), create_data_frame(file_list_2)
    data_frame = pd.concat([df_1, df_2], ignore_index=True)
    data_frame.to_json('../data/raw_data.json', force_ascii=False)

    print('Вакансии загружены в файл.')


def get_ttop(vac_list: list, num: int) -> None:
    """
    Сортирует список всех вакансий по убыванию зарплаты. Выводит заданное число
    самых высокооплачиваемых вакансий.
    """
    top = sorted(vac_list, key=lambda item: item['Заработная плата'], reverse=True)
    for t in top[:num]:
        for k, v in t.items():
            print(f'{k}: {v}')


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    pass


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    pass
