import firebase_admin
import pymysql, datetime, sys, os, random, string, numpy as np, openpyxl, shutil, calendar
from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QHeaderView
from firebase_admin import credentials, db

CPMS = []
USER = None
HOST = ""

def verifyIP():
    global HOST
    with open("ip.txt", "r") as f:
        ip = f.read()
    try:
        cnx = pymysql.Connect(host="10.73.200.200", user="yassine", password="1234@@it.", database="QM")
        HOST = "10.73.200.200"
        cnx.close()
    except:
        cnx = pymysql.Connect(host=ip, user="yassine", password="1234@@it.", database="QM")

        HOST = ip
        cnx.close()
    finally:

        cred = credentials.Certificate("qmkey.json")
        default_app = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://qmserver-5e178-default-rtdb.firebaseio.com/'
        })
        newip = str(db.reference("ip"))
        with open("ip.txt", "w") as f:
            f.write(newip)

        cnx = pymysql.Connect(host=newip, user="yassine", password="1234@@it.", database="QM")

        HOST = newip
        cnx.close()

def conn():
    return pymysql.Connect(host=HOST, user="yassine", password="1234@@it.", database="QM")





def extraction(self, agents, fdate, tdate ):
    cnx = conn()
    cur = cnx.cursor()
    extractionsData = []
    print(f'agents \n {agents}')

    qq = f'''select concat(a.fname, " ", a.lname), cr.reason, u.fullname, qq.calldate, qq.qdate, qq.accountNumber, qq.phoneNumber, qq.callLen, qq.id from agents a 
                        inner join qualification qq on qq.idagent = a.id 
                        inner join users u on qq.iduser = u.id 
                        inner join callReasons cr on qq.reason = cr.id where a.id {f'in {tuple(agents)}' if len(agents) > 1 else f'= {agents[0]}'} and qq.qdate >= "{fdate}" and qq.qdate <= "{tdate}";
    '''
    print(qq)
    cur.execute(qq)

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
        disct["Percentage Saccom"] = f"{round((ttGain / ttElj) * 100, 2)}%"
        extractionsData.append(disct)


    cnx.close()
    # fileName = os.path.join(os.getcwd(), "testExtracion.xlsx")
    fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save file ...", f"Extraxtion{datetime.datetime.today().strftime('%d-%m-%Y %H-%M-%S')}", "Excel Files (*.xlsx)")

    if fileName:
        shutil.copy2(os.path.join(os.getcwd(), "template.xlsx"), fileName)

        wb_obj = openpyxl.load_workbook(fileName)
        sh = wb_obj["ecoute_Saccom"]
        currentR = 3
        for agDict in extractionsData:
            for x, k in enumerate(agDict.keys()):
                cell = sh.cell(row=currentR, column=x+1)
                cell.value = agDict[k]

            currentR += 1
        wb_obj.save(fileName)
        QtWidgets.QMessageBox.about(self, "Extraction Done.", f"the data extracted to : {fileName}")
        os.startfile(fileName)


    print(extractionsData)


class Login(QtWidgets.QWidget):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi(os.path.join(os.getcwd(), 'ui', 'login.ui'), self)
        self.setWindowTitle("Login ...")
        self.label.setPixmap(QtGui.QPixmap('src/img/logo.png'))
        self.label.setScaledContents(True)
        self.camps = None
        self.cnx.clicked.connect(self.login)



    def login(self):
        cnx = conn()
        cur = cnx.cursor()
        try:
            if self.username.text() and self.passwrd.text():
                cur.execute(f'''select cmps from users where username like "{self.username.text()}" and pssword like "{self.passwrd.text()}"''')
                self.camps = cur.fetchone()[0]
                if self.camps:
                    global CPMS
                    CPMS = [i for i in str(self.camps).split(".")]
                    print(f"cmps ; {CPMS}")
                    cur.execute(
                        f'''select id from users where username like "{self.username.text()}" and pssword like "{self.passwrd.text()}"''')
                    global USER
                    USER = cur.fetchone()[0]
                    # self.main = Main()
                    # self.main.show()
                    self.rs = RSLT()
                    self.rs.show()
                    self.close()
                else:
                    self.username.setText("")
                    self.passwrd.setText("")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, f"Log in Failed", f"Invalid data or there is some error : {e}")

        cur.close()
        cnx.close()

#
# class Main(QtWidgets.QWidget):
#     def __init__(self):
#         super(Main, self).__init__()
#         uic.loadUi(os.path.join(os.getcwd(), 'ui', 'main.ui'), self)
#         self.setWindowTitle("HOME")
#         self.results.setFixedSize(150, 150)
#         self.newrec.setFixedSize(150, 150)
#
#         self.results.setPixmap(QtGui.QPixmap('src/img/rslts.png'))
#         self.results.setScaledContents(True)
#         self.results.installEventFilter(self)
#         self.newrec.installEventFilter(self)
#
#         self.newrec.setPixmap(QtGui.QPixmap('src/img/nrcrd.png'))
#         self.newrec.setScaledContents(True)
#
#
#     def eventFilter(self, s, e):
#         if e.type() == QtCore.QEvent.MouseButtonPress:
#             if s is self.results:
#                 self.rss = RSLT()
#                 self.rss.show()
#                 self.close()
#             if s is self.newrec:
#                 self.nr = NewQalif()
#                 self.nr.show()
#                 self.close()
#
#         return super(Main, self).eventFilter(s, e)
#

class RSLT(QtWidgets.QWidget):
    def __init__(self):
        super(RSLT, self).__init__()
        uic.loadUi(os.path.join(os.getcwd(), 'ui', 'rslts.ui'), self)
        self.agents = []
        self.camps = []
        now = datetime.datetime.now()
        self.dateEdit.setDateTime(now)
        cnx = conn()
        cur = cnx.cursor()
        cur.execute(f"""select campname from camps where id {f'in {tuple(CPMS)}' if len(CPMS) > 1 else f'= {CPMS[0]}'}""")
        cc = cur.fetchall()
        self.camps = [i[0] for i in cc] if len(cc) >1 else cc[0]
        # self.agents.insert(0, "choose Agent ...")
        # self.camps.insert(0, "choose Campaign ...")
        print(f'''agents : {self.agents}\ncomps : {self.camps}''')
        self.cm.addItems(self.camps)
        self.cm.currentTextChanged.connect(self.getAgents)
        self.getAgents()
        self.getQlfs()
        self.ag.currentIndexChanged.connect(self.getQlfs )
        self.qlfs.currentIndexChanged.connect(self.refresh )
        self.newR.clicked.connect(self.openNewR)
        self.dateEdit.dateChanged.connect(self.getQlfs)
        # self.refresh()

        cur.close()
        cnx.close()
        self.dwa2.clicked.connect(self.likoliDa2)
        self.dwa2.setEnabled(True)

    # def getQlfs(self):
    #     if self.ag.currentIndex() == 0:
    #         self.newR.setEnabled(False)
    #     else:
    #         self.newR.setEnabled(True)
    #         cnx = conn()
    #         cur = cnx.cursor()
    #         cur.execute(f'''select iden from rslt where qdate like "{self.dateEdit.date().toPyDate().strftime('%d-%m-%Y')}" and idagent = {str(self.ag.currentText()).split("-")[0]}''')
    #         qllls = [i[0] for i in cur.fetchall()]
    #         self.qlfs.clear()
    #         self.qlfs.addItems(qllls)
    #
    #         cnx.close()
    #

    def likoliDa2(self):
        self.HabaSawda = LhabaSawda()
        self.HabaSawda.show()
        self.close()

    def closeEvent(self, event):
        self.lgn = Login()
        self.lgn.close()
        self.close()

    def openNewR(self):
        self.nr = NewQalif(str(self.ag.currentText()).split('-')[0])
        self.nr.show()
        self.close()

    def getQlfs(self):
        cnx = conn()
        cur = cnx.cursor()
        try:

            if self.ag.currentIndex() != 0 and self.ag.isEnabled() and len([i for i in str(self.ag.currentText()).split('-')]):
                self.newR.setEnabled(True)
                self.qlfs.clear()
                q = f"""select id from qualification where idagent = {str(self.ag.currentText()).split('-')[0]} and qdate like '{self.dateEdit.date().toPyDate().strftime('%d-%m-%Y')}'"""
                print(q)
                cur.execute(q)
                c = cur.fetchall()
                if c:
                    print("$"*100)
                    print(c)
                    self.qlf = [f"Qualification ID : {i[0]}" for i in c] if len(c) > 1 else [f"Qualification ID : {c[0][0]}"]
                    print(self.qlf)
                    self.qlfs.setEnabled(True)
                    self.qlfs.addItems(self.qlf)
            else:
                self.newR.setEnabled(False)
                self.qlfs.clear()
                self.qlfs.setEnabled(False)
                self.tableWidget.clear()
        except:...
        self.refresh()
        cur.close()
        cnx.close()

    def getAgents(self):
        cnx = conn()
        cur = cnx.cursor()
        self.ag.setCurrentIndex(0)
        if self.cm.currentIndex() != 0:
            self.ag.clear()
            q =f"""select concat(id, '-', fname, ' ', lname) as fullName from agents where camp = (select id from camps where campname like "{self.cm.currentText()}")"""
            print(q)
            cur.execute(q)
            c = cur.fetchall()
            self.agents = ["choose Agent ..."]+[i[0] for i in c] if len(c) >1 else ["choose Agent ...", c[0][0]]
            # self.agents.insert(0, )
            print("@"*100)
            print(self.agents)
            self.ag.addItems(self.agents)
            self.ag.setEnabled(True)
        else:
            self.ag.clear()
            self.ag.setEnabled(False)

        self.refresh()
        cur.close()
        cnx.close()

    def refresh(self):
        if self.ag.currentText() not in self.agents or self.cm.currentText() not in self.camps :
            self.tableWidget.setEnabled(False)
        else:
            # try:
                if self.ag.currentIndex() != 0 and self.qlfs.currentText():
                    self.tableWidget.setEnabled(True)

                    cnx = conn()
                    cur = cnx.cursor()
                    qq = f"""select q.qname, r.r, r.note from qalif q inner join rslt r on r.idq = q.id inner join qualification qq on r.idqlf = qq.id inner join users u on qq.iduser = u.id where qq.idagent = {str(self.ag.currentText()).split('-')[0]} and qq.id = {str(self.qlfs.currentText()).split(" : ")[1]};"""
                    print(f'{"#"*100}\n{qq}')
                    cur.execute(qq)

                    data = cur.fetchall()
                    print(f"{'@'*100}\n{bool(data)}")
                    if data:

                        print(data)
                        infos = []
                        cur.execute(f'''select r, idq from rslt where idqlf = {str(self.qlfs.currentText()).split(" : ")[1]}''')
                        output = cur.fetchall()
                        allRsltPoints = [float(i[0]) for i in output]
                        # infos.append(allRsltPoints)
                        ttlGain = sum(allRsltPoints)
                        infos.append(ttlGain)
                        allQansewred = [i[1] for i in output]
                        qqr = f'''select ranger from qalif where id{f" in {tuple(allQansewred)}" if len(allQansewred) > 1 else f" = {allQansewred[0]}"}'''
                        print(qqr)
                        cur.execute(qqr)
                        ttlEligible = sum([float(str(i[0]).split(".")[1]) for i in cur.fetchall()])
                        infos.append(ttlEligible)


                        saccomPercentage = f"{str(round((ttlGain/ttlEligible) * 100, 2))}%"
                        infos.append(saccomPercentage)
                        qu = f'''select cr.reason, u.fullname, qq.qdate, qq.calldate, qq.accountNumber, qq.phoneNumber, qq.callLen from callReasons cr inner join qualification qq on qq.reason = cr.id inner join users u on qq.iduser = u.id where qq.id = {str(self.qlfs.currentText()).split(" : ")[1]}'''
                        print(qu)
                        cur.execute(qu)
                        dt = cur.fetchone()
                        reason = dt[0]
                        infos.append(reason)
                        qualifier = dt[1]
                        infos.append(qualifier)
                        date = dt[2]
                        infos.append(date)
                        calldate = dt[3]
                        infos.append(calldate)
                        accN = dt[4]
                        infos.append(accN)
                        phN = dt[5]
                        infos.append(phN)
                        cLen = dt[6]
                        infos.append(cLen)

                        self.tableWidget_2.clear()
                        self.tableWidget_2.setColumnCount(len(infos))
                        self.tableWidget_2.setRowCount(1)
                        self.tableWidget_2.setHorizontalHeaderLabels("Total Gain.Total Eligible.Saccom Percentage.Call Reason.User Qualifier.Qualification Date.Call Date.Account Number.Phone Number.Call length".split('.'))
                        [self.tableWidget_2.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch) for i in range(len(infos))]

                        [self.tableWidget_2.setItem(0,c, QtWidgets.QTableWidgetItem(str(infos[c])))for c in range(len(infos))]


                        self.tableWidget.clear()
                        self.tableWidget.setColumnCount(len(data[0]))
                        self.tableWidget.setRowCount(len(data))
                        self.tableWidget.setHorizontalHeaderLabels("Qualification.Result.Note".split('.'))
                        [self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch) for i in range(len(data[0]))]

                        for r in range(len(data)):
                            for c in range(len(data[0])):
                                self.tableWidget.setItem(r,c, QtWidgets.QTableWidgetItem(str(data[r][c])))
                    else:
                        self.tableWidget.clear()
                    cur.close()
                    cnx.close()
                else:
                    self.tableWidget.clear()
                    self.tableWidget_2.clear()
            # except :
            #         self.tableWidget.clear()
            #         self.tableWidget_2.clear()
            # except Exception as e:
            #     print(e)
            #     self.tableWidget.setEnabled(False)


class NewQalif(QtWidgets.QWidget):
    def __init__(self, agent):
        super(NewQalif, self).__init__()
        uic.loadUi(os.path.join(os.getcwd(), 'ui', 'newqalif.ui'), self)
        self.submit.setEnabled(False)

        self.lbtn.setPixmap(QtGui.QPixmap('src/img/left.png'))
        self.lbtn.setScaledContents(True)
        # self.rbtn.setPixmap(QtGui.QPixmap('src/img/right.png'))
        # self.rbtn.setScaledContents(True)
        self.rbtn.installEventFilter(self)
        self.lbtn.installEventFilter(self)

        self.cnx = conn()
        self.ansers = {}
        self.cur = self.cnx.cursor()
        # self.qid.setText(f'Qualification ID is : -{self.getIden(self.cur)}')
        self.qlfs = []
        self.cur.execute(f'select id, qname from qalif')
        for i in self.cur.fetchall():
            if i[0] not in self.ansers.keys():
                self.qlfs.append("-".join([str(j) for j in i]))
        self.label_3.setText(self.qlfs[0])
        self.agent = agent
        # self.refreshCombo()
        self.save.clicked.connect(self.nextq)
        self.comboBox.currentIndexChanged.connect(lambda : self.startQlf.setEnabled(False if self.comboBox.currentIndex() == 0 else True))
        self.startQlf.clicked.connect(self.startTheQlf)
        self.submit.clicked.connect(self.finish)
        self.pushButton.clicked.connect(self.addReason)
        self.refreshreasons()
        self.refreshQlf()
        self.back.clicked.connect(self.goback)
        now = datetime.datetime.now()
        self.dateEdit.setDateTime(now)


    def closeEvent(self, event):
        self.goback()

    def goback(self):
        self.rslt = RSLT()
        self.rslt.show()
        self.close()


    def eventFilter(self, s, e):
        if e.type() == QtCore.QEvent.MouseButtonPress:
            if s is self.rbtn:

                currentIndx = int(self.qlfs.index(str(self.label_3.text())))
                if currentIndx != len(self.qlfs)-1:
                    self.label_3.setText(self.qlfs[currentIndx + 1])
                    self.refreshQlf()

            if s is self.lbtn:

                currentIndx = int(self.qlfs.index(str(self.label_3.text())))
                if currentIndx != 0:
                    self.label_3.setText(self.qlfs[currentIndx - 1])
                    self.refreshQlf()
        if e.type() == QtCore.QEvent.MouseButtonDblClick:

            if s is self.rbtn:

                currentIndx = int(self.qlfs.index(str(self.label_3.text())))
                self.label_3.setText(self.qlfs[-1])
                self.refreshQlf()

            if s is self.lbtn:

                currentIndx = int(self.qlfs.index(str(self.label_3.text())))
                self.label_3.setText(self.qlfs[0])
                self.refreshQlf()


        return super(NewQalif, self).eventFilter(s, e)


    def refreshQlf(self):

        self.cur.execute(f'select ranger from qalif where id like {str(self.label_3.text()).split("-")[0]}')

        theRange = [int(i) for i in str(self.cur.fetchone()[0]).split('.')]
        items = [str(i) for i in np.arange(theRange[0], theRange[1]+0.5, 0.5)]
        self.comboBox_2.clear()
        self.comboBox_2.addItems(items)
        if "qlf" in self.ansers:

            if  any(str(self.label_3.text()).split("-")[0] in i for i in self.ansers["qlf"]):
                # self.comboBox_2.setCurrentIndex(items.index(self.ansers["qlf"][self.ansers["qlf"].index(str(self.label_3.text()).split("-")[0])]["ans"]))
                for i in self.ansers["qlf"]:
                    for k in i.keys():
                        if k == str(self.label_3.text()).split("-")[0]:
                            self.label_2.setText("(saved)")
                            self.comboBox_2.setCurrentIndex(items.index(i[k]["ans"]))
                            self.textEdit.setPlainText(i[k]["note"])
                        else:
                            self.label_2.setText("")


                # self.textEdit.setPlainText(self.ansers["qlf"][str(self.label_3.text()).split("-")[0]]["note"])
            else:
                self.comboBox_2.setCurrentIndex(items.index("0.0"))
                self.textEdit.setPlainText("")
                self.label_2.setText("")

        self.submit.setEnabled(True if 'qlf' in self.ansers else False)


    def addReason(self):
        r, d =QtWidgets.QInputDialog.getText(
             self, 'Add new reason to database', 'Enter the new Call Reason :')
        if d:
            print(r)

        if d:
            if r:
                self.cur.execute(f'select count(id) from callReasons where reason like "{str(r).strip()}"')
                rr = self.cur.fetchone()[0]
                if not rr:
                        self.cur.execute(f'''insert into callReasons(reason) value("{str(r).strip()}")''')
                        self.cnx.commit()
                        self.refreshreasons(c=True)
                else:
                    QtWidgets.QMessageBox.about(self, "Failed to add :", "This Reason already exists.")
            else:
                    QtWidgets.QMessageBox.about(self, "Failed to add :", "Invalid input")


    def refreshreasons(self, c = None):
        self.comboBox.clear()
        self.cur.execute(f'''select concat(id, "-", reason) from callReasons''')
        items = ["Call Reason ..."]+[i[0] for i in self.cur.fetchall()]
        self.comboBox.addItems(items)
        if c:
            self.comboBox.setCurrentIndex(len(items)-1)

    def startTheQlf(self):
        self.ansers["callReason"] = str(self.comboBox.currentText()).split("-")[0]
        self.ansers["user"] = USER
        self.ansers["agent"] = self.agent
        self.ansers["date"] = datetime.datetime.today().strftime('%d-%m-%Y')
        self.ansers["calldate"] = self.dateEdit.date().toPyDate().strftime('%d-%m-%Y')
        self.ansers["accountNumber"] = self.accN.text()
        self.ansers["phone"] = self.PhN.text()
        self.ansers["calllen"] = self.CN.text()
        self.ansers["qlf"] = []





        self.widget.setEnabled(True)
        self.widget_2.setEnabled(False)


    #
    # def refreshCombo(self):
    #
    #     if self.ql.currentIndex() != 0:
    #         self.cur.execute(f'select id, ranger from qalif where qname like "{self.ql.currentText()}"')
    #         data = self.cur.fetchone()
    #         self.currentQlId = data[0]
    #         theRange = [int(i) for i in str(data[1]).split('.')]
    #         items = [str(i) for i in np.arange(theRange[0], theRange[1]+0.5, 0.5)]
    #         self.ansr.clear()
    #         self.ansr.addItems(items)
    #
    #         try :
    #             self.ansr.setCurrentIndex(items.index(self.ansers["qlf"][self.currentQlId]["ans"]))
    #             self.textEdit.setPlainText(self.ansers["qlf"][self.currentQlId]["n"])
    #         except:...
    #
    #     self.submit.setEnabled(True) if "qlf" in self.ansers else ...
    #     self.next.setEnabled(False) if self.ql.currentIndex() == 0 else self.next.setEnabled(True)


    def nextq(self):

        qlfID = str(self.label_3.text()).split("-")[0]
        savedAns = [[k for k in  i.keys()][0] for i in self.ansers["qlf"]]
        if qlfID not in savedAns:
            self.ansers["qlf"].append(
                {qlfID: {"ans": self.comboBox_2.currentText(), "note": self.textEdit.toPlainText(), }})
        else:
            self.ansers["qlf"][savedAns.index(qlfID)][qlfID] = {"ans": self.comboBox_2.currentText(), "note": self.textEdit.toPlainText(), }

        print([[k for k in  i.keys()][0] for i in self.ansers["qlf"]])
        print(self.ansers)
        currentIndx = int(self.qlfs.index(str(self.label_3.text())))
        if currentIndx != len(self.qlfs) - 1:
            self.label_3.setText(self.qlfs[currentIndx + 1])
            self.refreshQlf()

    #
    # def getIden(self, cur):
    #     ll = [i for i in string.ascii_lowercase]+ [i for i in string.digits]+ [i for i in string.ascii_uppercase]
    #     # upper = [i for i in string.ascii_uppercase]
    #     # digit = [i for i in string.digits]
    #
    #     iden = ''.join(random.choice(ll) for _ in range(random.randint(7, 20)))
    #
    #     cur.execute(f'''select count(id) from rslt where iden like "{iden}"''')
    #     if cur.fetchone()[0]:
    #         self.getIden(cur)
    #     return iden

    def finish(self):
        print(self.ansers)
        messedQ = []

        self.cur.execute("select id from qalif where important = 1")
        importentQ = [int(i[0]) for i in self.cur.fetchall()]

        ansewred = []
        for q in self.ansers["qlf"]:
            for k in q.keys():
                ansewred.append(int(k))

        for i in importentQ:
            if i not in ansewred:
                messedQ.append(i)

        if messedQ:
            qr = f'select qname from qalif where id in {tuple(messedQ)}'
            self.cur.execute(qr)
            messedQN = [f"{i[0]}\n" for i in self.cur.fetchall()]

            msg = f'''\nthose Qualifications are important to fill :\n {" ".join(messedQN)}'''
            QtWidgets.QMessageBox.about(self, "you have to complete all the important elements ", msg)

        else:
            self.cur.execute(f"""insert into qualification(iduser, idagent, qdate, reason, calldate, accountNumber, phoneNumber, callLen) values(
                        {self.ansers["user"]},
                        {self.ansers["agent"]},
                        "{datetime.datetime.today().strftime('%d-%m-%Y')}",
                        {self.ansers["callReason"]},
                        "{self.ansers["calldate"]}",
                        "{self.ansers["accountNumber"]}",
                        "{self.ansers["phone"]}",
                        "{self.ansers["calllen"]}"
            
            )""")
            self.cnx.commit()
            self.cur.execute(f'''select max(id) from qualification ''')
            qid = self.cur.fetchone()[0]
            for q in self.ansers["qlf"]:
                for k in q.keys():
                    self.cur.execute(f"""insert into rslt(idq, r, idqlf, note) values (
                                {k}, "{q[k]["ans"]}", {qid}, "{q[k]["note"]}"
                        )""")
                    self.cnx.commit()

            QtWidgets.QMessageBox.about(self, "Qualification Saved Successfully ", f"The Qualification save with the ID : {qid}.")
            # self.rsts = RSLT()
            # self.rsts.show()
            self.close()


class LhabaSawda(QtWidgets.QWidget):
    def __init__(self):
        super(LhabaSawda, self).__init__()
        uic.loadUi(os.path.join(os.getcwd(), "ui", "extr.ui"), self)

        now = datetime.datetime.now()
        self.dateEdit.setDateTime(now)
        self.dateEdit_2.setDateTime(now)

        cnx = conn()
        cur = cnx.cursor()
        cur.execute("select concat(id, '-', fname, lname) as agent from agents")
        self.agents = ["Choose Agent ..."]+[i[0] for i in cur.fetchall()]
        # print(self.agents)
        # self.comboBox.addItems(self.agents)
        self.refr()
        self.comboBox.currentIndexChanged.connect(lambda : self.add.setEnabled(False if self.comboBox.currentIndex() == 0 else True))

        self.add.clicked.connect(self.addAg)
        self.addAll.clicked.connect(self.addAllAg)
        self.pushButton_2.clicked.connect(self.extractLkhra)
        self.selectedAgents = []
        cnx.close()
        self.pushButton_3.clicked.connect(self.goback)


    def closeEvent(self, event):
        self.goback()

    def goback(self):
        self.rslt = RSLT()
        self.rslt.show()
        self.close()



    def extractLkhra(self):
        extraction(self=self, agents=self.selectedAgents, fdate=self.dateEdit.date().toPyDate().strftime('%d-%m-%Y'), tdate=self.dateEdit_2.date().toPyDate().strftime('%d-%m-%Y'))
        self.goback()


    def refr(self):

        self.comboBox.clear()
        self.comboBox.addItems(self.agents)
        self.comboBox.setCurrentIndex(0)

    def addAllAg(self):
        for i in range(1, len(self.agents)+1):
            self.comboBox.setCurrentIndex(1)
            self.addAg()
        self.pushButton_2.setEnabled(True)

    def addAg(self):
        cnx = conn()
        cur = cnx.cursor()
        id = str(self.comboBox.currentText()).split('-')[0]
        if id:
            dd = f"""select a.id, a.fname, a.lname, c.campname from agents a inner join camps c on a.camp = c.id where a.id = {id} """
            print(dd)
            cur.execute(dd)
            data = [r for r in cur.fetchone()]
            self.selectedAgents.append(data[0])
            header = "Agent ID.First Name.Last Name.Campaign".split('.')
            self.tableWidget.setColumnCount(len(header))

            [self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch) for i in range(len(header))]
            self.tableWidget.setHorizontalHeaderLabels(header)
            self.tableWidget.insertRow(0)
            [self.tableWidget.setItem(0, c, QtWidgets.QTableWidgetItem(str(data[c]))) for c in range(len(data))]
            self.agents.remove(self.comboBox.currentText())
            self.refr()
            self.pushButton_2.setEnabled(True)
        else:
            self.comboBox.setCurrentIndex(0)
        cnx.close()


if __name__ == '__main__':
    # print(sys.getrecursionlimit())
    # sys.setrecursionlimit(1500)
    # print(sys.getrecursionlimit())
    app = QtWidgets.QApplication(sys.argv)
    screen = Login()
    # CPMS = ["1", "2", ]
    # USER = 1
    # screen = LhabaSawda() #todo for the test
    screen.show()
    sys.exit(app.exec_())