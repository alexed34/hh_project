import json


def read_json(patch):
    with open(f'{patch}', 'r', encoding='utf-8') as f:
        text = f.readlines()
        for i in text:
            dd = json.loads(i)
            # id = dd.get('id')
            print(dd)
    return text


read_json('w_data_2022-12-03_sql_разработчик.txt')