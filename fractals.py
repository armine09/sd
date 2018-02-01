from PySide import QtCore, QtGui

import sys
from math import *


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__num = 0
        self.resize(500, 300)
        self.__fractal = "Koch"
        self.x, self.y = 0, 0
        self.w, self.h = 500, 300
        self.k = 1

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        if self.__fractal == "Koch":
            length = min(self.w, 6 * self.h / (sqrt(3))) - 20
            X1, Y1, X2, Y2 = self.x + (self.w - length) / 2, self.y + (self.h + length * sqrt(3) / 6) / 2, self.x + (self.w + length) / 2, self.y + (self.h + length * sqrt(3) / 6) / 2
            self.koh_curve(self.__num, X1, Y1, X2, Y2, painter)
        elif self.__fractal == "Ice_Rect":
            length = min(self.w, self.h * 3) - 20
            X1, Y1, X2, Y2 = self.x + (self.w - length) / 2, self.y + (self.h + length / 3) / 2, self.x + (self.w + length) / 2, self.y + (self.h + length / 3) / 2
            self.ice_rect(self.__num, X1, Y1, X2, Y2, painter)
        else:
            length = min(self.w, self.h * 3 / 2 - 50) - 20
            X1, Y1, X2, Y2 = self.x + (self.w - length) / 2, self.y + (self.h + 30) / 2, self.x + (self.w + length) / 2, self.y + (self.h + 30) / 2
            self.minkowski(self.__num, X1, Y1, X2, Y2, painter)
        painter.end()

    def koh_curve(self, n, x1, y1, x2, y2, painter):
        if n == 0:
            painter.drawLine(x1, y1, x2, y2)
            return
        else:
            a1, b1 = (2 * x1 + x2) / 3, (2 * y1 + y2) / 3
            a2, b2 = (x1 + 2 * x2) / 3, (y1 + 2 * y2) / 3
            a3, b3 = ((a2 - a1) - (b1 - b2) * sqrt(3)) / 2 + a1, ((a1 - a2) * sqrt(3) + (b2 - b1)) / 2 + b1
            self.koh_curve(n - 1, x1, y1, a1, b1, painter)
            self.koh_curve(n - 1, a1, b1, a3, b3, painter)
            self.koh_curve(n - 1, a3, b3, a2, b2, painter)
            self.koh_curve(n - 1, a2, b2, x2, y2, painter)

    def ice_rect(self, n, x1, y1, x2, y2, painter):
        if n == 0:
            painter.drawLine(x1, y1, x2, y2)
            return
        else:
            a1, b1 = (x2 + x1) / 2, (y1 + y2) / 2
            a2, b2 = a1 + (b1 - y1) * 2 / 3, b1 + (x1 - a1) * 2 / 3
            self.ice_rect(n - 1, x1, y1, a1, b1, painter)
            self.ice_rect(n - 1, a1, b1, a2, b2, painter)
            self.ice_rect(n - 1, a2, b2, a1, b1, painter)
            self.ice_rect(n - 1, a1, b1, x2, y2, painter)

    def minkowski(self, n, x1, y1, x2, y2, painter):
        if n == 0:
            painter.drawLine(x1, y1, x2, y2)
            return
        else:
            l = (x2 - x1) / 4
            a1, b1 = x1 + (x2 - x1) / 4, y1 + (y2 - y1) / 4
            a2, b2 = a1 + b1 - y1, b1 + x1 - a1
            a3, b3 = a2 + b1 - b2, b2 + a2 - a1
            a4, b4 = a3 + b2 - b3, b3 + a3 - a2
            a5, b5 = a4 + a4 - a3, b4 + b4 - b3
            a6, b6 = a5 + (b5 - b4), b5 + (a4 - a5)
            a7, b7 = a6 + b6 - b5, b6 + a5 - a6
            self.minkowski(n - 1, x1, y1, a1, b1, painter)
            self.minkowski(n - 1, a1, b1, a2, b2, painter)
            self.minkowski(n - 1, a2, b2, a3, b3, painter)
            self.minkowski(n - 1, a3, b3, a4, b4, painter)
            self.minkowski(n - 1, a4, b4, a5, b5, painter)
            self.minkowski(n - 1, a5, b5, a6, b6, painter)
            self.minkowski(n - 1, a6, b6, a7, b7, painter)
            self.minkowski(n - 1, a7, b7, x2, y2, painter)

    def setValue(self, val):
        self.__num = val
        self.repaint()

    def setFractal(self, number):
        if number == 0:
            self.__fractal = "Koch"
        elif number == 1:
            self.__fractal = "Minkowsky"
        else:
            self.__fractal = "Ice_Rect"
        self.repaint()

    def mousePressEvent(self, event):
        self.__Xmouse = event.pos().x()
        self.__Ymouse = event.pos().y()
        self.__Xsaved = self.x
        self.__Ysaved = self.y

    def mouseMoveEvent(self, event):
        self.x = self.__Xsaved + event.pos().x() - self.__Xmouse
        self.y = self.__Ysaved + event.pos().y() - self.__Ymouse
        self.repaint()

    def wheelEvent(self, event):
        old_k = self.k
        self.k *= (1 + event.delta() / 1000)
        if self.k < 0:
            self.k = 0
        if old_k != 0:
            self.y -= (self.k / old_k - 1) * (Window.height() / 2 - self.y)
            self.x -= (self.k / old_k - 1) * (Window.width() / 2 - self.x)
            self.w = self.w / old_k * self.k
            self.h = self.h / old_k * self.k
        self.repaint()    


class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.resize(500, 300)
        self.setMinimumSize(300, 200)
        self.setWindowTitle("Koh")
        self.Widget = MyWidget(self)

    def resizeEvent(self, event):
        size = (self.Widget.width(), self.Widget.height())        
        self.Widget.setGeometry(0, 0, self.width(), self.height())
        self.Widget.x = self.Widget.x + (self.Widget.width() - size[0]) / 2
        self.Widget.y = self.Widget.y + (self.Widget.height() - size[1]) / 2


X = 500
Y = 300
app = QtGui.QApplication(sys.argv)
Window = MyWindow()
SpinBox = QtGui.QSpinBox(Window)
SpinBox.setGeometry(10, 10, 100, 30)
QtCore.QObject.connect(SpinBox, QtCore.SIGNAL("valueChanged(int)"), Window.Widget.setValue)
ComboBox = QtGui.QComboBox(Window)
ComboBox.setGeometry(120, 10, 150, 30)
ComboBox.addItems(["Koch", "Minkowski", "Ice Rect"])
QtCore.QObject.connect(ComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), Window.Widget.setFractal)
Window.show()
app.exec_()