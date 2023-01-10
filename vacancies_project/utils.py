import json
import os.path
import re
import pandas as pd
from vacancies_project.classes import Connector

FILE_PATH = '../data/all_data.json'


def collect_data(vacancy_class, key):
    vacancy = vacancy_class(None, None, None, None)
    file = vacancy.get_data(key)
    return file


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
    if os.path.isfile(FILE_PATH):
        os.remove(FILE_PATH)
    data_frame.to_json(FILE_PATH, force_ascii=False)


def upload_1000():
    file_path_1000 = '../data/1000_data.json'
    df = pd.read_json(FILE_PATH)
    df.iloc[:1000].to_json(file_path_1000, force_ascii=False)
    print(f'Вакансии загружены в файл {file_path_1000}.')


def sorting():
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    df = pd.read_json(FILE_PATH)
    df.sort_values(by=['refactored_salary'], ascending=False, inplace=True)
    return df


def get_top(vacancies_df, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    top_path = f'../data/salary_top_{top_count}'
    vacancies_df.iloc[:top_count].to_json(top_path, force_ascii=False)
    print(f'Топ вакансий загружен в файл {top_path}.')
