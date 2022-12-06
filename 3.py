import collections


data_check = collections.defaultdict(list)
id_vacansy = []
id_vacansy_2 = []
def read_json(patch):
    with open(f'{patch}', 'r', encoding='utf-8') as f:
        text = f.readlines()
    for i in text:
        a = eval(i)
        id_emploer = a.get('employer').get('id')
        name_vacansy = a.get('name')
        # print(data_check.get(id_emploer))
        if data_check.get(id_emploer) is None or name_vacansy not in data_check.get(id_emploer):
            id_vacansy.append(a.get('id'))
            data_check[id_emploer].append(name_vacansy)
        elif name_vacansy in data_check.get(id_emploer):
            id_vacansy_2.append(a.get('id'))


    print(id_vacansy)
    print(id_vacansy_2)
# return text


read_json('w_data_2022-12-03_sql_разработчик.txt')

#
# "{'id': '73121079', 'premium': False, 'name': 'Программист SQL', 'department': None, 'has_test': False, " \
# "'response_letter_required': False, 'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'}, " \
# "'salary': {'from': 160000, 'to': 280000, 'currency': 'RUR', 'gross': True}, 'type': {'id': 'open', 'name': 'Открытая'}," \
# " 'address': None, 'response_url': None, 'sort_point_distance': None, 'published_at': '2022-12-03T10:28:34+0300', " \
# "'created_at': '2022-12-03T10:28:34+0300', 'archived': False, " \
# "'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=73121079', 'insider_interview': None," \
# " 'url': 'https://api.hh.ru/vacancies/73121079?host=hh.ru', " \
# "'adv_response_url': 'https://api.hh.ru/vacancies/73121079/adv_response?host=hh.ru', " \
# "'alternate_url': 'https://hh.ru/vacancy/73121079', 'relations': [], " \
# "'employer': {'id': '839098', 'name': 'Автомакон', 'url': 'https://api.hh.ru/employers/839098'," \
# " 'alternate_url': 'https://hh.ru/employer/839098', 'logo_urls': {'240': 'https://hhcdn.ru/employer-logo/4221269.png'," \
# " '90': 'https://hhcdn.ru/employer-logo/4221268.png', 'original': 'https://hhcdn.ru/employer-logo-original/945183.png'}, " \
# "'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=839098', 'trusted': True}, " \
# "'snippet': {'requirement': 'Опыт разработки <highlighttext>SQL</highlighttext>-запросов для СУБД MS <highlighttext>SQL</highlighttext> Server. " \
# "Написание хранимых процедур, триггеров, функций. Умение пользоваться анализатором запросов. " \
# "', 'responsibility': 'Проектирование таблиц, БД. Написание оптимальных запросов в высоконагруженных " \
# "СУБД для MS <highlighttext>SQL</highlighttext> на языке T-<highlighttext>SQL</highlighttext>. " \
# "Работа с высоконагруженными базами.'}, 'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}," \
# " 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': True}\n"