# =============================================================================
# --------------------------------------------------------------------------------------------
# Project                         : 5 Bar Cubuk mekaizması - Paralel maniplator yazılımı
# Author                          : Yavuz BEKTAŞ, Murat Hep.
# Hardware and Software           : Omron PLC NX1P2, Python 3.7 , QT Designer
#
# Code Version                    : 1.1
# Require Library                 : os,pyqt5, sys, struct,socket(UDP comm)
# #######################################
__file__ = "MyApp.py"
__author__ = "Yavuz Bektaş"
__version__ = "1.0"
__email__ = "yavuzbektas@gmail.com"
__linkedin__ = "https://www.linkedin.com/in/yavuz-bekta%C5%9F-28659642/"
__release_date__ = "2020.05.01"
# #######################################


# ============================================================================
import sys, time,os
from struct import pack, unpack
from GUI.mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from servo import ServoClass

import socket
from threading import Thread
# ============================================================================
# ================   SETTINGS     ===================================
BASE_PATH = os.getcwd()
FILE_DIR = (BASE_PATH + '\\staticfiles\\')

# print('Setting files are in {} folder. '.format(FILE_DIR))
# ----------------------------------------------#
REMOTE_UDP_IP_ADDRESS = "192.168.0.131"
REMOTE_UDP_PORT_NO = 6000
LOCAL_UDP_IP_ADDRESS = "192.168.0.100"
LOCAL_UDP_PORT_NO = 6001
RECIEVE_DATA_SIZE = 16
SEND_DATA_SIZE = 14
# ----------------------------------------------#
# globals
data = ["" for x in range(RECIEVE_DATA_SIZE)]
message = [0 for x in range(SEND_DATA_SIZE)]


# ----------------------------------------------#

class Thread(QThread):
    val1 = pyqtSignal(float)
    data_val = pyqtSignal(list)

    def __init__(self, parent=None, *args, **kwargs):
        QThread.__init__(self, parent, *args, **kwargs)
        self.flag = False

    def send_message(self,Message):
        # Message = bytes(Message)

        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSock.sendto(Message, (REMOTE_UDP_IP_ADDRESS, REMOTE_UDP_PORT_NO))
        # print(Message)

    def recieve_message(self):
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSock.bind((LOCAL_UDP_IP_ADDRESS, LOCAL_UDP_PORT_NO))

        data, addr = serverSock.recvfrom(RECIEVE_DATA_SIZE * 8)
        # print("Message: ", list(data))
        return list(data)
    def send_recieve_data(self, ver):
        self.ver = ver
        try:
            deger = pack("hhhhhhhhdddddd", self.ver[0], self.ver[1], self.ver[2], self.ver[3], self.ver[4], self.ver[5],
                         self.ver[6], self.ver[7], self.ver[8], self.ver[9],self.ver[10],self.ver[11],self.ver[12],self.ver[13])
        except:

            print("deger hatası")
            deger = bytes(0)

        self.send_message(deger)
        data = self.recieve_message()
        self.data_val.emit(data)

    def run(self):
        self.flag = True
        while self.flag:
            global message
            self.send_recieve_data(message)
            QThread.sleep(0.01)

    def stop(self):
        self.flag = False
        print("thread durdu")

        self.wait(1)

    def exit(self, returnCode: int = ...) -> None:
        print("thread sonlandı")

class MyApp(QMainWindow):
    sig = pyqtSignal(float)

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.handle_button()
        self.userUI()
        self.th = Thread()
        self.ui.groupBox_6.setEnabled(False)

    def handle_button(self):  # basılan tüm butonlar yakalnaır
        self.ui.connect_pb_s1.clicked.connect(self.button_check)
        self.ui.modeSelection_cb_s1.currentIndexChanged.connect(self.msg_update)
        self.ui.servoOn_pb_s1.clicked.connect(self.button_onOff)
        self.ui.reset_pb_s1.pressed.connect(self.reset_onoff)
        self.ui.reset_pb_s1.released.connect(self.reset_onoff)
        self.ui.start_pb_s1.clicked.connect(self.button_onOff)

    def msg_update(self): #send message
        global message

        message[0] = self.ui.modeSelection_cb_s1.currentIndex()
        message[1] = 1 if self.ui.servoOn_pb_s1.text() == "OFF" else 0
        message[2] = 1 if self.ui.reset_pb_s1.text() == "ACKNOWLEDGED" else 0
        message[3] = self.ui.direction_sb_s1.value()
        message[4] = 1 if self.ui.start_pb_s1.text() == "OFF" else 0
        message[5] = 0 #reserved
        message[6] = 0#reserved
        message[7] = 0#reserved
        message[8] = self.ui.vel_sp_s1.value()
        message[9] = self.ui.acc_sp_s1.value()
        message[10] = self.ui.dcc_sp_s1.value()
        message[11] = self.ui.pos_sp_s1.value()
        message[12] = self.ui.dist_sp_s1.value()
        message[13] = 0.0  # reserved

        self.data_update()

    def data_update(self):

        data_new = [x for x in data]
        self.ui.mcerror_cb_s1.setCurrentIndex(data_new[0])
        self.ui.errID_lb_s1.setText(str(hex(data_new[1])))
        self.ui.driver_error_lb_s1.setText(str(hex(data_new[3])))
        self.ui.statusword_lb_s1.setText(str(hex(data_new[4])))
        self.ui.act_trq_le_s1.setText(str(data_new[5]))
        self.ui.mode_status_cb_s1.setCurrentIndex(data_new[6])
        if data_new[7]==1 :
            self.ui.dir_lb_s1.setText("Forward")
        else:
            self.ui.dir_lb_s1.setText("Reverse")

        self.ui.act_pos_le_s1.setText(str(data_new[9]))

        self.ui.vel_le_s1.setText(str(data_new[12]))
        self.ui.act_vel_le_s1.setText(str(data_new[12]))
        self.ui.acc_le_s1.setText(str(data_new[13]))
        self.ui.dcc_le_s1.setText(str(data_new[13]))
        self.ui.pos_le_s1.setText(str(data_new[14]))
        self.statusword_radiobutton(data_new[4])
        self.digitalinputs_radiobutton(data_new[10])


    def statusword_radiobutton(self,statusword):
        try:

            statusword=bin(statusword)[2:].zfill(16)
            self.ui.statusword_bin_lb_s1.setText(statusword)
            # veri=unpack("????????", bytes(statusword))

        except Exception as e:
            print(e)


        if statusword[15]=='1':
            self.ui.sw_0_rb_s1.setChecked(True)
        else:
            self.ui.sw_0_rb_s1.setChecked(False)
        if statusword[14]=='1':
            self.ui.sw_1_rb_s1.setChecked(True)
        else:
            self.ui.sw_1_rb_s1.setChecked(False)
        if statusword[13]=='1':
            self.ui.sw_2_rb_s1.setChecked(True)
        else:
            self.ui.sw_2_rb_s1.setChecked(False)
        if statusword[12]=='1':
            self.ui.sw_3_rb_s1.setChecked(True)
        else:
            self.ui.sw_3_rb_s1.setChecked(False)
        if statusword[11]=='1':
            self.ui.sw_4_rb_s1.setChecked(True)
        else:
            self.ui.sw_4_rb_s1.setChecked(False)
        if statusword[10]=='1':
            self.ui.sw_5_rb_s1.setChecked(True)
        else:
            self.ui.sw_5_rb_s1.setChecked(False)
        if statusword[9]=='1':
            self.ui.sw_6_rb_s1.setChecked(True)
        else:
            self.ui.sw_6_rb_s1.setChecked(False)
        if statusword[8]=='1':
            self.ui.sw_7_rb_s1.setChecked(True)
        else:
            self.ui.sw_7_rb_s1.setChecked(False)
        if statusword[7]=='1':
            self.ui.sw_8_rb_s1.setChecked(True)
        else:
            self.ui.sw_8_rb_s1.setChecked(False)
        if statusword[6]=='1':
            self.ui.sw_9_rb_s1.setChecked(True)
        else:
            self.ui.sw_9_rb_s1.setChecked(False)
        if statusword[5]=='1':
            self.ui.sw_10_rb_s1.setChecked(True)
        else:
            self.ui.sw_10_rb_s1.setChecked(False)
        if statusword[4]=='1':
            self.ui.sw_11_rb_s1.setChecked(True)
        else:
            self.ui.sw_11_rb_s1.setChecked(False)
        if statusword[3]=='1':
            self.ui.sw_12_rb_s1.setChecked(True)
        else:
            self.ui.sw_12_rb_s1.setChecked(False)
        if statusword[2]=='1':
            self.ui.sw_13_rb_s1.setChecked(True)
        else:
            self.ui.sw_13_rb_s1.setChecked(False)
        if statusword[1]=='1':
            self.ui.sw_14_rb_s1.setChecked(True)
        else:
            self.ui.sw_14_rb_s1.setChecked(False)
        if statusword[0]=='1':
            self.ui.sw_15_rb_s1.setChecked(True)
        else:
            self.ui.sw_15_rb_s1.setChecked(False)


    def digitalinputs_radiobutton(self,inputsdWord):
        try:

            inputsWord=bin(inputsdWord)[2:].zfill(32)
            self.ui.digitalinputs_lb_s1.setText(inputsWord)
        except Exception as e:
            print(e)


        if inputsWord[31]=='1':
            self.ui.digin_0_rb_s1.setChecked(True)
        else:
            self.ui.sw_0_rb_s1.setChecked(False)
        if inputsWord[30]=='1':
            self.ui.digin_1_rb_s1.setChecked(True)
        else:
            self.ui.sw_1_rb_s1.setChecked(False)
        if inputsWord[29]=='1':
            self.ui.digin_2_rb_s1.setChecked(True)
        else:
            self.ui.digin_2_rb_s1.setChecked(False)
        if inputsWord[13]=='1':
            self.ui.digin_16_rb_s1.setChecked(True)
        else:
            self.ui.digin_16_rb_s1.setChecked(False)
        if inputsWord[12]=='1':
            self.ui.digin_17_rb_s1.setChecked(True)
        else:
            self.ui.digin_17_rb_s1.setChecked(False)
        if inputsWord[26]=='1':
            self.ui.digin_18_rb_s1.setChecked(True)
        else:
            self.ui.digin_18_rb_s1.setChecked(False)
        if inputsWord[11]=='1':
            self.ui.digin_20_rb_s1.setChecked(True)
        else:
            self.ui.digin_20_rb_s1.setChecked(False)
        if inputsWord[10]=='1':
            self.ui.digin_21_rb_s1.setChecked(True)
        else:
            self.ui.digin_21_rb_s1.setChecked(False)
        if inputsWord[9]=='1':
            self.ui.digin_22_rb_s1.setChecked(True)
        else:
            self.ui.digin_22_rb_s1.setChecked(False)
        if inputsWord[8]=='1':
            self.ui.digin_23_rb_s1.setChecked(True)
        else:
            self.ui.digin_23_rb_s1.setChecked(False)
        if inputsWord[7]=='1':
            self.ui.digin_24_rb_s1.setChecked(True)
        else:
            self.ui.digin_24_rb_s1.setChecked(False)
        if inputsWord[6]=='1':
            self.ui.digin_25_rb_s1.setChecked(True)
        else:
            self.ui.digin_25_rb_s1.setChecked(False)
        if inputsWord[5]=='1':
            self.ui.digin_26_rb_s1.setChecked(True)
        else:
            self.ui.digin_26_rb_s1.setChecked(False)
        if inputsWord[4]=='1':
            self.ui.digin_27_rb_s1.setChecked(True)
        else:
            self.ui.digin_27_rb_s1.setChecked(False)
        if inputsWord[3]=='1':
            self.ui.digin_28_rb_s1.setChecked(True)
        else:
            self.ui.digin_28_rb_s1.setChecked(False)
        if inputsWord[2]=='1':
            self.ui.digin_29_rb_s1.setChecked(True)
        else:
            self.ui.digin_29_rb_s1.setChecked(False)
        if inputsWord[1]=='1':
            self.ui.digin_30_rb_s1.setChecked(True)
        else:
            self.ui.digin_30_rb_s1.setChecked(False)
        if inputsWord[0]=='1':
            self.ui.digin_31_rb_s1.setChecked(True)
        else:
            self.ui.digin_31_rb_s1.setChecked(False)




    def userUI(self):
        pass

    def button_onOff(self):
        sender = self.sender()

        if sender.text() == "ON":
            sender.setText("OFF")
            sender.setStyleSheet("background-color: rgb(65, 197, 96);")
        else:
            sender.setText("ON")
            sender.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.msg_update()

    def reset_onoff(self):

        sender = self.sender()

        if sender.text() == "ACKNOWLEDGED":
            sender.setText("RESET")
            sender.setStyleSheet("background-color: rgb(255, 0, 0);")
        else:
            sender.setText("ACKNOWLEDGED")
            sender.setStyleSheet("background-color: rgb(65, 197, 96);")
        self.msg_update()

    def button_check(self):

        if self.ui.connect_pb_s1.text() == "DISCONNECT":
            self.ui.connect_pb_s1.setText("CONNECT")
            self.ui.connect_pb_s1.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.ui.groupBox_6.setEnabled(False)

            self.stop_driver()
            self.thread_stop()
        else:
            self.ui.connect_pb_s1.setText("DISCONNECT")
            self.ui.connect_pb_s1.setStyleSheet("background-color: rgb(65, 197, 96);")
            self.ui.groupBox_6.setEnabled(True)
            self.thread_start()

    def stop_driver(self):


        self.msg_update()
        return True

    def thread_stop(self):

        self.th.stop()

    def thread_start(self):

        if self.th.isRunning():
            print("thread is already running")
        else:
            self.th.data_val.connect(self.recieved_data)
            self.th.start()
            print("thread started")

    @pyqtSlot(list)
    def recieved_data(self, send_list):
        global data
        # print("Send Data Frame for Servo 1 = ", message)

        try:

            data = unpack("hhhhhhhhhlLdddd", bytes(send_list))

            # print("Recieved Data Frame for Servo 1 = ", data)
        except Exception as e:
            print(e)
            print("Alınan Mesaj Hatalı")
            data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.msg_update()

    def __del__(self):
        self.th.exit()


def program():
    app = QApplication(sys.argv)
    MainWindow = MyApp()

    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    program()
