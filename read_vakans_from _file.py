import collections



def read_json(patch):
    data_check = collections.defaultdict(list)
    id_vacansy = []
    id_vacansy_bed = []
    with open(f'{patch}', 'r', encoding='utf-8') as f:
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




vakans = read_json('w_data_2022-12-03_sql_разработчик.txt')
print(len(vakans))

