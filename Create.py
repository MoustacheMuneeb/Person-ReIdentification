import mysql.connector
import sys
import re
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, QCheckBox, QLabel, QWidget, QHBoxLayout, \
    QFileDialog
from PyQt5.QtGui import QRegularExpressionValidator, QColor

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import cv2

class Welcomescreen(QtWidgets.QMainWindow):
    def __init__(self, widget):
        super(Welcomescreen, self).__init__()
        loadUi("wwlcome.ui", self)
        self.widget = widget
        self.login.clicked.connect(self.gotologin)

    def gotologin(self):
        login = LoginScreen(self.widget)
        self.add_screen(login)

    def add_screen(self, screen):
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)


class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self, widget):
        super(LoginScreen, self).__init__()
        loadUi("loginpage.ui", self)
        self.widget = widget
        self.signin.clicked.connect(self.loginfunction)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)

        # Email Validation
        email_validator = QRegularExpressionValidator(QRegularExpression(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'))
        self.emailfield.setValidator(email_validator)

    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        if not user or not password:
            self.error.setText("Please input all fields")
        elif not self.is_valid_email(user):
            self.error.setText("Invalid email format")
        else:
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    database="mydata"
                )
                print("Connected to MySQL database!")

                cursor = mydb.cursor()

                cursor.execute("SELECT * FROM login WHERE Email = %s AND Password = %s", (user, password))

                row = cursor.fetchone()

                if row:
                    status = row[4]
                    if status == 0:
                        self.error.setText("Your account is blocked. Please contact support.")
                    else:
                        user_type = row[3]
                        if user_type == 0:
                            # Open home_page.ui
                            home_screen = HomeScreen(self.widget)
                            self.widget.addWidget(home_screen)
                            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
                        elif user_type == 1:
                            # Open home_user.ui
                            home_user_screen = HomeUserScreen(self.widget)
                            self.widget.addWidget(home_user_screen)
                            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
                else:
                    self.error.setText("Invalid email or password")

                cursor.close()
                mydb.close()

            except mysql.connector.Error as err:
                print("Error:", err)

    def is_valid_email(self, email):
        return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email) is not None


class HomeScreen(QtWidgets.QMainWindow):
    def __init__(self, widget, rtsp_url=None):
        super(HomeScreen, self).__init__()
        loadUi("home_page.ui", self)
        self.widget = widget
        self.search_person.clicked.connect(self.gotosearch)
        self.camera.clicked.connect(self.addcamera)
        self.List.clicked.connect(self.adduser)
        self.log.clicked.connect(self.gotologin)
        self.rtsp_url = rtsp_url
        self.initUI()

    def initUI(self):
        if self.rtsp_url:
            self.display_stream(self.rtsp_url)

    def display_stream(self, rtsp_url):
        self.capture = cv2.VideoCapture(rtsp_url)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            step = channel * width
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(qImg))

    def closeEvent(self, event):
        if self.capture.isOpened():
            self.capture.release()

    def gotologin(self):
        back = LoginScreen(self.widget)
        self.widget.addWidget(back)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def adduser(self):
        back = ListUser(self.widget)
        self.widget.addWidget(back)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotosearch(self):
        search_person = SearchPerson(self.widget)
        self.widget.addWidget(search_person)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def addcamera(self):
        search_person = AddCamera(self.widget)
        self.widget.addWidget(search_person)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)


class HomeUserScreen(QtWidgets.QMainWindow):
    def __init__(self, widget):
        super(HomeUserScreen, self).__init__()
        loadUi("home_user.ui", self)
        self.widget = widget
        self.search_person.clicked.connect(self.gotosearch)
        self.log.clicked.connect(self.gotologin)

    def gotologin(self):
        back = LoginScreen(self.widget)
        self.widget.addWidget(back)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotosearch(self):
        search_person = Search_user_person(self.widget)
        self.widget.addWidget(search_person)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)


class Search_user_person(QtWidgets.QMainWindow):
    def __init__(self, widget):
        super(Search_user_person, self).__init__()
        loadUi("search_person_pag.ui", self)
        self.widget = widget
        self.home.clicked.connect(self.gotohomeuser)
        self.log.clicked.connect(self.gotologin)

    def gotohomeuser(self):
        goto = HomeUserScreen(self.widget)
        self.widget.addWidget(goto)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotologin(self):
        back = LoginScreen(self.widget)
        self.widget.addWidget(back)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)


class SearchPerson(QtWidgets.QMainWindow):
    def __init__(self, widget):
        super(SearchPerson, self).__init__()
        loadUi("search_Admin.ui", self)
        self.widget = widget
        self.home.clicked.connect(self.gotohome)
        self.log.clicked.connect(self.gotologin)
        self.clicking.clicked.connect(self.addcamera)
        self.List.clicked.connect(self.adduser)
        self.pushButton_5.clicked.connect(self.open_file_dialog)

    def addcamera(self):
        search_person = AddCamera(self.widget)
        self.widget.addWidget(search_person)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotologin(self):
        back = LoginScreen(self.widget)
        self.widget.addWidget(back)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog(self)
        file_dialog.setStyleSheet("background-color: white;")
        file_path, _ = file_dialog.getOpenFileName(self, "Choose File", "", "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        if file_path:
            self.label_4.setText(file_path)
            self.label_4.setStyleSheet("color: white;")

    def adduser(self):
        back = ListUser(self.widget)
        self.widget.addWidget(back)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotohome(self):
        home_screen = HomeScreen(self.widget)
        self.widget.addWidget(home_screen)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)


class AddCamera(QMainWindow):
    def __init__(self, widget):
        super(AddCamera, self).__init__()
        loadUi("add_camera_page.ui", self)
        self.widget = widget
        self.home.clicked.connect(self.gotohome)
        self.person.clicked.connect(self.gotosearch)
        self.List.clicked.connect(self.adduser)
        self.log.clicked.connect(self.gotologin)
        self.Save.clicked.connect(self.save_camera)  # Connect the Save button to save_camera method

    def gotologin(self):
        back = LoginScreen(self.widget)
        self.widget.addWidget(back)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def save_camera(self):
        print("misha1")
        camera_name = self.CameraName.text()  # assuming CameraName is the object name for camera name field
        ip_address = self.IPAddress.text()  # assuming IPAddress is the object name for IP address field
        location = self.Location.toPlainText()  # assuming Location is the object name for location field
        rtsp_url = f"rtsp://{ip_address}:554/stream1"  # Convert IP address to RTSP URL
        if self.save_camera_configuration(camera_name, rtsp_url, location):
            self.gotohome(rtsp_url)

    def save_camera_configuration(self, camera_name, ip_address, location):
        print("misha2")
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                database="mydata"
            )
            cursor = mydb.cursor()
            sql = "INSERT INTO cameraconfig (CameraName, IPAddress, Location) VALUES (%s, %s, %s)"
            val = (camera_name, ip_address, location)
            cursor.execute(sql, val)
            mydb.commit()
            print("Camera configuration saved successfully.")
            cursor.close()
            mydb.close()
            return True
        except mysql.connector.Error as err:
            print("Error:", err)
            self.error.setText("Error in saving configuration. Please try again.")
            return False

    def adduser(self):
        back = ListUser(self.widget)
        self.widget.addWidget(back)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotohome(self, rtsp_url=None):
        home_screen = HomeScreen(self.widget, rtsp_url)
        self.widget.addWidget(home_screen)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotosearch(self):
        search_person = SearchPerson(self.widget)
        self.widget.addWidget(search_person)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

class ListUser(QtWidgets.QMainWindow):
    def __init__(self, widget):
        print("iqra1")
        super(ListUser, self).__init__()
        loadUi("user_list.ui", self)
        self.widget = widget
        self.add_button.clicked.connect(self.add_data)
        self.home.clicked.connect(self.gotohome)
        self.person.clicked.connect(self.gotosearch)
        self.camera.clicked.connect(self.addcamera)
        self.log.clicked.connect(self.gotologin)

        # Connect to MySQL database
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            database="mydata"
        )

        # Populate tableWidget with data from the database
        self.populate_table()

    def populate_table(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT Email, Password, status FROM login WHERE user_type = 1")
            data = cursor.fetchall()
            cursor.close()

            for rowposition, (email, password, status) in enumerate(data):
                self.tableWidget.insertRow(rowposition)
                self.tableWidget.setItem(rowposition, 0, QTableWidgetItem(email))
                password_item = QTableWidgetItem(password)
                password_item.setForeground(Qt.white)
                self.tableWidget.setItem(rowposition, 1, password_item)

                # Add delete button to the new row
                delete_button = QPushButton('Delete')
                delete_button.setStyleSheet("color: white; background-color: black;")
                delete_button.clicked.connect(lambda _, row=rowposition: self.delete_row(row))
                self.tableWidget.setCellWidget(rowposition, 2, delete_button)

                # Add checkbox to the new row
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout()
                checkbox = QCheckBox()
                checkbox_layout.addWidget(checkbox)
                label = QLabel('Enable' if status == 1 else 'Disable')
                label.setStyleSheet("color: white;")
                checkbox_layout.addWidget(label)
                checkbox_widget.setLayout(checkbox_layout)
                self.tableWidget.setCellWidget(rowposition, 3, checkbox_widget)
                checkbox.stateChanged.connect(
                    lambda state, label=label, row=rowposition: self.update_status(state, label, row))

        except mysql.connector.Error as err:
            print("Error:", err)

    def gotologin(self):
        back = LoginScreen(self.widget)
        self.widget.addWidget(back)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotohome(self):
        home_screen = HomeScreen(self.widget)
        self.widget.addWidget(home_screen)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def addcamera(self):
        search_person = AddCamera(self.widget)
        self.widget.addWidget(search_person)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotosearch(self):
        search_person = SearchPerson(self.widget)
        self.widget.addWidget(search_person)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def add_data(self):
        print("iqra")
        email = self.email_edit.text()
        password = self.password_edit.text()

        # Email validation regex pattern
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

        # Password validation criteria: at least 8 characters
        password_min_length = 8

        if not re.match(email_pattern, email):
            self.label_6.setText("Invalid email format")
            return

        if len(password) < password_min_length:
            self.label_6.setText(f"Password must be at least {password_min_length} characters long")
            return

        if email.strip() and password.strip():
            try:
                # Insert data into MySQL database
                cursor = self.db_connection.cursor()
                insert_query = "INSERT INTO login (Email, Password, status) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (email, password, 0))
                self.db_connection.commit()
                cursor.close()

                # Add data to the tableWidget
                rowposition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowposition)
                self.tableWidget.setItem(rowposition, 0, QTableWidgetItem(email))

                password_item = QTableWidgetItem(password)
                password_item.setForeground(Qt.white)
                self.tableWidget.setItem(rowposition, 1, password_item)

                # Add delete button to the new row
                delete_button = QPushButton('Delete')
                delete_button.setStyleSheet("color: white; background-color: black;")
                delete_button.clicked.connect(lambda _, row=rowposition: self.delete_row(row))
                self.tableWidget.setCellWidget(rowposition, 2, delete_button)

                # Add checkbox to the new row
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout()
                checkbox = QCheckBox()
                checkbox_layout.addWidget(checkbox)
                label = QLabel('Disable')
                label.setStyleSheet("color: white;")
                checkbox_layout.addWidget(label)
                checkbox_widget.setLayout(checkbox_layout)
                self.tableWidget.setCellWidget(rowposition, 3, checkbox_widget)
                checkbox.stateChanged.connect(
                    lambda state, label=label, row=rowposition: self.update_status(state, label, row))

                # Clear input fields after adding data
                self.email_edit.clear()
                self.password_edit.clear()

            except mysql.connector.Error as err:
                print("Error:", err)

    def delete_row(self, row):
        try:
            # Get the email from the tableWidget
            email_item = self.tableWidget.item(row, 0)
            email = email_item.text()

            # Remove the row from the tableWidget
            self.tableWidget.removeRow(row)

            # Delete the row from the backend (MySQL database)
            cursor = self.db_connection.cursor()
            delete_query = "DELETE FROM login WHERE Email = %s"
            cursor.execute(delete_query, (email,))
            self.db_connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Error:", err)

    def update_status(self, state, label, row):
        try:
            # Update the status in the database based on the checkbox state
            cursor = self.db_connection.cursor()
            update_query = "UPDATE login SET status = %s WHERE Email = %s"
            cursor.execute(update_query, (1 if state == Qt.Checked else 0, self.tableWidget.item(row, 0).text()))
            self.db_connection.commit()
            cursor.close()

            # Update the label text based on the checkbox state
            if state == Qt.Checked:
                label.setText('Enable')
            else:
                label.setText('Disable')

        except mysql.connector.Error as err:
            print("Error:", err)


import source

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    welcome = Welcomescreen(widget)
    widget.addWidget(welcome)
    welcome.widget = widget  # Assign the QStackedWidget to Welcomescreen's widget attribute
    widget.addWidget(welcome)
    widget.showMaximized()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Exiting")
