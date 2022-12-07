from datetime import date
import collections
import requests


def write_json(text, name):
    with open(name, 'a', encoding='utf-8') as f:
        f.write(f'{text}\n')


def get_request(url, params, headers):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    return response


def get_base_vacancies(vacancy):
    url = 'https://api.hh.ru/vacancies'
    page = 0
    url_parameter = {'text': vacancy, 'area': '1', 'describe_arguments': 'true', 'page': page}
    headers = {}
    name_file = f'w_data_{date.today()}_{vacancy}.txt'
    pages = get_request(url, url_parameter, headers).get('pages')
    while page < pages:
        url_parameter = {'text': vacancy, 'area': '1', 'describe_arguments': 'true', 'page': page}
        works = get_request(url, url_parameter, headers).get('items')
        for work in works:
            write_json(work, name_file)
        page += 1
    return name_file


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


if __name__ == "__main__":
    vacancy = 'sql разработчик'
    patch_to_file = get_base_vacancies(vacancy)
    vacancies = get_vacancies_from_file(patch_to_file)
