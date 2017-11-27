# coding:utf-8

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer


class Test(QWidget):
    def __init__(self):
        app = QApplication(sys.argv)

        super().__init__()
        self.init_desplay()
        self.init_hoge()
        self.hogehoge()

        self.timer = QTimer(self)
        self.main_timer = QTimer(self)
        time_list = [2000, 2000]
        #self.main_timer.timeout.connect(self.update)
        #self.timer.singleShot(2000, self.hogehoge)
        self.timer.timeout.connect(self.nyan)
        #self.timer.singleShot(2000, self.fugafuga)
        self.timer.start(sum(time_list))

        app.exec_()

    def nyan(self):
        self.count += 1
        if self.count % 2:
            self.hogehoge()
        else:
            self.fugafuga()

    def init_desplay(self):
        self.setWindowTitle("nitacad")
        self.resize(500, 500)
        self.i = 0
        self.count = 0
        print("hoge")

    def init_hoge(self):
        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(20)
        self.hoge = QLabel(None, self)
        self.hoge.move(100, 100)
        self.hoge.setFont(self.font)

    def hogehoge(self):
        self.i += 1
        print("nyan{0}".format(self.i))
        if self.i % 2:
            self.hoge.setText("hohoge{:<10}".format(self.i))
            self.show()
        else:
            self.hoge.setText("fuga{:<10}".format(self.i))
            self.show()

    def fugafuga(self):
        self.hoge.setText("114514!!{:<10}".format(self.i))
        self.show()

if __name__ == "__main__":
    Test()
