import itertools
import math
import random
import time

import requests
import re
import sqlite3 as sl
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import datetime


def check_name(name):
    bad_names = [r'курьер', r'грузчик', r'врач', r'менеджер по закупу',
                 r'менеджер по продажам', r'оператор', r'повар', r'продавец',
                 r'директор магазина', r'директор по продажам', r'директор по маркетингу',
                 r'кабельщик', r'начальник отдела продаж', r'заместитель', r'администратор магазина',
                 r'категорийный', r'аудитор', r'юрист', r'контент', r'супервайзер', r'стажер-ученик',
                 r'су-шеф', r'маркетолог$', r'региональный', r'ревизор', r'экономист', r'ветеринар',
                 r'торговый', r'клиентский', r'начальник цеха', r'территориальный', r'переводчик',
                 r'маркетолог /', r'маркетолог по', r'Лаборант', r'химик',  r'лаборант', r'медсес', r'медбра' , r'хроматографи'
                 , r'педагог']
    for item in bad_names:
        if re.search(item, name):
            return True


def get_valut(s, v, valutes):
    valute = valutes.get(v, {'Value': 1}).get('Value')
    n = valute.get(v, 1)
    return s * n


def chek_salary(to, fromm, cur):
    s = 0
    if isinstance(to, str) and isinstance(fromm, str):
        return 0
    elif isinstance(to, float | int) and isinstance(fromm, float | int):
        s = (to + fromm) / 2
    elif isinstance(to, float | int):
        s = to
    elif isinstance(fromm, float | int):
        s = fromm
    if cur == 'RUR' or cur is None:
        return int(s)
    return get_valut(int(s), cur)


def update_sheet():
    print('Updating cell at', datetime.datetime.now())
    columns = []
    for item in client.execute("pragma table_info('vacancies_short')"):
        columns.append(item[1])
    vacancies = client.execute('SELECT * FROM vacancies_short')
    df_vacancies = pd.DataFrame(vacancies, columns=columns)
    df_vacancies.to_csv('vacancies_short.csv', index=False, encoding='utf8')
    content = open('vacancies_short.csv', 'r', encoding='utf8').read()
    gc.import_csv('1YkMDm2GK7hCvnUDh8NyUDeIofiHxUcFXvrMJvek1vYw', content.encode('utf-8'))




def get_vacansys_add():
    vacancy_id = client.execute("SELECT  vacancy_id FROM vacancies_short")
    data = []
    for id in vacancy_id:
        data.append(id[0])
    return data


def add_data_sqlite(tuple_to_insert):
    client.execute(f'INSERT INTO vacancies_short VALUES {tuple_to_insert}')
    con.commit()
    # data = client.execute("SELECT count(1) FROM vacancies_short ")
    # print(data.fetchall())


def update_data_sql(ti, vacancy_id):
    n = ti[49]
    if not isinstance(n, int):
        n = 0
    print(n, vacancy_id )
    client.execute(f"UPDATE vacancies_short SET counters = {n} where vacancy_id = '{vacancy_id}'")
                   # f"requirement = '{ti[47]}', "
                   # f"schedule_name = '{ti[48]}', "
                   # f"counters = {ti[49]}, "
                   # f"professional_roles = '{ti[50]}', "
                   # f"working_days = '{ti[51]}', "
                   # f"working_time_intervals = '{ti[52]}', "
                   # f"working_time_modes = '{ti[53]}' "
                   # f"where vacancy_id = '{vacancy_id} '")
    con.commit()
    # print(vacancy_id)


def get_vacansis(query_string, experience):
    url = 'https://api.hh.ru/vacancies'
    par = {'text': query_string, 'premium':'true', 'responses_count_enabled':'true', 'per_page': '100', 'page': 0,
           'period': 3, 'experience': experience}
    r = requests.get(url, params=par).json()
    if r.get('errors') is not None:
        print('https://hh.ru/account/captcha?state=pxvcxBozfu7ry7R4QCetFpRgByk-d8c77C_TwpAbKNKURyNV7jIN3ZmLkwVMlGAXc_sfWHbRBT2JhAGcYUh8AEYZdathULSPsW--Ekq31x68gKH8DWjKYPhjmpARJAgP&backurl=http://eledia.rul')
        exit()


    pages = r['pages']
    found = r['found']
    vacancies_from_response = []

    if found == 0:
        print('нет данных')
        return None
    date_now = datetime.datetime.now().date()
    date_from = date_now - datetime.timedelta(days=1)
    date_to = datetime.datetime.now().date()
    for day in range(math.ceil(found/2000)):
        date_from += datetime.timedelta(days=day)
        date_to += datetime.timedelta(days=day)
        print(pages, found, experience, query_string, day, date_from, date_to)
        for i in range(0, pages + 1):
            par = {'text': query_string, 'experience': experience, 'page': i, 'date_from': date_from.strftime('%Y-%m-%d'),
                   'date_to': date_to.strftime('%Y-%m-%d'),
                   'premium':'true', 'responses_count_enabled':'true', 'per_page': '100'
                   }

            r = requests.get(url, params=par).json()
            # time.sleep(random.randint(1,4))

            try:
                vacancies_from_response.append(r['items'])
            except Exception as E:
                print(E,r,1)
    return vacancies_from_response

def get_data_vacancies(vacancies_from_response, vacansys_add, query_string):
    added_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for item in vacancies_from_response:
        try:
            for vacancy in item:
                name = vacancy['name'].replace("'", "").replace('"', '')
                vacancy_id = int(vacancy['id'])
                exp = 0
                if experience == 'noExperience':
                    exp = 1
                elif experience == 'between1And3':
                    exp = 2
                elif experience == 'between3And6':
                    exp = 3
                elif experience == 'moreThan6':
                    exp = 4
                try:
                    employer_id = vacancy['employer']['id']
                except Exception as E:
                    print(E,2)

                if check_name(name.lower()):
                    continue

                try:
                    ccount = client.execute(
                        f"SELECT count(1) FROM vacancies_short WHERE (employer_id={employer_id} AND name='{name}')").fetchall()[
                        0][0]
                except Exception as E:
                    print(f'!!!!! {vacancy}',3)

                if ccount == 0:
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
                    published_at = datetime.datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%S%z').strftime(
                        '%Y-%m-%d %H:%M:%S')
                    try:
                        employer_url = vacancy['employer']['url']
                    except Exception as E:
                        # print(E)
                        employer_url = ""
                    try:
                        employer_alternate_url = vacancy['employer']['alternate_url']
                    except Exception as E:
                        # print(E)
                        employer_alternate_url = ""
                    try:
                        employer_logo_urls_90 = vacancy['employer']['logo_urls']['90']
                        employer_logo_urls_240 = vacancy['employer']['logo_urls']['240']
                        employer_logo_urls_original = vacancy['employer']['logo_urls']['original']
                    except Exception as E:
                        # print(E)
                        employer_logo_urls_90 = ""
                        employer_logo_urls_240 = ""
                        employer_logo_urls_original = ""
                    employer_name = vacancy['employer']['name'].replace("'", "").replace('"', '')

                    response_letter_required = int(vacancy['response_letter_required'])
                    type_id = vacancy['type']['id']
                    type_name = vacancy['type']['name']
                    is_archived = int(vacancy['archived'])
                    if is_archived == 1:
                        continue
                    try:
                        schedule = vacancy['schedule']['id']
                    except Exception as E:
                        schedule = None
                    if schedule == 'flyInFlyOut':
                        continue
                    try:
                        requirement = vacancy['snippet']['requirement']
                    except Exception as E:
                        requirement = ''
                    try:
                        schedule_name = vacancy['schedule']['name']
                    except Exception as E:
                        schedule_name = ''
                    try:
                        counters = vacancy['counters']['responses']
                    except Exception as E:
                        counters = 0
                    try:
                        professional_roles = vacancy['professional_roles'][0]['name']
                    except Exception as E:
                        professional_roles = ' '
                    try:
                        working_days = vacancy['working_days'][0]['name']
                    except Exception as E:
                        working_days = ' '
                    try:
                        working_time_intervals = vacancy['working_time_intervals'][0]['name']
                    except Exception as E:
                        working_time_intervals = ' '
                    try:
                        working_time_modes = vacancy['working_time_modes'][0]['name']
                    except Exception as E:
                        working_time_modes = ' '

                    vacancies_short_list = [added_at, query_string, vacancy_id,
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
                                            type_name, is_archived, schedule, avg_solary, exp, requirement,
                                            schedule_name, counters, professional_roles, working_days,
                                            working_time_intervals, working_time_modes]
                    # print(1)
                    for index, item in enumerate(vacancies_short_list):
                        if item is None:
                            vacancies_short_list[index] = ""
                    tuple_to_insert = tuple(vacancies_short_list)
                    if vacancy_id in vacansys_add:
                        # continue
                        # print(0)
                        update_data_sql(tuple_to_insert, vacancy_id)
                        print(00)
                    else:
                        add_data_sqlite(tuple_to_insert)
                        print(name,44)
        except Exception as E:
            print(f'!!!!!### {E}',5)





if __name__ == "__main__":
    con = sl.connect('my-test.db')
    client = con.cursor()

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        r'C:\Users\eduard2\PycharmProjects\hh_project\leftjoin\credentials.json', scope)
    gc = gspread.authorize(creds)

    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    valutes = requests.get(url).json().get('Valute')
    valutes['BYR'] = valutes.get('BYN')
    vacansys_add = get_vacansys_add()

    query_strings = ['NAME:анали*', 'NAME:analis*' ,'NAME:!BI', 'NAME:analys*' ,'NAME:!datalens', 'NAME:!Tableau', 'NAME:Qlik*']
    experience =  ['noExperience', 'between1And3', 'between3And6', 'moreThan6']
    all_found = list(itertools.product(query_strings, experience))

    for point in list(itertools.product(query_strings, experience))[1:]:
        query_string = point[0]
        experience = point[1]
        vacancies_from_response = get_vacansis(query_string, experience)
        time.sleep(random.randint(1,4))
        if vacancies_from_response is None:
            continue
        get_data_vacancies(vacancies_from_response, vacansys_add, query_string)
    update_sheet()
