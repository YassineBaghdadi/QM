#
#
# import pymysql
#
# cnx = pymysql.Connect(host="10.73.200.200", user="yassine", password="1234@@it.", database="QM")
# cur = cnx.cursor()
#
#
# with open("callREasons.txt", "r") as f:
#     qls = [i.replace('\n', '') for i in f.readlines()]
# qls = [i for i in set(qls)]
# for i in qls:
#     if i:
#         cur.execute(f"""insert into callReasons(reason)values("{str(i)}")""")
#         cnx.commit()
#
#
# cnx.close()


#
l = {'callReason': '4', 'user': 1, 'agent': '3', 'date': '17-11-2021', 'qlf': [{'2': {'ans': '1.0', 'note': 'asdasdasd'}}, {'3': {'ans': '2.0', 'note': 'asdasdasd'}}]}

for i in l["qlf"]:
    for k in i.keys():
        print(k)
