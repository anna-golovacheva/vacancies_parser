def make_lists_of_vacancies(list_of_raw_data: list, vac) -> tuple:
    """
    Устанавливает значения полей объектов класса Vacancy, формирует два списка:
    для последующей загрузки данных по каждой вакансии в файл и для вывода
    информации для пользователя.
    """
    list_of_vacs_to_upload = []
    list_of_vacs_to_analyze = []
    for data in list_of_raw_data:
        vac.set_data(data)
        list_of_vacs_to_upload.append(vac.__repr__())
        list_of_vacs_to_analyze.append(vac.get_vacancy())

    return list_of_vacs_to_upload, list_of_vacs_to_analyze


def upload_data_to_file(up_list: list) -> None:
    with open('../data.txt', 'w', encoding='utf-8') as file:
        for vac in up_list:
            file.write(vac)

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
