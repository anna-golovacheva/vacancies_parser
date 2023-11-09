import json
import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import os
import re

from settings import *


class Connector:
    """
    Класс-коннектор к json-файлу
    """
    __data_file = None

    def __init__(self, df: str):
        self.__data_file = DATA_PATH + df
        self.__connect()

    @property
    def data_file(self) -> None:
        return self.__data_file

    @data_file.setter
    def data_file(self, value: str) -> None:
        if value[-5:-1] == '.json':
            self.__data_file = DATA_PATH + value
        else:
            self.__data_file = DATA_PATH + value + '.json'
        self.__connect()

    def __connect(self) -> None:
        """
        Проверка файла с данными на существование и
        создание его при необходимости
        """
        if os.path.isfile(self.__data_file):
            try:
                with open(self.__data_file, encoding='utf-8') as file:
                    value_from_file = json.load(file)[0]['name']
                capitalized_check = value_from_file.capitalize()
            except (AttributeError, IndexError):
                raise AttributeError('файл поврежден')
        else:
            new_file = open(self.__data_file, 'x')
            new_file.close()

    def insert(self, data: list) -> None:
        """
        Запись данных в файл с сохранением структуры исходных данных
        """
        with open(self.__data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

    def select(self, query: dict, strong: bool=True) -> list:
        """
        Выбор данных из файла с применением фильтрации;
        query содержит словарь, в котором ключ - это поле для
        фильтрации, а значение - это искомое значение
        """
        with open(self.__data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if query:
            key, value = list(query.items())[0]
            if strong:
                selected_data = [item for item in data if item[key] == value]
            else:
                selected_data = [item for item in data if value in item[key]]
            return selected_data
        return data

    def delete(self, query: dict) -> None:
        """
        Удаление записей из файла, которые соответствуют запросу,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if query:
            with open(self.__data_file, 'r', encoding='utf-8') as file_r:
                data = json.load(file_r)

            key, value = query.items()[0]
            saved_data = [item for item in data if item[key] != value]
            with open(self.__data_file, 'w', encoding='utf-8') as file_w:
                json.dump(saved_data, file_w)


class Engine(ABC):
    @abstractmethod
    def get_request(self, keyword: str):
        pass

    @staticmethod
    def get_connector(file_name: str) -> Connector:
        """ Возвращает экземпляр класса Connector """
        connector = Connector(file_name)
        return connector


class HH(Engine):
    def __init__(self):
        self.response_list = []
        self.max_range = 0

    def get_request(self, key: str) -> list:
        """
        Выгружает данные обо всех подходящих вакансиях с сайта HeadHunter.
        """
        key = key.capitalize()
        url = HH_URL

        total_num_response = requests.get(url, {'text': key,
                                                'area': HH_AREA_PARAM
                                                })
        total_num = total_num_response.json()['found']
        if total_num <= HH_TOTAL_NUM:
            self.max_range = total_num // HH_PER_PAGE + 1
        else:
            self.max_range = HH_MAX_RANGE

        for i in range(self.max_range):
            params = {'page': i,
                      'per_page': HH_PER_PAGE,
                      'text': key,
                      'area': str(HH_AREA_PARAM)}
            response = requests.get(url, params=params)
            self.response_list += response.json()['items']

        return self.response_list

    def __len__(self):
        return len(self.response_list)


class SuperJob(Engine):
    def get_request(self, key: str) -> list:
        """
        Выгружает данные обо всех подходящих вакансиях с сайта SuperJob.
        """
        key = key.lower()
        raw_items_list = []
        url_start = SJ_URL

        for i in range(1, 4):
            page = i
            url = url_start + f'?keywords={key}&page={page}'

            response = requests.get(url)
            response_text = response.text

            soup = BeautifulSoup(response_text, 'lxml')
            soup_items = soup.find_all('div',
                                       class_= SJ_SOUP_CLASS
                                       )

            raw_items_list += soup_items

        return raw_items_list


class Vacancy:
    __slots__ = ('__name', '__url',
                 '__description', '__salary',
                 '__refactored_salary')

    def __init__(self, name: str, url: str,
                 description: str, salary: str | int):
        self.__name = name
        self.__url = url
        self.__description = description
        self.__salary = salary
        self.__refactored_salary = 0

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, value: str) -> None:
        self.__url = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        self.__description = value.replace('<highlighttext>', '')

    @property
    def salary(self) -> str | int:
        return self.__salary

    @salary.setter
    def salary(self, value: str | int)  -> None:
        self.__salary = value

    def refactor_salary(self) -> None:
        """
        Приводит данные о зарплате к одному виду - числовому представлению.
        """
        money = self.__salary

        if isinstance(money, int):
            self.__refactored_salary = self.__salary

        elif isinstance(money, str):
            if all(word not in money for word in NO_SALARY_LIST):
                regexp = re.compile(r'(^\d{4,6})|[а-я]{2}(\d{4,6})')
                m = regexp.match(money)
                if m.group(1):
                    self.__refactored_salary = int(m.group(1))
                elif m.group(2):
                    self.__refactored_salary = int(m.group(2))

    def __lt__(self, other: int) -> bool:
        return self.__refactored_salary < other

    def __gt__(self, other: int) -> bool:
        return self.__refactored_salary > other

    def __eq__(self, other: int) -> bool:
        return self.__refactored_salary == other

    def __ne__(self, other: int) -> bool:
        return self.__refactored_salary != other

    def __repr__(self):
        """
        Возвращает строку, содержащую данные о вакансии.
        """
        return f'Позиция: {self.__name}:\nОписание: {self.__description}\n' \
               f'Заработная плата от: {self.__refactored_salary}\n' \
               f'Ссылка на вакансию: {self.__url}\n\n'


class CountMixin:
    @property
    def get_count_of_vacancy(self) -> int:
        """
        Возвращает количество вакансий от текущего сервиса (из файла).
        """
        dir = DATA_PATH
        with open(dir + self.data_file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return len(data)


class HHVacancy(Vacancy, CountMixin):
    """ Класс вакансий HeadHunter """
    __slots__ = ('data_file_name')

    def __init__(self, __name: str, __url: str,
                 __description: str, __salary: str):
        self.data_file_name = HH_FILE
        super().__init__(__name, __url, __description, __salary)

    def __str__(self):
        return f'HH: {self.__name}, зарплата: {self.__salary} руб/мес'

    def get_data(self, key: str) -> str:
        hh = HH()
        data_list = hh.get_request(key)
        list_for_vacancies = []

        if len(hh) < 1:
            return None

        for i in range(len(hh)):
            self.__name = data_list[i]['name']
            self.__url = data_list[i]['alternate_url']
            description_req = f'{data_list[i]["snippet"]["requirement"] }'
            description_resp = f'{data_list[i]["snippet"]["responsibility"]}'
            description_raw = description_req + description_resp

            description_r = description_raw.replace(SJ_HTML_ARTIFACTS, '')
            self.__description = description_r.replace(SJ_HTML_ARTIFACTS.lower(),
                                                       '')
            try:
                self.__salary = data_list[i]['salary']['from']
            except TypeError:
                self.__salary = NO_SALARY

            list_for_vacancies.append({'name': self.__name, 'url': self.__url,
                                       'description': self.__description,
                                       'salary': self.__salary})

        connector = hh.get_connector(self.data_file_name)
        connector.insert(list_for_vacancies)

        return connector.data_file


class SJVacancy(Vacancy, CountMixin):
    """ Класс вакансий SuperJob """
    __slots__ = ('data_file_name')

    def __init__(self, __name: str, __url: str,
                 __description: str, __salary: str):
        self.data_file_name = SJ_FILE
        super().__init__(__name, __url, __description, __salary)

    def __str__(self):
        return f'SJ: {self.__name}, зарплата: {self.__salary} руб/мес'

    def get_data(self, key: str) -> str:
        sj = SuperJob()
        data_list = sj.get_request(key)
        list_for_vacancies = []
        for data in data_list:
            basic_path_description = ''
            basic_path_others = ''
            salary_v_r = ''
            is_ad = False
            try:

                basic_path_description = (data.contents[1].contents[0]
                                          .contents[0])
                basic_path_others = (basic_path_description.contents[0]
                                     .contents[0].contents[1]
                                     .contents[0].contents[0])
                salary_v_r = basic_path_others.contents[1].text

            except (IndexError, AttributeError) as e:
                try:
                    basic_path_description = (data.contents[0].contents[0]
                                              .contents[0])
                    basic_path_others = (basic_path_description.contents[0]
                                         .contents[0].contents[1]
                                         .contents[0].contents[0])
                    salary_v_r = basic_path_others.contents[1].text
                except (IndexError, AttributeError) as e:
                    print('Пропускаем рекламу...')
                    is_ad = True

            finally:
                if is_ad:
                    continue

                url_start = SJ_URL
                self.__salary = salary_v_r.replace('\xa0', '')
                self.__name = basic_path_others.contents[0].text
                self.__description = basic_path_description.contents[2].text
                self.__url = url_start + (basic_path_others.contents[0]
                                          .contents[0].contents[0]
                                          .contents[0].attrs['href'])
                list_for_vacancies.append({'name': self.__name,
                                           'url': self.__url,
                                           'description': self.__description,
                                           'salary': self.__salary})

        if len(list_for_vacancies) < 1:
            return None

        connector = sj.get_connector('data_sj.json')
        connector.insert(list_for_vacancies)

        return connector.data_file
