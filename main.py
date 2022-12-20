import time
from datetime import datetime
from datetime import date
from datetime import timedelta
import collections
import requests


def write_json(text, name):
    with open(name, 'a', encoding='utf-8') as f:
        f.write(f'{text}\n')


def get_request(url, params=None, headers={}):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    # print(response.keys())
    # print(response.get('items'))
    # print(response.get('found'))
    # print(response.get('pages'))
    # print(response.get('per_page'))
    # print(response.get('page'))
    # print(response.get('clusters'))
    # print(response.get('arguments'))
    # print(response.get('alternate_url'))
    return response


def get_date_responses(count_pages: int):
    n = int(count_pages / 1000) + 1
    days_count = int(30/n) - 1
    return days_count


def get_base_vacancies(vacancy, name_file):
    url = 'https://api.hh.ru/vacancies'
    page = 0
    url_parameter = {'text': vacancy, 'area': '1', 'describe_arguments': 'true', 'page': page, 'date_from ': None, 'date_to': None}
    response = get_request(url, url_parameter, {})
    days_count = get_date_responses(response.get('found'))
    for i in range(int(30/days_count)):
        url_parameter['date_to'] = date.today()-timedelta(i * days_count)
        url_parameter['date_from'] = date.today()-timedelta(((i+1) *days_count) -1)
        response = get_request(url, url_parameter, {})
        time.sleep(1)
        pages = response.get('pages')
        page = 0
        print(pages, ' ---', date.today()-timedelta(i * days_count), date.today()-timedelta(((i+1) *days_count) -1))
        while page < pages:
            print(page)
            url_parameter['page'] = page
            works = get_request(url, url_parameter, {}).get('items')
            for work in works:
                write_json(work, name_file)
            page += 1
    return None


def get_vacancies_from_file(patch):
    data_check = collections.defaultdict(list)
    id_vacansy = []
    id_vacansy_bed = []
    with open(patch, 'r', encoding='utf-8') as f:
        text = f.readlines()
    for i in text:
        a = eval(i)
        id_emploer = a.get('employer').get('id')
        name_vacansy = a.get('name')
        if data_check.get(id_emploer) is None or name_vacansy not in data_check.get(id_emploer):
            id_vacansy.append(a.get('id'))
            data_check[id_emploer].append(name_vacansy)
        elif name_vacansy in data_check.get(id_emploer):
            id_vacansy_bed.append(a.get('id'))
    return id_vacansy


def get_vacanci(ids_vacancies, name_file):
    new_name = f'vac_{name_file}'
    n = 1
    for i in ids_vacancies:
        url = f'https://api.hh.ru/vacancies/{i}'
        vacancy =  get_request(url)
        print(n)
        write_json(vacancy, new_name)
        n += 1




if __name__ == "__main__":
    vacancy = 'sql разработчик'
    name_file = f'w_data_{date.today()}_{vacancy}.txt'
    # patch_to_file = get_base_vacancies(vacancy, name_file)
    ids_vacancies = get_vacancies_from_file(name_file)
    print(len(ids_vacancies))
    get_vacanci(ids_vacancies,name_file)
