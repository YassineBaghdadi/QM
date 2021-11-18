
import pymysql, datetime, sys, os, random, string, numpy as np
from PyQt5 import QtGui, QtWidgets, uic, QtCore

from PyQt5.QtWidgets import QHeaderView


def conn() :
    return pymysql.Connect(host="10.73.200.200", user="qlfier", password="1234@@it.", database="QM")

CPMS = []
USER = None
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
    #
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

    def openNewR(self):
        self.nr = NewQalif(str(self.ag.currentText()).split('-')[0])
        self.nr.show()
        self.close()

    def getQlfs(self):
        cnx = conn()
        cur = cnx.cursor()
        if self.ag.currentIndex() != 0 and self.ag.isEnabled():
            self.newR.setEnabled(True)
            self.qlfs.clear()
            q = f"""select id from qualification where idagent = {str(self.ag.currentText()).split('-')[0]} and qdate like '{self.dateEdit.date().toPyDate().strftime('%d-%m-%Y')}'"""
            print(q)
            cur.execute(q)
            c = cur.fetchall()
            if c:
                print("$"*100)
                print(c)
                self.qlf = [str(i[0]) for i in c] if len(c) > 1 else c[0]
                print(self.qlf)
                self.qlfs.setEnabled(True)
                self.qlfs.addItems(self.qlf)
        else:
            self.newR.setEnabled(False)
            self.qlfs.clear()
            self.qlfs.setEnabled(False)

        self.refresh()
        cur.close()
        cnx.close()

    def getAgents(self):
        cnx = conn()
        cur = cnx.cursor()
        if self.cm.currentIndex() != 0:
            self.ag.clear()
            q =f"""select concat(id, '-', fname, ' ', lname) as fullName from agents where camp = (select id from camps where campname like "{self.cm.currentText()}")"""
            print(q)
            cur.execute(q)
            c = cur.fetchall()
            self.agents = [i[0] for i in c] if len(c) >1 else [c[0]]
            print(self.agents)
            self.agents.insert(0, "choose Agent ...")
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
            try:
                self.tableWidget.setEnabled(True)

                cnx = conn()
                cur = cnx.cursor()
                qq = f"""select q.qname, r.r, qq.qdate, u.fullname from qalif q inner join rslt r on r.idq = q.id inner join qualification qq on r.idqlf = qq.id inner join users u on qq.iduser = u.id where qq.idagent = {str(self.ag.currentText()).split('-')[0]} and qq.id like "{self.qlfs.currentText()}";"""
                print(f'{"#"*100}\n{qq}')
                cur.execute(qq)

                data = cur.fetchall()

                self.tableWidget.clear()
                self.tableWidget.setColumnCount(len(data[0]))
                self.tableWidget.setRowCount(len(data))
                self.tableWidget.setHorizontalHeaderLabels("Qualification.Result.Qualifier.Date".split('.'))
                [self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch) for i in range(len(data[0]))]

                for r in range(len(data)):

                    for c in range(data[0]):
                        self.tableWidget.setItem(r,c, QtWidgets.QTableWidgetItem(str(data[r][c])))
                cur.close()
                cnx.close()
            except Exception as e:
                print(e)
                self.tableWidget.setEnabled(False)


class NewQalif(QtWidgets.QWidget):
    def __init__(self, agent):
        super(NewQalif, self).__init__()
        uic.loadUi(os.path.join(os.getcwd(), 'ui', 'newqalif.ui'), self)
        self.submit.setEnabled(False)

        self.lbtn.setPixmap(QtGui.QPixmap('src/img/left.png'))
        self.lbtn.setScaledContents(True)
        self.rbtn.setPixmap(QtGui.QPixmap('src/img/right.png'))
        self.rbtn.setScaledContents(True)
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
                            self.comboBox_2.setCurrentIndex(items.index(i[k]["ans"]))
                            self.textEdit.setPlainText(i[k]["note"])


                # self.textEdit.setPlainText(self.ansers["qlf"][str(self.label_3.text()).split("-")[0]]["note"])
            else:
                self.comboBox_2.setCurrentIndex(items.index("0.0"))
                self.textEdit.setPlainText("")

        self.submit.setEnabled(True if 'qlf' in self.ansers else False)


    def addReason(self):
        if self.lineEdit.text():
            self.cur.execute(f'select id from callReasons where reason like "{str(self.lineEdit.text()).strip()}"')
            try:
                if not self.cur.fetchone()[0]:
                    self.cur.execute(f'''insert into callReasons(reason) value("{str(self.lineEdit.text()).strip()}")''')
                    self.cnx.commit()
                    self.refreshreasons()
                    self.lineEdit.setText('')
            except:
                self.cur.execute(f'''insert into callReasons(reason) value("{str(self.lineEdit.text()).strip()}")''')
                self.cnx.commit()
                self.refreshreasons()
                self.lineEdit.setText('')

    def refreshreasons(self):
        self.comboBox.clear()
        self.cur.execute(f'''select concat(id, "-", reason) from callReasons''')
        self.comboBox.addItems(["Call Reason ..."]+[i[0] for i in self.cur.fetchall()])

    def startTheQlf(self):
        self.ansers["callReason"] = str(self.comboBox.currentText()).split("-")[0]
        self.ansers["user"] = USER
        self.ansers["agent"] = self.agent
        self.ansers["date"] = datetime.datetime.today().strftime('%d-%m-%Y')
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
        self.ansers["qlf"].append(
            {qlfID: {"ans": self.comboBox_2.currentText(), "note": self.textEdit.toPlainText(), }})

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
        self.cur.execute(f"""insert into qualification(iduser, idagent, qdate, reason) values(
                    {self.ansers["user"]},
                    {self.ansers["agent"]},
                    "{datetime.datetime.today().strftime('%d-%m-%Y')}",
                    {self.ansers["callReason"]}
        
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












if __name__ == '__main__':
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(1500)
    print(sys.getrecursionlimit())
    app = QtWidgets.QApplication(sys.argv)
    screen = Login()
    # CPMS = ["1", "2", ]
    # USER = 1
    # screen = NewQalif("3") #todo for the test
    screen.show()
    sys.exit(app.exec_())