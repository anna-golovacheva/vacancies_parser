import json
import os.path
from vacancies_project.classes import Connector, Vacancy

FILE_PATH = '../data/all_data.json'


def collect_data(vacancy_class, key):
    vacancy = vacancy_class(None, None, None, None)
    file = vacancy.get_data(key)
    return file


def get_data_from_little_file(file):
    connector = Connector(file)
    data_from_file = connector.select(None)
    return data_from_file


def check_file(file):
    file_path = '../data/' + file
    if os.path.isfile(file_path):
        os.remove(file_path)


def upload_data_to_file(file_list_1, file_list_2):
    all_data_file = 'all_data.json'
    check_file(all_data_file)

    all_data = []
    for file in (file_list_1, file_list_2):
        data = get_data_from_little_file(file)
        all_data += data
    connector = Connector(all_data_file)
    connector.insert(all_data)

    return connector.data_file


def upload_1000(file):
    file_1000 = '1000_data.json'

    connector_1 = Connector(file)
    extracted_data = connector_1.select(None)[:1000]

    connector_2 = Connector(file_1000)
    connector_2.insert(extracted_data)

    return f'Информация о 1000 вакансий по запросу загружена в файл {connector_2.data_file}'


def sorting(file):
    """ Должен сортировать любой список вакансий по ежемесячной оплате
    (gt, lt magic methods) """
    sorted_file = 'sorted_data.json'

    connector_1 = Connector(file)
    data_to_sort = connector_1.select(None)
    vacancies_list = []
    for vac in data_to_sort:
        name = vac['name']
        url = vac['url']
        description = vac['description']
        salary = vac['salary']
        vacancy = Vacancy(name, url, description, salary)
        vacancy.refactor_salary()

        vacancies_list.append(vacancy)

    sorted_vacancies = sorted(vacancies_list, reverse=True)
    data_for_file = []
    for vac in sorted_vacancies:
        vac_dict = {
            'name': vac.name,
            'url': vac.url,
            'description': vac.description,
            'salary': vac.salary}
        data_for_file.append(vac_dict)

    connector_2 = Connector(sorted_file)
    connector_2.insert(data_for_file)

    print(f'Информация о 1000 вакансий по запросу загружена в файл {connector_2.data_file}')
    return connector_2.data_file


def get_top(file, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате
    (iter, next magic methods) """
    salary_top_file = f'salary_top_{top_count}'

    connector_1 = Connector(file)
    sorted_data = connector_1.select(None)
    top_data = sorted_data[:top_count]

    connector_2 = Connector(salary_top_file)
    connector_2.insert(top_data)

    return f'Информация о {top_count} самых высокооплачиваемых вакансиях загружена в файл {connector_2.data_file}'


def select_data_from_all_data(file, query_dict, strong=True):
    key, value = list(query_dict.items())[0]
    selected_data_file = f'selected_{key}_{value}.json'
    connector_1 = Connector(file)
    selected_data = connector_1.select(query_dict, strong)

    connector_2 = Connector(selected_data_file)
    connector_2.insert(selected_data)

    return f'Информация о вакансиях по запросу {key} - {value} загружена в файл {connector_2.data_file}'

