
#
import calendar

import pymysql
#
cnx = pymysql.Connect(host="10.73.200.200", user="yassine", password="1234@@it.", database="QM")
cur = cnx.cursor()

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

# l = {'callReason': '4', 'user': 1, 'agent': '3', 'date': '17-11-2021', 'qlf': [{'2': {'ans': '1.0', 'note': 'asdasdasd'}}, {'3': {'ans': '2.0', 'note': 'asdasdasd'}}]}
# #
# [print(i[[j for j in i.keys()][0]]["ans"]) for i in l["qlf"]]


#
# cur.execute(f'''select concat(a.fname, " ", a.lname), cr.reason, u.fullname, qq.calldate, qq.qdate, qq.id from agents a
#                     inner join qualification qq on qq.idagent = a.id
#                     inner join users u on qq.iduser = u.id
#                     inner join callReasons cr on qq.reason = cr.id;
# ''')
#
# data = [[c for c in r] for r in cur.fetchall()]
# for i in data:
#     print(i)
#     cur.execute(f'''select q.qname, q.ranger, r.r, r.note from rslt r inner join qalif q on r.idq = q.id where r.idqlf = {i[-1]}''')
#     dt = [[c for c in r] for r in cur.fetchall()]
#     [print(i) for i in dt]
#     print("#"*200)
#
#
#
# cnx.close()
# data = {}
# with open("clms.txt", "r") as f :
#     ll = [i.replace("\n", "") for i in f.readlines()]
#
# for n,i in enumerate(ll):
#     data[i] = f""


def extraction():
    cur = cnx.cursor()
    extractionsData = []

    cur.execute(f'''select concat(a.fname, " ", a.lname), cr.reason, u.fullname, qq.calldate, qq.qdate, qq.accountNumber, qq.phoneNumber, qq.callLen, qq.id from agents a 
                        inner join qualification qq on qq.idagent = a.id 
                        inner join users u on qq.iduser = u.id 
                        inner join callReasons cr on qq.reason = cr.id;
    ''')
    data = [[c for c in r] for r in cur.fetchall()]
    for i in data:
        disct = {'Qualification ID': '',
                 'Employee Name': '',
                 'Call reason': '',
                 'QM Officer': '',
                 'Call Date': '',
                 'Evaluation Month': '',
                 'Evaluation date': '',
                 'Percentage Saccom': '',
                 'Account number': '',
                 'Phone Number': '',
                 'Call length': '',
                 'Proper Greeting (Yes/No)': '',
                 "Restate Customer's Needs (Yes/Some/No)": '',
                 'Show genuine Empathy (Yes/Some/No)': '',
                 'Show ownership To client (Yes/Some/No)': '',
                 "Verified Customer's vital information (Yes/Some/No)": '',
                 'Confirm Email (use as a security question?) (Yes/No)': '',
                 "Reconfirm Customer's Call back number (Yes/No)": '',
                 "Understanding Client's current situation from Salesforce": '',
                 'Permission to proceed with questions*(Yes/No)': '',
                 'Ask good relevant questions (Yes/Some/No)': '',
                 'Transition and probing for needs* (Yes/No)': '',
                 'Present a Solution (Yes/Some/No)': '',
                 'Present added value (upselling)* (Yes/No)': '',
                 'overcoming rejection (Rejection to their solution) (Yes/No)': '',
                 'Summarize Actions during call (Yes/Some/No)': '',
                 'Reaffirm with client choice or solution (Yes/No)': '',
                 'End call with appreciation for customer loyality/sincere close (Yes/Some/No)': '',
                 'Clear and Accurate documentation with concise notes (Yes/Some/No)': '',
                 'Accurate information provided': '',
                 'All details pretained were provided - points to mention, Dates times and next steps': '',
                 'Adhere to eligibility and policy details (Yes/Some/No)': '',
                 'All Transactions were completed accurately and following correct process': '',
                 'Proper Tone (Yes/No)': '', 'Following Best practice guidlines for hold and mute* (Yes/No)': '',
                 'Following best practice guidlines for transfer call (Yes/No)': '',
                 'Total Gain': '',
                 'Total Eligible': '',
                 'TOTAL': '',
                 'Note': ''}
        disct["Qualification ID"] = i[-1]
        disct["Employee Name"] = i[0]
        disct["Call reason"] = i[1]
        disct["QM Officer"] = i[2]
        disct["Call Date"] = i[3]
        disct["Evaluation Month"] = calendar.month_name[int(str(i[4]).split('-')[1])]
        disct["Evaluation date"] = i[4]
        disct["Account number"] = i[5]
        disct["Phone Number"] = i[6]
        disct["Call length"] = i[7]
        cur.execute(
            f'''select q.qname, q.ranger, r.r, r.note from rslt r inner join qalif q on r.idq = q.id where r.idqlf = {i[-1]}''')
        ttlNote = ""
        ttGain = 0
        ttElj = 0
        rts = [[c for c in r] for r in cur.fetchall()]
        for j in rts:
            disct[j[0]] = j[2]
            ttlNote += f"{j[3]} , " if j[3] else ''
            ttGain += float(j[2])
            ttElj += float(str(j[1]).split(".")[1])
        disct["Note"] = ttlNote
        disct["Total Gain"] = ttGain
        disct["Total Eligible"] = ttElj
        disct["Percentage Saccom"] = (ttGain / ttElj) * 100
        extractionsData.append(disct)

    cnx.close()

    print(extractionsData)


extraction()