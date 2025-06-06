import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)
        self.ui.pushButton_3.clicked.connect(self.call_api_generate_keys)
        self.ui.pushButton_4.clicked.connect(self.call_api_sign)
        self.ui.pushButton_5.clicked.connect(self.call_api_verify)
    def call_api_generate_keys(self):
        url="http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            reponse = requests.get(url)     
            if reponse.status_code == 200:
                data = reponse.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("message")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:  
            print("Error: %s" % e.message)
        
    def call_api_encrypt(self):
        url="http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui(),
            "key_type": "public"
        }
        try:
            reponse = requests.post(url, json=payload)
            if reponse.status_code == 200:
                data = reponse.json()
                self.ui.txt_ciphertext.setPlainText("encrypted_message")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
    def call_api_decrypt(self):
        url="http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_ciphertext.toPlainText(),
            "private_key": "private"
        }
        try:
            reponse = requests.post(url, json=payload)
            if reponse.status_code == 200:
                data = reponse.json()
                self.ui.plainTextEdit.setPlainText(data["decrypted_message"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            
            
            
    def call_api_sign(self):
        url="http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
        }
        try:
            reponse = requests.post(url, json=payload)
            if reponse.status_code == 200:
                data = reponse.json()
                self.ui.txt_sign.setPlainText(data["signature"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
    def call_api_verify(self):
        url="http://123.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText(),
        }
        try:
            reponse = requests.post(url, json=payload)
            if reponse.status_code == 200:
                data = reponse.json()
                if (data["is_verified"]):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("verification successful")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Verification failed")
                    msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
if __name__ == "__main__":
    app=QApplication(sys.argv)
    window=MyApp()
    window.show()
    sys.exit(app.exec_())