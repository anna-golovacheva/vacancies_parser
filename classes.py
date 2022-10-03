import requests

from bs4 import BeautifulSoup

import re

from abc import ABC, abstractmethod

import fake_useragent


class Engine(ABC):
    @abstractmethod
    def get_request(self, keyword: str):
        pass


class HH(Engine):
    def get_request(self, key: str) -> list:
        """
        Выгружает данные обо всех подходящих вакансиях с сайта HeadHunter.
        """
        key = key.capitalize()
        response_list = []
        ua = fake_useragent.UserAgent()

        for i in range(46):
            url = 'https://api.hh.ru/vacancies'
            par = {'page': i, 'per_page': '20', 'text': key, 'area': '113', 'user-agent': ua.random}
            response = requests.get(url, params=par)
            response_list += response.json()['items']

        return response_list


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
            soup_items = soup.find_all('div', class_='_2lp1U _2J-3z _3B5DQ')
            raw_items_list += soup_items

        return raw_items_list


class Vacancy:
    def __init__(self):
        self.name = None
        self.url = None
        self.description = None
        self.salary = None

    def get_data_hh(self, WebsiteClass, key: str) -> list:
        hh = WebsiteClass()
        super_list = hh.get_request(key)
        list_for_vacancies = []
        for i in range(917):
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
            salary_v_r = data.contents[3].contents[0].contents[1].text
            salary_v = salary_v_r.replace('\xa0', '')
            name_v = data.contents[3].contents[0].contents[0].text
            description_v = data.contents[5].text
            url_v = 'https://russia.superjob.ru' + data.contents[3].contents[0].contents[0].contents[0].contents[0].contents[0].attrs['href']
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
