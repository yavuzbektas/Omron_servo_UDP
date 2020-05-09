from PyQt5 import QtCore, QtGui, QtWidgets

from GUI.mainwindow import Ui_MainWindow

class ServoClass(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ServoClass, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mode_selection = self.ui.comboBox
        self.servo_pwr_on = False
        self.servo_run = False
        self.reset = False
        self.direction = False
        self.velocity = 0.0
        self.acc = 0.0
        self.dcc = 0.0
        self.position = 0.0
        self.distance = 0.0

        self.param_mode = 0
        self.act_pos = 0.0
        self.act_vel = 0.0
        self.act_trq = 0.0
        self.act_accdcc = 0.0
        self.dir_pos = True
        self.dir_neg = False
        self.drvstatus_ready = False
        self.drvstatus_servoON = False
        self.drvstatus_alarm = False
        self.drvstatus_alarmID = 0

    def pwr_control_block(self):
        self.param_mode=5

    def reset_control_block(self):
        pass

    def move_jog_control_block(self):
        pass

    def move_relative_control_block(self):
        pass

    def move_absolute_control_block(self):
        pass

    def move_velocity_control_block(self):
        pass

    def read_axis_parameters(self):
        pass


