def upload_vacancies_hh(WebsiteClass, VacancyClass) -> list:
    """
    Создает объекты класса HH. Создает на их основе объекты класса Vacancy,
    записывает их в файл и возвращает список словарей, в которых содержатся
    данные вакансий.
    """
    hh = WebsiteClass()
    super_list = hh.get_request()

    vacancies_list_hh = []

    with open('data.txt', 'w', encoding='utf-8') as file:

        for i in range(917):
            name_v = super_list[i]['name']
            url_v = super_list[i]['alternate_url']
            description_v_raw = f'{super_list[i]["snippet"]["requirement"] }' + f'{super_list[i]["snippet"]["responsibility"]}'
            description_v_r = description_v_raw.replace('<highlighttext>Python</highlighttext>', '')
            description_v = description_v_r.replace('<highlighttext>python</highlighttext>', '')
            try:
                salary_v = super_list[i]['salary']['from']
            except:
                salary_v = 'не указано'

            vacancy = VacancyClass(name_v, url_v, description_v, salary_v)

            vacancies_list_hh.append(vacancy.get_vacancy())

            file.write(vacancy.__repr__())

        return vacancies_list_hh


def upload_vacancies_sj(WebsiteClass, VacancyClass) -> list:
    """
    Создает объекты класса SuperJob. Создает на их основе объекты класса Vacancy,
    записывает их в файл и возвращает список словарей, в которых содержатся
    данные вакансий.
    """
    sj = WebsiteClass()
    list_of_everything = sj.get_request()

    vacancies_list_sj = []

    with open('data.txt', 'a', encoding='utf-8') as file:
        for data in list_of_everything:
            salary_v_r = data.contents[3].contents[0].contents[1].text
            salary_v = salary_v_r.replace('\xa0', '')
            name_v = data.contents[3].contents[0].contents[0].text
            description_v = data.contents[5].text
            url_v = 'https://russia.superjob.ru' + data.contents[3].contents[0].contents[0].contents[0].contents[0].contents[0].attrs['href']

            vacancy = VacancyClass(name_v, url_v, description_v, salary_v)

            vacancies_list_sj.append(vacancy.get_vacancy())

            file.write(vacancy.__repr__())

        return vacancies_list_sj


def get_top(vac_list: list, num: int) -> None:
    """
    Сортирует список всех вакансий по убыванию зарплаты. Выводит заданное число
    самых высокооплачиваемых вакансий.
    """
    top = sorted(vac_list, key=lambda item: item['Заработная плата'], reverse=True)
    for t in top[:num]:
        for k, v in t.items():
            print(f'{k}: {v}')
