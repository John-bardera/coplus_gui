# coding:utf-8

import sys
import time
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
import beautiful
import get_real_time
import akashi_pass

akashi_login_bool = False


class Main(QWidget):
    def __init__(self):
        app = QApplication(sys.argv)
        super().__init__()
        self.init_info()
        self.init_fonts()
        self.init_ui()
        self.init_contents()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.replay)
        self.timer.start(6000)

        app.exec_()

    def init_info(self):
        if akashi_login_bool:
            akashi_pass.akashi_login()

        start_datetime = get_real_time.now_time_datetime()
        start_time = start_datetime.hour*60 + start_datetime.minute + 1
        start_linux_time = round(time.time())
        self.standard_linux_time = start_linux_time - start_time*60

        self.window_x = 1280
        self.window_y = 1024

        self.sanyou_to_list = ["西代・阪神梅田方面", "山陽姫路方面"]
        self.jr_to_list = ["加古川・姫路方面", "三ノ宮・大阪方面"]

        sanyou_diagram = beautiful.train_sanyou_get()
        self.sanyou_diagram1 = sanyou_diagram[0]
        self.sanyou_diagram2 = sanyou_diagram[1]
        jr_diagram = beautiful.train_jr_get()
        self.jr_diagram1 = jr_diagram[0]
        self.jr_diagram2 = jr_diagram[1]

        self.i = 0

    def init_ui(self):
        use_window_size = [self.window_x + 10, self.window_y + 10]
        self.resize(use_window_size[0], use_window_size[1])
        self.move(-6, 0)
        self.setWindowTitle("nitacad")

    def init_fonts(self):
        self.h1_font = QFont()
        self.h1_font.setFamily("M+ 2p")
        self.h1_font.setPointSize(40)

        self.timer_label_font = QFont()
        self.timer_label_font.setFamily("M+ 2p")
        self.timer_label_font.setPointSize(40)

        self.timer_font = QFont()
        self.timer_font.setFamily("M+ 2p")
        self.timer_font.setPointSize(80)

        self.to_place_font = QFont()
        self.to_place_font.setFamily("M+ 2p")
        self.to_place_font.setPointSize(40)

        self.text_font = QFont()
        self.text_font.setFamily("M+ 2p")
        self.text_font.setPointSize(60)

    def init_contents(self):
        self.h1 = QLabel(None, self)
        self.h1.move(10, 10)
        self.h1.setFont(self.h1_font)

        self.timer_label = QLabel(None, self)
        self.timer_label.move(self.window_x - 400, 15)
        self.timer_label.setFont(self.timer_label_font)

        self.timer_main = QLabel(None, self)
        self.timer_main.move(self.window_x - 350, 50)
        self.timer_main.setFont(self.timer_font)

        to_place_y1 = 280
        to_place_y2 = 480
        self.to_place1 = QLabel(None, self)
        self.to_place1.move(20, to_place_y1 - 40)
        self.to_place1.setFont(self.to_place_font)
        self.to_place2 = QLabel(None, self)
        self.to_place2.move(20, to_place_y2 - 40)
        self.to_place2.setFont(self.to_place_font)

        self.text1 = QLabel(None, self)
        self.text1.move(100, to_place_y1 + 100)
        self.text1.setFont(self.text_font)
        self.text2 = QLabel(None, self)
        self.text2.move(100, to_place_y2 + 100)
        self.text2.setFont(self.text_font)

        self.text1_time = QLabel(None, self)
        self.text1_time.move(950, to_place_y1 + 80)
        self.text1_time.setFont(self.text_font)
        self.text2_time = QLabel(None, self)
        self.text2_time.move(950, to_place_y2 + 80)
        self.text2_time.setFont(self.text_font)

    def str_num2_2(self, number):
        number = str(number)
        if len(number) == 1:
            number = "0" + number
        return number

    def next_train(self, diagram_list):
        now_goal_time = int((time.time() - self.standard_linux_time)/60 + 2)
        for part_diaguram in diagram_list:
            if part_diaguram[0] > now_goal_time:
                hour_minute_place_list = [int(part_diaguram[0]/60), part_diaguram[0]%60, part_diaguram[1]]
                return hour_minute_place_list

    def replay(self):
        self.i += 1
        if self.i % 2:
            desplay_place = "山陽"
            next_train_1 = self.next_train(self.sanyou_diagram1)
            next_train_2 = self.next_train(self.sanyou_diagram2)
            to_list = self.sanyou_to_list
        else:
            desplay_place = "JR"
            next_train_1 = self.next_train(self.jr_diagram1)
            next_train_2 = self.next_train(self.jr_diagram2)
            to_list = self.jr_to_list

        self.h1.setText("<h1> {0} </h1> <h2> 次の電車 </h2>".format(desplay_place))
        self.timer_label.setText("現在時刻")
        now_time = int((time.time() - self.standard_linux_time)/60)
        hour = self.str_num2_2(int(now_time/60))
        minute = self.str_num2_2(int(now_time%60))
        self.timer_main.setText("{0}:{1}".format(hour, minute))
        self.to_place1.setText("{0}{1}".format(to_list[0], " "*5))
        self.to_place2.setText(to_list[1])
        self.text1.setText("{0}行き{1}".format(next_train_1[2], " "*5))
        self.text2.setText("{0}行き{1}".format(next_train_2[2], " "*5))
        self.text1_time.setText("<h3> {0}:{1} </h3>".format(self.str_num2_2(next_train_1[0]), self.str_num2_2(next_train_1[1])))
        self.text2_time.setText("<h3> {0}:{1} </h3>".format(self.str_num2_2(next_train_2[0]), self.str_num2_2(next_train_2[1])))

        self.showMaximized()

if __name__ == "__main__":
    Main()
