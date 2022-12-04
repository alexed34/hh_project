from datetime import date
import collections
import json

import requests

def write_json(text, url_parameter):
    current_date = date.today()
    vacancy = url_parameter['text']
    with open(f'w_data_{current_date}_{vacancy}.txt', 'a', encoding='utf-8') as f:
        # f.write(json.dumps(text, indent=4, ensure_ascii=False))
        f.write(f'{text}\n')

def get_request(url, params, headers):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    return response

def main(vacancy):
    url = 'https://api.hh.ru/vacancies'
    page = 0
    url_parameter = {'text': vacancy, 'area': '1', 'describe_arguments': 'true', 'page': page}
    headers = {}
    pages = get_request(url, url_parameter, headers).get('pages')
    # works = get_request(url, url_parameter, headers).get('items')
    # print(works)
    # write_json(works, url_parameter)
    # key_skills_dict = collections.defaultdict(int)
    while page < pages:
        url_parameter = {'text': vacancy, 'area': '1', 'describe_arguments': 'true', 'page': page}
        print(page)
        works = get_request(url, url_parameter, headers).get('items')
        for work in works:
            write_json(work, url_parameter)

        page += 1







if __name__ == "__main__":
    vacancy = 'sql разработчик'
    main(vacancy)