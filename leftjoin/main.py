import sqlite3 as sl
import pandas as pd





# queries = pd.read_csv('hh_data.csv')
client = sl.connect('my-test.db')
cursorObj = client.cursor()
# with con:
#     con.execute("""
#         CREATE TABLE USER (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             age INTEGER
#         );
#     """)
#

# sql = 'INSERT INTO USER ( name, age) values( ?, ?)'
# data = [
#     ( 'Alice', 21),
#     ( 'Bob', 22),
#     ( 'Chris', 23)
# ]
# with client:
#     client.executemany(sql, data)



tuple_to_inserts = [
('2023-02-20 16:55:03', '"Marketing Analyst" OR "Маркетинговый аналитик"', 'Профессия', 'Линейный специалист', 'Analytics', '76234631', 0, 0, '', 'Москва', 'улица Авиаконструктора Микояна', '12', '', 55.792589, 37.527588, 'Москва, улица Авиаконструктора Микояна, 12', '[{"station_name": "Аэропорт", "line_name": "Замоскворецкая", "station_id": "2.12", "line_id": "2", "lat": 55.800441, "lng": 37.530477}]', 'https://hh.ru/vacancy/76234631', 'https://hh.ru/applicant/vacancy_response?vacancyId=76234631', '', '', 'cast(Null as Nullable(UInt64))', 'cast(Null as Nullable(UInt64))', '', 'cast(Null as Nullable(UInt8))', 'Senior Marketing Analyst', 'cast(Null as Nullable(UInt64))', '', 'https://api.hh.ru/areas/1', '1', 'Москва', 'https://api.hh.ru/vacancies/76234631?host=hh.ru', '2023-02-20 13:45:01', 'https://api.hh.ru/employers/83639', 'https://hh.ru/employer/83639', 'https://hhcdn.ru/employer-logo/3788287.png', 'https://hhcdn.ru/employer-logo/3788288.png', 'https://hhcdn.ru/employer-logo-original/836851.png', 'Профи (profi.ru)', '83639', 0, 'open', 'Открытая', 0, 'remote'),
('2023-02-20 17:47:29', '"Marketing Analyst" OR "Маркетинговый аналитик"', 'Профессия', 'Линейный специалист', 'Analytics', '76592136', 0, 0, '', '', '', '', '', '', '', '', '', 'https://hh.ru/vacancy/76592136', 'https://hh.ru/applicant/vacancy_response?vacancyId=76592136', '', '', 'cast(Null as Nullable(UInt64))', 'cast(Null as Nullable(UInt64))', '', 'cast(Null as Nullable(UInt8))', 'Product Marketing Manager (E-Learning)', 'cast(Null as Nullable(UInt64))', '', 'https://api.hh.ru/areas/1', '1', 'Москва', 'https://api.hh.ru/vacancies/76592136?host=hh.ru', '2023-02-03 12:54:54', 'https://api.hh.ru/employers/5744540', 'https://hh.ru/employer/5744540', 'https://hhcdn.ru/employer-logo/5642196.png', 'https://hhcdn.ru/employer-logo/5642197.png', 'https://hhcdn.ru/employer-logo-original/1005354.png', 'Онлайн-школа Фоксфорд', '5744540', 0, 'open', 'Открытая', 0, 'fullDay')
,('2023-02-20 17:47:29', '"Marketing Analyst" OR "Маркетинговый аналитик"', 'Профессия', 'Линейный специалист', 'Analytics', '76607050', 0, 0, '', 'Москва', 'улица Ленинская Слобода', '26', '', 55.710129, 37.65461, 'Москва, улица Ленинская Слобода, 26', '[{"station_name": "Автозаводская", "line_name": "Замоскворецкая", "station_id": "2.2", "line_id": "2", "lat": 55.706634, "lng": 37.657008}]', 'https://hh.ru/vacancy/76607050', 'https://hh.ru/applicant/vacancy_response?vacancyId=76607050', '', '', 'cast(Null as Nullable(UInt64))', 'cast(Null as Nullable(UInt64))', '', 'cast(Null as Nullable(UInt8))', 'Product / Growth Marketing Manager', 'cast(Null as Nullable(UInt64))', '', 'https://api.hh.ru/areas/1', '1', 'Москва', 'https://api.hh.ru/vacancies/76607050?host=hh.ru', '2023-02-03 17:06:45', 'https://api.hh.ru/employers/3335742', 'https://hh.ru/employer/3335742', 'https://hhcdn.ru/employer-logo/2498948.png', 'https://hhcdn.ru/employer-logo/2498949.png', 'https://hhcdn.ru/employer-logo-original/514340.png', 'Образовательные инновации', '3335742', 0, 'open', 'Открытая', 0, 'fullDay')]

cursorObj.execute('delete from vacancies_short')
client.commit()
# for i in tuple_to_inserts:
#     print(i[0])
#     cursorObj.execute(f'INSERT INTO vacancies_short VALUES {i}')

# data = client.execute("SELECT count(1) FROM vacancies_short ")
# print(data.fetchall())
# client.commit()

# client.execute('delete from vacancies_short')




# with client:
# data = client.execute("SELECT * FROM vacancies_short ") #vacancies_short
# data = client.execute(
#     f"SELECT count(1) FROM vacancies_short WHERE vacancy_id={1} AND query_string='{'fff'}'")
# print(data.fetchall())
# for row in data:
#     print(row)






# CREATE TABLE headhunter.vacancies_short
# (
#     `added_at` DateTime,
#     `query_string` String,
#     `type` String,
#     `level` String,
#     `direction` String,
#     `vacancy_id` UInt64,
#     `premium` UInt8,
#     `has_test` UInt8,
#     `response_url` String,
#     `address_city` String,
#     `address_street` String,
#     `address_building` String,
#     `address_description` String,
#     `address_lat` String,
#     `address_lng` String,
#     `address_raw` String,
#     `address_metro_stations` String,
#     `alternate_url` String,
#     `apply_alternate_url` String,
#     `department_id` String,
#     `department_name` String,
#     `salary_from` Nullable(Float64),
#     `salary_to` Nullable(Float64),
#     `salary_currency` String,
#     `salary_gross` Nullable(UInt8),
#     `name` String,
#     `insider_interview_id` Nullable(UInt64),
#     `insider_interview_url` String,
#     `area_url` String,
#     `area_id` UInt64,
#     `area_name` String,
#     `url` String,
#     `published_at` DateTime,
#     `employer_url` String,
#     `employer_alternate_url` String,
#     `employer_logo_urls_90` String,
#     `employer_logo_urls_240` String,
#     `employer_logo_urls_original` String,
#     `employer_name` String,
#     `employer_id` UInt64,
#     `response_letter_required` UInt8,
#     `type_id` String,
#     `type_name` String,
#     `archived` UInt8,
#     `schedule_id` Nullable(String)
# )
# ENGINE = ReplacingMergeTree
# ORDER BY vacancy_id


