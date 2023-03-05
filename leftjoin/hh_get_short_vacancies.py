import requests
import re
import sqlite3 as sl
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# https://www.cbr-xml-daily.ru/daily_json.js


def check_name(name):
    bad_names = [r'курьер', r'грузчик', r'врач', r'менеджер по закупу',
                 r'менеджер по продажам', r'оператор', r'повар', r'продавец',
                 r'директор магазина', r'директор по продажам', r'директор по маркетингу',
                 r'кабельщик', r'начальник отдела продаж', r'заместитель', r'администратор магазина',
                 r'категорийный', r'аудитор', r'юрист', r'контент', r'супервайзер', r'стажер-ученик',
                 r'су-шеф', r'маркетолог$', r'региональный', r'ревизор', r'экономист', r'ветеринар',
                 r'торговый', r'клиентский', r'начальник цеха', r'территориальный', r'переводчик',
                 r'маркетолог /', r'маркетолог по']
    for item in bad_names:
        if re.match(item, name):
            return True
        
def get_valut(s, v, valutes):
    valute = valutes.get(v, {'Value': 1}).get('Value')
    # print(s, v, valute)
    n = valute.get(v, 1)
    return s*n

def chek_salary(to, fromm, cur):

    s = 0
    if isinstance(to, str) and isinstance(fromm, str):
        return 0
    elif isinstance(to, float|int) and isinstance(fromm, float|int):
        s = (to + fromm) / 2
    elif isinstance(to, float|int) :
        s = to
    elif isinstance(fromm, float|int):
        s = fromm
    if cur == 'RUR' or cur is None:
        return s
    return get_valut(s, cur)

def update_sheet():
    print('Updating cell at', datetime.now())
    columns = []
    # for item in client.execute("SELECT SQL FROM sqlite_master WHERE tbl_name = 'vacancies_short'"):
    for item in client.execute("pragma table_info('vacancies_short')"):
        columns.append(item[0])
    vacancies = client.execute('SELECT * FROM vacancies_short')
    df_vacancies = pd.DataFrame(vacancies, columns=columns)
    df_vacancies.to_csv('vacancies_short.csv', index=False, encoding='utf8')
    content = open('vacancies_short.csv', 'r',  encoding='utf8').read()
    gc.import_csv('1YkMDm2GK7hCvnUDh8NyUDeIofiHxUcFXvrMJvek1vYw', content.encode('utf-8'))


queries = pd.read_csv('hh_data.csv')
con = sl.connect('my-test.db')
client = con.cursor()

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\eduard2\PycharmProjects\hh_project\leftjoin\credentials.json', scope)
gc = gspread.authorize(creds)

url = 'https://www.cbr-xml-daily.ru/daily_json.js'
valutes = requests.get(url).json().get('Valute')
valutes['BYR'] = valutes.get('BYN')

for query_type, level, direction, query_string in zip(queries['Тип'], queries['Уровень'], queries['Направление'],
                                                      queries['Ключевое слово']):
    try:

        url = 'https://api.hh.ru/vacancies'
        par = {'text': query_string, 'per_page': '10', 'page': 0, 'period':2}
        r = requests.get(url, params=par).json()
        added_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pages = r['pages']
        found = r['found']
        vacancies_from_response = []
        print(f'ключевое слово: {query_string}', pages, found)

        for i in range(0, pages + 1):
            par = {'text': query_string, 'per_page': '10', 'page': i}
            r = requests.get(url, params=par).json()
            try:
                vacancies_from_response.append(r['items'])
            except Exception as E:
                continue
        for item in vacancies_from_response:
            print(item)


            for vacancy in item:
                name = vacancy['name'].replace("'", "").replace('"', '')
                if check_name(name):
                    continue

                # try:
                #     ccount = client.execute(
                #         f"SELECT count(1) FROM vacancies_short WHERE (employer_id={vacancy['employer']['id']} AND name='{name}')").fetchall()[
                #         0][0]
                # except Exception as E:
                #     print(f'!!!!! {vacancy}')
                #     continue

                if True: #ccount == 0:

                    vacancy_id = vacancy['id']
                    is_premium = int(vacancy['premium'])
                    has_test = int(vacancy['has_test'])
                    response_url = vacancy['response_url']
                    try:
                        address_city = vacancy['address']['city']
                        address_street = vacancy['address']['street']
                        address_building = vacancy['address']['building']
                        address_description = vacancy['address']['description']
                        address_lat = vacancy['address']['lat']
                        address_lng = vacancy['address']['lng']
                        address_raw = vacancy['address']['raw']
                        address_metro_stations = str(vacancy['address']['metro_stations']).replace("'", '"')
                    except TypeError:
                        address_city = ""
                        address_street = ""
                        address_building = ""
                        address_description = ""
                        address_lat = ""
                        address_lng = ""
                        address_raw = ""
                        address_metro_stations = ""
                    alternate_url = vacancy['alternate_url']
                    apply_alternate_url = vacancy['apply_alternate_url']
                    try:
                        department_id = vacancy['department']['id']
                    except TypeError as E:
                        department_id = ""
                    try:
                        department_name = vacancy['department']['name']
                    except TypeError as E:
                        department_name = ""
                    try:
                        salary_from = vacancy['salary']['from']
                    except TypeError as E:
                        salary_from = ""
                    try:
                        salary_to = vacancy['salary']['to']
                    except TypeError as E:
                        salary_to = ""



                    try:
                        salary_currency = vacancy['salary']['currency']
                        if salary_currency == 'RUR' and salary_from < 15000:
                            continue
                    except TypeError as E:
                        salary_currency = ""
                    try:
                        salary_gross = int(vacancy['salary']['gross'])
                    except TypeError as E:
                        salary_gross = ""
                    try:
                        if vacancy['salary'] is not None:
                            avg_solary = chek_salary(salary_to, salary_from, salary_currency)
                        else:
                            avg_solary = ""
                    except TypeError as E:
                        avg_solary = ""
                    try:
                        insider_interview_id = vacancy['insider_interview']['id']
                    except TypeError:
                        insider_interview_id = ""
                    try:
                        insider_interview_url = vacancy['insider_interview']['url']
                    except TypeError:
                        insider_interview_url = ""
                    area_url = vacancy['area']['url']
                    area_id = vacancy['area']['id']
                    area_name = vacancy['area']['name']
                    url = vacancy['url']
                    published_at = vacancy['published_at']
                    published_at = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%S%z').strftime(
                        '%Y-%m-%d %H:%M:%S')
                    try:
                        employer_url = vacancy['employer']['url']
                    except Exception as E:
                        print(E)
                        employer_url = ""
                    try:
                        employer_alternate_url = vacancy['employer']['alternate_url']
                    except Exception as E:
                        print(E)
                        employer_alternate_url = ""
                    try:
                        employer_logo_urls_90 = vacancy['employer']['logo_urls']['90']
                        employer_logo_urls_240 = vacancy['employer']['logo_urls']['240']
                        employer_logo_urls_original = vacancy['employer']['logo_urls']['original']
                    except Exception as E:
                        print(E)
                        employer_logo_urls_90 = ""
                        employer_logo_urls_240 = ""
                        employer_logo_urls_original = ""
                    employer_name = vacancy['employer']['name'].replace("'", "").replace('"', '')
                    try:
                        employer_id = vacancy['employer']['id']
                    except Exception as E:
                        print(E)
                    response_letter_required = int(vacancy['response_letter_required'])
                    type_id = vacancy['type']['id']
                    type_name = vacancy['type']['name']
                    is_archived = int(vacancy['archived'])
                    if is_archived == 1:
                        continue
                    try:
                        schedule = vacancy['schedule']['id']
                    except Exception as E:
                        print(E)
                        schedule = None
                    if schedule == 'flyInFlyOut':
                        continue
                    
                    vacancies_short_list = [added_at, query_string, query_type, level, direction, vacancy_id,
                                            is_premium, has_test, response_url, address_city, address_street,
                                            address_building, address_description, address_lat, address_lng,
                                            address_raw, address_metro_stations,
                                            alternate_url, apply_alternate_url, department_id, department_name,
                                            salary_from, salary_to, salary_currency, salary_gross, name,
                                            insider_interview_id, insider_interview_url, area_url, area_id,
                                            area_name, url, published_at, employer_url, employer_alternate_url,
                                            employer_logo_urls_90, employer_logo_urls_240,
                                            employer_logo_urls_original,
                                            employer_name, employer_id, response_letter_required, type_id,
                                            type_name, is_archived, schedule, avg_solary]
                    for index, item in enumerate(vacancies_short_list):
                        if item is None:
                            vacancies_short_list[index] = ""
                    tuple_to_insert = tuple(vacancies_short_list)
                    # print(vacancies_short_list)

                    client.execute(f'INSERT INTO vacancies_short VALUES {tuple_to_insert}')
                    con.commit()
                    data = client.execute("SELECT count(1) FROM vacancies_short ")
                    print(data.fetchall())
    except Exception as E:
        print(f'!!!!!### {E}')
        continue

update_sheet()
