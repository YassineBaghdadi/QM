
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
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QComboBox, QMainWindow, QWidget, QVBoxLayout, QApplication, QLineEdit, QListWidget, \
    QCheckBox, QListWidgetItem

l = {'callReason': '4', 'user': 1, 'agent': '3', 'date': '17-11-2021', 'qlf': [{'2': {'ans': '1.0', 'note': 'asdasdasd'}}, {'3': {'ans': '2.0', 'note': 'asdasdasd'}}]}
#
[print(i[[j for j in i.keys()][0]]["ans"]) for i in l["qlf"]]



