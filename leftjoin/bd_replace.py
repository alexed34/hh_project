import sqlite3 as sl





con = sl.connect('my-test.db')
client = con.cursor()
columns = []
for item in client.execute("pragma table_info('vacancies_short2')"):
    columns.append(item[0])
    print(item)

# vacancy_id = client.execute("SELECT  vacancy_id FROM vacancies_short2 ")
#
# vacancy_id = vacancy_id.fetchall()
# data = []
# for id in vacancy_id[:5]:
#     print(type(id[0]))
#     data.append(id[0])
# print(data)


# for i in data:
    # i = i + (0,)
    # # print(i)
    # # print(tuple(i))
    # if i[5] not in id_vacansy:
    #     client.execute(f'INSERT INTO vacancies_short2 VALUES {i}')
    #     id_vacansy.append(i[5])
# con.commit()