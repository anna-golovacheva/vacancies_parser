import requests

from bs4 import BeautifulSoup

import re

from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    def get_request(self) -> list:
        """
        Выгружает данные обо всех подходящих вакансиях с сайта HeadHunter.
        """
        response_list = []

        for i in range(46):
            url = 'https://api.hh.ru/vacancies'
            par = {'page': i, 'per_page': '20', 'text': 'Python', 'area': '113'}
            response = requests.get(url, params=par)
            response_list += response.json()['items']

        return response_list


class Superjob(Engine):
    def get_request(self) -> list:
        """
        Выгружает данные обо всех подходящих вакансиях с сайта SuperJob.
        """
        raw_items_list = []

        for i in range(1, 4):
            page = i
            url = f'https://russia.superjob.ru/vacancy/search/?keywords=python&page={page}'
            response = requests.get(url)
            response_text = response.text
            soup = BeautifulSoup(response_text, 'lxml')
            soup_items = soup.find_all('div', class_='_2lp1U _2J-3z _3B5DQ')
            raw_items_list += soup_items

        return raw_items_list


class Vacancy:
    def __init__(self, name: str, url: str, description: str, salary: str | int):
        self.name = name
        self.url = url
        self.description = description
        self.salary = salary

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

        return f'Позиция: {self.name}:\nОписание: {self.description}\nЗаработная плата от: {self.salary}\nСсылка на вакансию: {self.url}\n'
