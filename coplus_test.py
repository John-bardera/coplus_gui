# coding:utf-8

import sys
import datetime
import time
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer


window_x = 1280
window_y = 1024


class test_main:
    def __init__(self, s1):
        self.timer = QTimer(self)
        self.w = QWidget()
        self.window_size = [window_x, window_y]
        self.use_window_size = [self.window_size[0] + 10, self.window_size[1] + 10]
        self.w.resize(self.use_window_size[0], self.use_window_size[1])
        self.w.move(-6, 0)
        self.w.setWindowTitle("nitacad")
        self.now_weather = QLabel(None, self.w)
        self.now_weather.setPixmap(QPixmap("./now_weather.gif"))
        self.font = QtGui.QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(20)
        self.hoge = QLabel(None, self.w)
        self.hoge.setText(s1)
        self.hoge.move(100, 100)
        self.hoge.setFont(self.font)
        self.i = 0
        self.timer.timeout.connect(self.replay())
        self.timer.start(5000)

    def show(self):
        self.w.showMaximized()

    def hogehoge(self):
        self.i += 1
        self.hoge.setText("hogehoge")
        self.hoge.move(200, 200)
        self.show()

    def fugafuga(self):
        self.i += 1
        self.hoge.setText("fugafuga")
        self.hoge.move(400, 400)
        self.show()


    def replay(self):
        if self.i % 2:
            self.fugafuga()
        else:
            self.hogehoge()

def shot(window_name):
    window = test_main(window_name)
    QTimer(5000, window.show())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop_size = app.primaryScreen().availableGeometry()
    height = desktop_size.height()
    width = desktop_size.width()

    main = test_main("nyan")


    #gui_main = test_main("hoge")
    #gui_main.show()
    #gui_hoge = test_main("nyan")
    #gui_hoge.show()


    #gui_main.hogehoge("nyan")
    #QTimer.singleShot(5000, lambda hoge=hoge, text="<h1> nyan </h1>": hoge_set(hoge, text))

    sys.exit(app.exec_())