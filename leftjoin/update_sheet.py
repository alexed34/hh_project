import sqlite3 as sl
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
# from clickhouse_driver import Client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# client = Client(host='', user='default', password='', port='9000', database='')
con = sl.connect('my-test.db')
client = con.cursor()
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\eduard2\PycharmProjects\hh_project\leftjoin\credentials.json', scope)
gc = gspread.authorize(creds)

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

update_sheet()
# schedule.every().day.at("11:11").do(update_sheet)
# while True:
#     schedule.run_pending()
