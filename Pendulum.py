from math import (sin, cos, radians, ceil)
import sys
import qdarkstyle
from PyQt5.QtWidgets import   QMainWindow, QApplication, QToolTip, QMessageBox, QProgressBar
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import QCoreApplication, QBasicTimer
class Pendulum:
        def __init__(self):
            self.k = 20  # Spring stiffness, N/m
            self.m_1 = 1  # Spring load mass, kg
            self.m_2 = 1  # Weight of the load to the rod, kg
            self.l = 1  # Rod length, m
            self.fi0 = radians(-50)  # The initial angle of deflection of the rod from the vertical, measured clockwise
            self.x0 = 0  # Initial x-coordinate of the spring pendulum
            self.fi0_der = radians(0)  # The following 'der' is derivative
            self.x0_der = 0
            self.dt = 0.001  # Time between iterations
            self.res_x = self.x0  # Current x-coordinate of the spring pendulum
            self.res_fi = self.fi0  # Rod deflection angle
            self.t = 0.01  # End time
            self.x_der = self.x0_der
            self.fi_der = self.fi0_der
      # Further there're all sorts of calculations, Lagrangians, Runge Kutta
        def a_der(self, x, fi, fi_der):
             numerator = self.m_2 * self.l * sin(fi) * fi_der** 2 + self.k * x + self.m_2 * 9.81 * sin(fi) * cos(fi)
             denominator = self.m_2 * (cos(fi)) ** 2 - self.m_1 - self.m_2
             return numerator/denominator
        def b_der(self, x, fi, fi_der):
             numerator = 9.81 * sin(fi) + cos(fi) * (self.m_2 * self.l * fi_der ** 2 * sin(fi) + self.k * x) / (self.m_1 + self.m_2)
             denominator = -1 * self.l + self.m_2 * self.l * (cos(fi)) ** 2 / (self.m_1 + self.m_2)
             return numerator / denominator
        def result(self):
            fi = self.fi0
            x = self.x0
            x_der = self.x0_der
            fi_der = self.fi0_der
            for i in range(1, ceil(self.t / self.dt), 1):
                k1_a = self.a_der(x, fi, fi_der) * self.dt
                k1_b = self.b_der(x, fi, fi_der) * self.dt
                k1_x = x_der* self.dt
                k1_fi = fi_der * self.dt
                k2_a = self.a_der(x + k1_x / 2, fi + k1_fi / 2, fi_der + k1_b / 2) * self.dt
                k2_b = self.b_der(x + k1_x / 2, fi + k1_fi / 2, fi_der + k1_b / 2) * self.dt
                k2_x = (x_der + k1_a / 2) * self.dt
                k2_fi = (fi_der + k1_b / 2) * self.dt
                k3_a = self.a_der(x + k2_x / 2, fi + k2_fi / 2, fi_der + k2_b / 2) * self.dt
                k3_b = self.b_der(x + k2_x / 2, fi + k2_fi / 2, fi_der + k2_b / 2) * self.dt
                k3_x = (x_der + k2_a / 2) * self.dt
                k3_fi = (fi_der + k2_b / 2) * self.dt
                k4_a = self.a_der(x + k3_x / 2, fi + k3_fi / 2, fi_der + k3_b / 2) * self.dt
                k4_b = self.b_der(x + k3_x / 2, fi + k3_fi / 2, fi_der + k3_b / 2) * self.dt
                k4_x = (x_der + k3_a / 2) * self.dt
                k4_fi = (fi_der + k3_b / 2) * self.dt
                x_der += (k1_a + 2 * k2_a + 2 * k3_a + k4_a) / 6
                fi_der += (k1_b + 2 * k2_b + 2 * k3_b + k4_b) / 6
                x += (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
                fi += (k1_fi + 2 * k2_fi + 2 * k3_fi + k4_fi) / 6
            self.res_x = x
            self.res_fi = fi
            self.x_der = x_der
            self.fi_der = fi_der
      # The replacement of the initial conditions with received pendulum coordinates
        def up_date(self):
            self.x0_der = self.x_der
            self.fi0 = self.res_fi
            self.fi0_der = self.fi_der
            self.x0_der = self.x_der
class AnimationExample(QMainWindow):
    # Constructor, create the GUI
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.resize(700, 350)
        self.setWindowTitle('Sting Pendulum')
        
        # ProgressBar
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(70, 250, 200, 25)

        # Weight_1 (on the sting)
        self.paramM1 = QtWidgets.QLineEdit("2", self)
        self.paramM1.move(170, 30)
        self.labelM1 = QtWidgets.QLabel("Weight_1, kg:", self)
        self.labelM1.move(20, 30)

        # Weitght_2 (on the rod)
        self.paramM2 = QtWidgets.QLineEdit("15", self)
        self.paramM2.move(170, 80)
        self.labelM2 = QtWidgets.QLabel("Weight_2, kg:", self)
        self.labelM2.move(20, 80)

        # Sting Stiffness
        self.paramk = QtWidgets.QLineEdit("20", self)
        self.paramk.move(170, 130)
        self.labelk = QtWidgets.QLabel("Sting Stiffness, N/m:", self)
        QtWidgets.QLabel.setFixedWidth(self.labelk, 150)
        self.labelk.move(20, 130)

        # Rod length
        self.paraml = QtWidgets.QLineEdit("0.5", self)
        self.paraml.move(170, 180)
        self.labell = QtWidgets.QLabel("Rod length, m:", self)
        QtWidgets.QLabel.setFixedWidth(self.labell, 150)
        self.labell.move(20, 180)

        # Button Start
        QToolTip.setFont(QFont('SansSerif',10))
        self.buttonStart = QtWidgets.QPushButton("Start", self)
        self.buttonStart.setToolTip('Press the <b>Button Start</b> to start process of drawing')
        self.buttonStart.resize(self.buttonStart.sizeHint())
        self.buttonStart.move(20, 250)
        self.buttonStart.clicked.connect(self.doAction)
        self.buttonStart.clicked.connect(self.onStart)

        # Button Stop
        self.buttonStop = QtWidgets.QPushButton("Stop", self)
        self.buttonStop.setToolTip('Press the <b>Button Stop</b> to end this process')
        self.buttonStop.resize(self.buttonStop.sizeHint())
        self.buttonStop.move(20, 280)
        self.buttonStop.clicked.connect(self.onStop)
        
        # Button Quit
        #self.buttonQuit = QtWidgets.QPushButton("Quit", self)
        #self.buttonQuit.setToolTip('Press the <b>Button Quit</b> to close the window')
        #self.buttonQuit.resize(self.buttonStop.sizeHint())
        #self.buttonQuit.move(80, 250)
        #self.buttonQuit.clicked.connect(QCoreApplication.instance().quit)

        # LabelBar
        self.labelBar = QtWidgets.QLabel("", self)
        QtWidgets.QLabel.setFixedWidth(self.labelBar, 140)
        self.labelBar.move(136, 280)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10)  # it influences on the speed, but idk how it works
        self.timer.timeout.connect(self.onTimer)

        self.A = Pendulum()  # Creation of pendulum
        self.x1 = 0
        self.x2 = 0
        self.y2 = 0
        
        self.timer2 = QBasicTimer()
        self.step = 0
        
    def timerEvent(self, ev):
        if self.step >= 100:
            self.timer.stop()
            self.labelBar.setText("Finished")
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)
        
    #def closeEvent(self, ev):
        #reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yex| QMessageBox.No, QMessageBox.No)
        #if reply == QMessageBox.Yes:
        #    ev.accept()
        #else:
        #    ev.ignore()

    def paintEvent(self, ev):
        # Draw the current moment of the system
        qp = QPainter()
        qp.begin(self)
        qpp = QPainter()
        qpp.begin(self)
        qpp.setPen(QColor(68,134,3))
        qpp.setFont(QFont('SansSerif', 150)) #(Decorative)

        # Draw points from its coordinates
        p0 = QtCore.QPointF(500, 80)
        p1 = QtCore.QPointF(500 - self.x1, 80)
        p2 = QtCore.QPointF(500 - self.x2, 80 + self.y2)

        # Draw lines through that points
        qp.drawLine(p0, p1)
        qpp.drawLine(p1, p2)
        qpp.drawLine(p1, p2)

        qp.end()
        qpp.end()

    def onTimer(self):
        x = self.A.res_x  # The x-coordinate of the sting pendulum
        fi = self.A.res_fi  # The angle of deflection of the rod from the vertical
        self.x1 = 500.0 * x  # Calibration x from meters into pixels
        self.x2 = self.x1 - 500.0 * self.A.l * sin(fi)  # Calculation of rod pendulum's x-coordinate
        self.y2 = 500.0 * self.A.l * cos(fi)  # Calculation of rod pendulum's y-coordinate
        self.A.result()  # Calculation of the current position of the pendulum
        self.A.up_date()  # The update of the initial conditions

        # The redrawing of the window
        self.update()

    def onStart(self):
        m1_str = self.paramM1.text()
        self.m_1 = 0;
        m1 = float(str(m1_str))
        self.A.m_1 = m1

        m2_str = self.paramM2.text()
        self.m_2 = 0;
        m2 = float(str(m2_str))
        self.A.m_2 = m2

        k_str = self.paramk.text()
        self.k = 0;
        k = float(str(k_str))
        self.A.k = k

        l_str = self.paraml.text()
        self.l = 0;
        l = float(str(l_str))
        self.A.l = l

        x = self.A.res_x  # The x-coordinate of the sting pendulum
        fi = self.A.res_fi  # The angle of deflection of the rod from the vertical
        self.x1 = 500.0 * x  # Calibration x from meters to pixels
        self.x2 = self.x1 - 500.0 * sin(fi)  # Calculation of rod pendulum's x-coordinate
        self.y2 = 500.0 * cos(fi)  # Calculation of rod pendulum's y-coordinate

        self.timer.start()  # Start

    def onStop(self):
        self.timer.stop()
        
    def doAction(self):
        if self.timer2.isActive():
            self.timer2.stop()
        else:
            self.timer2.start(100, self)


app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
widget = AnimationExample()
#app.setWindowIcon(QIcon('web.png'))
widget.show()
sys.exit(app.exec_())