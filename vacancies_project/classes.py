import requests

from bs4 import BeautifulSoup

import re

from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def get_request(self, keyword: str):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    def __init__(self):
        self.response_list = []
        self.max_range = 0

    def get_request(self, key: str) -> list:
        """
        Выгружает данные обо всех подходящих вакансиях с сайта HeadHunter.
        """
        key = key.capitalize()

        # ua = fake_useragent.UserAgent()
        url = 'https://api.hh.ru/vacancies'
        total_num_response = requests.get(url, {'text': key, 'area': 113})
        total_num = total_num_response.json()['found']
        per_page = 100
        if total_num < 500:
            self.max_range = total_num // per_page + 1
        else:
            self.max_range = 9
        for i in range(self.max_range):
            par = {'page': i, 'per_page': per_page, 'text': key, 'area': '113'}
            response = requests.get(url, params=par)
            self.response_list += response.json()['items']

        return self.response_list

    def __len__(self):
        return len(self.response_list)


    # 'user-agent': ua.random


class Superjob(Engine):
    def get_request(self, key: str) -> list:
        """
        Выгружает данные обо всех подходящих вакансиях с сайта SuperJob.
        """
        key = key.lower()
        raw_items_list = []

        for i in range(1, 4):
            page = i
            url = f'https://russia.superjob.ru/vacancy/search/?keywords={key}&page={page}'

            response = requests.get(url)
            response_text = response.text

            soup = BeautifulSoup(response_text, 'lxml')
            soup_items = soup.find_all('div', class_='f-test-search-result-item')

            raw_items_list += soup_items

        print(len(raw_items_list))

        return raw_items_list


class Vacancy:
    __slots__ = ('name', 'url', 'description', 'salary')

    def __init__(self, name, url, description, salary):
        # self.name = name
        # self.url = url
        # self.description = description
        # self.salary = salary
        pass

    @property
    def name(self):
        return self.name

    @property
    def url(self):
        return self.url

    @property
    def description(self):
        return self.description

    @property
    def salary(self):
        return self.salary

    def get_data_hh(self, WebsiteClass, key: str) -> list:
        hh = WebsiteClass()
        super_list = hh.get_request(key)
        list_for_vacancies = []
        for i in range(len(hh)):
            name_v = super_list[i]['name']
            url_v = super_list[i]['alternate_url']
            description_v_raw = f'{super_list[i]["snippet"]["requirement"] }' + f'{super_list[i]["snippet"]["responsibility"]}'
            description_v_r = description_v_raw.replace('<highlighttext>Python</highlighttext>', '')
            description_v = description_v_r.replace('<highlighttext>python</highlighttext>', '')
            try:
                salary_v = super_list[i]['salary']['from']
            except TypeError:
                salary_v = 'не указано'
            list_for_vacancies.append([name_v, url_v, description_v, salary_v])
        return list_for_vacancies

    def get_data_sj(self, WebsiteClass, key: str) -> list:
        sj = WebsiteClass()
        list_of_everything = sj.get_request(key)

        list_for_vacancies = []
        for data in list_of_everything:
            basic_path_url = ''
            basic_path_others = ''
            salary_v_r = ''
            is_ad = False
            try:
                basic_path_description = data.contents[0].contents[0].contents[0].contents[0]
                basic_path_others = basic_path_description.contents[0].contents[0].contents[1].contents[0].contents[0]
                salary_v_r = basic_path_others.contents[1].text

            except IndexError:
                try:
                    basic_path_description = data.contents[1].contents[0].contents[0].contents[0]
                    basic_path_others = basic_path_description.contents[0].contents[0].contents[1].contents[0].contents[0]
                    salary_v_r = basic_path_others.contents[1].text
                except (IndexError, AttributeError) as e:
                    print('Пропускаю рекламу...')
                    is_ad = True

            finally:
                if is_ad:
                    continue

                salary_v = salary_v_r.replace('\xa0', '')
                name_v = basic_path_others.contents[0].text
                description_v = basic_path_description.contents[2].text
                url_v = 'https://russia.superjob.ru' + basic_path_others.contents[0].contents[0].contents[0].contents[0].attrs['href']
                list_for_vacancies.append([name_v, url_v, description_v, salary_v])

        return list_for_vacancies

    def set_data(self, list_of_params: list) -> None:
        self.name, self.url, self.description, self.salary = list_of_params[0], list_of_params[1], list_of_params[2], list_of_params[3]

    def _refactor_salary(self) -> int:
        """
        Приводит данные о зарплате к одному виду - числовому представалению.
        """
        money = self.salary
        if type(money) is int:
            return money
        elif type(money) is str and 'По договорённости' not in money and 'не указано' not in money and 'None' not in money:
            regexp = re.compile(r'(^\d{4,6})|[а-я]{2}(\d{4,6})')
            m = regexp.match(money)
            if m.group(1):
                return int(m.group(1))
            elif m.group(2):
                return int(m.group(2))
        else:
            return 0

    def get_vacancy(self) -> dict:
        """
        Создает и возвращает словарь с данными о вакансии (зарплата только в формате int).
        """
        vacancy_dict = {
            'Позиция': self.name,
            'Ссылка': self.url,
            'Описание': self.description,
            'Заработная плата': self._refactor_salary()
        }

        return vacancy_dict

    def __repr__(self) -> str:
        """
        Создает и возвращает строку, содержащую данные о вакансии.
        """

        return f'Позиция: {self.name}:\nОписание: {self.description}\nЗаработная плата от: {self.salary}\nСсылка на вакансию: {self.url}\n\n'


class CountMixin:

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        pass


class HHVacancy(Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """

    def __str__(self):
        return f'HH: {self.comany_name}, зарплата: {self.salary} руб/мес'


class SJVacancy(Vacancy):  # add counter mixin
    """ SuperJob Vacancy """

    def __str__(self):
        return f'SJ: {self.comany_name}, зарплата: {self.salary} руб/мес'

class Connector:
    """
    Класс-коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None
    @property
    def data_file(self):
        pass

    @data_file.setter
    def data_file(self, value):
        # тут должен быть код для установки файла
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        pass

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        pass

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        pass

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        pass