import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi


db = sqlite3.connect("school(1).db")
sql = db.cursor()



class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)

        
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.createaccbutton.clicked.connect(self.gotocreate)
        



    def loginfunction(self):

        email=self.email.text()
        password=self.password.text()
        sql.execute(f"SELECT * FROM users WHERE username = '{self.email.text()}' AND password = '{self.password.text()}';")
        db.commit() 


        if sql.fetchone() == None:
            print("Нет такой записи")
        else:
            print('Welcome')
            loginbutton=Client()
            widget.addWidget(loginbutton)
            widget.setCurrentIndex(widget.currentIndex()+1)




    def gotocreate(self):
        createaccbutton=CreateAcc()
        widget.addWidget(createaccbutton)
        widget.setCurrentIndex(widget.currentIndex()+1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.conn = None

    def createaccfunction(self):
        email = self.email.text()
        password=self.password.text()
        if self.password.text()==self.confirmpass.text():
               sql.execute(f"SELECT username, password FROM users WHERE username = '{email}' AND password = '{password}'")

        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES (?,?)", (email, password))
            db.commit()
            print('You have registered')
            signupbutton=Login()
            widget.addWidget(signupbutton)
            widget.setCurrentIndex(widget.currentIndex()+1)

        else:
            print('Такая запись уже существует')
            for i in sql.execute('SELECT * FROM users'):
                print(i)



class Client(QDialog):
    def __init__(self):
        super(Client, self).__init__()
        loadUi("client.ui",self)
        self.rbMale.setChecked(True)
        self.pbInsert.clicked.connect(self.insert_staff)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.pushButton_3.clicked.connect(self.gotouslugu)
        self.pushButton_2.clicked.connect(self.gotosvod)
        self.conn = None

    def open_file(self):
        try:
            self.conn = sqlite3.connect('school(1).db')
            cur = self.conn.cursor()
            data = cur.execute("select * from client")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def update_twStaffs(self, query="select * from client"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def insert_staff(self):
        row = [self.leFio.text(), self.leFio_2.text(), self.leFio_3.text(),  'м' if self.rbMale.isChecked() else 'ж', self.lePhone.text(), self.sbAge.text(),
                self.leEmail.text(), self.sbAge_2.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into client(second_name, first_name, last_name, gender, phone, data_start, Email, data_reg)
            values('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_twStaffs()

    def delete_staff(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from client where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()


    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from client where {col} like '{val}%'")

    def closeEvent(self, event):
        if self.conn is not None:
            self.conn.close()
        event.accept()

    def gotosvod(self):
        pushButton_2=Swod()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotouslugu(self):
        pushButton_3=Uslugu()
        widget.addWidget(pushButton_3)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Swod(QDialog):
    def __init__(self):
        super(Swod, self).__init__()
        loadUi("svod.ui",self)
        self.pbInsert.clicked.connect(self.insert_staff)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.pushButton_2.clicked.connect(self.gotouslugu)
        self.pushButton_1.clicked.connect(self.gotoclient)
        self.conn = None

    def open_file(self):
        try:
            self.conn = sqlite3.connect('school(1).db')
            cur = self.conn.cursor()
            data = cur.execute("select * from main;")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def update_twStaffs(self, query="select * from main"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def insert_staff(self):
        row = [self.leFio.text(), self.dateEdit.text(),
               self.timeEdit.text(), self.leEmail.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into main(id_usl, date_usl, time_usl, id_client)
            values('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def delete_staff(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from main where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from main where {col} like '{val}%'")


    def gotoclient(self):
        pushButton_1=Client()
        widget.addWidget(pushButton_1)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotouslugu(self):
        pushButton_2=Uslugu()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Uslugu(QDialog):
    def __init__(self):
        super(Uslugu, self).__init__()
        loadUi("uslugu.ui",self)
        self.pbInsert.clicked.connect(self.insert_staff)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.pushButton_2.clicked.connect(self.gotosvod)
        self.pushButton_1.clicked.connect(self.gotoclient)
        self.conn = None

    def open_file(self):
        try:
            self.conn = sqlite3.connect('school(1).db')
            cur = self.conn.cursor()
            data = cur.execute("select * from uslugu;")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setColumnCount(len(col_name))
        self.twStaffs.setHorizontalHeaderLabels(col_name)
        self.twStaffs.setRowCount(0)
        self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def update_twStaffs(self, query="select * from uslugu"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStaffs.setRowCount(0)
        for i, row in enumerate(data):
            self.twStaffs.setRowCount(self.twStaffs.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStaffs.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStaffs.resizeColumnsToContents()
        

    def insert_staff(self):
        row = [self.leFio.text(), self.leFio_2.text(), self.leFio_3.text(),
               self.lePhone.text(), self.leEmail.text(), self.leEmail_2.text(),]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into uslugu(name_usl, price, sale, price_finish, duration, image)
            values('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}')""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()

    def delete_staff(self):
        row = self.twStaffs.currentRow()
        num = self.twStaffs.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from uslugu where id_usl = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_twStaffs()


    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from uslugu where {col} like '{val}%'")

    def closeEvent(self, event):
        if self.conn is not None:
            self.conn.close()
        event.accept()



    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_twStaffs(f"select * from main where {col} like '{val}%'")

    def closeEvent(self, event):
        if self.conn is not None:
            self.conn.close()
        event.accept()

    def gotosvod(self):
        pushButton_2=Swod()
        widget.addWidget(pushButton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoclient(self):
        pushButton_1=Client()
        widget.addWidget(pushButton_1)
        widget.setCurrentIndex(widget.currentIndex()+1)



app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(700)
widget.show()
app.exec_()