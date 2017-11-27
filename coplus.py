# coding:utf-8

import sys
import datetime
import time
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import beautiful
import get_real_time
import akashi_pass

# config
akashi_pass.akashi_login()

window_x = 1280
window_y = 1024

sanyou_to_list = ["西代・阪神梅田方面", "山陽姫路方面"]
jr_to_list = ["加古川・姫路方面", "三ノ宮・大阪方面"]

sanyou_diagram = beautiful.train_sanyou_get()
sanyou_diagram1 = sanyou_diagram[0]
sanyou_diagram2 = sanyou_diagram[1]
jr_diagram = beautiful.train_jr_get()
jr_diagram1 = jr_diagram[0]
jr_diagram2 = jr_diagram[1]


def str_num2_2(number):
    if len(number) == 1:
        number = "0" + number
    return number


class GuiMain:
    def init_ul(self):
        w = QWidget()
        window_size = [window_x, window_y]
        use_window_size = [window_size[0]+10, window_size[1]+10]
        w.resize(use_window_size[0], use_window_size[1])
        w.move(-6, 0)
        w.setWindowTitle("nitacad")
        return w

    def train_desplay(self, window):
        h1_font = QtGui.QFont()
        h1_font.setFamily("Arial")
        h1_font.setPointSize(40)
        h1 = QLabel(None, window)
        h1.move(10, 10)
        h1.setFont(h1_font)

        timer_label_font = QtGui.QFont()
        timer_label_font.setFamily("Arial")
        timer_label_font.setPointSize(40)
        timer_label = QLabel(None, window)
        timer_label.move(window_x - 350, 15)
        timer_label.setFont(timer_label_font)

        timer_font = QtGui.QFont()
        timer_font.setFamily("Arial")
        timer_font.setPointSize(80)
        timer = QLabel(None, window)
        timer.move(window_x - 300, 30)
        timer.setFont(timer_font)

        to_place_font = QtGui.QFont()
        to_place_font.setFamily("Arial")
        to_place_font.setPointSize(40)

        to_place1 = QLabel(None, window)
        to_place1.move(20, 280)
        to_place1.setFont(to_place_font)
        to_place2 = QLabel(None, window)
        to_place2.move(20, 480)
        to_place2.setFont(to_place_font)

        text_font = QtGui.QFont()
        text_font.setFamily("Arial")
        text_font.setPointSize(60)
        text1 = QLabel(None, window)
        text1.move(100, 340)
        text1.setFont(text_font)
        text2 = QLabel(None, window)
        text2.move(100, 540)
        text2.setFont(text_font)

        return [h1, timer_label, timer, to_place1, to_place2, text1, text2]


def next_train(diagram_dict, now_hour=str(get_real_time.now_time_datetime().hour)):
    now_minute = str(get_real_time.now_time_datetime().minute + 1)
    if now_hour not in diagram_dict:
        while True:
            if now_hour not in diagram_dict:
                now_hour = str(int(now_hour) + 1)
            else:
                break
        return [now_hour, diagram_dict[now_hour][0]]
    this_hour_list = list(map(lambda target: target[1], diagram_dict[now_hour]))
    for i in range(1, len(this_hour_list)+1):
        if int(now_minute) >= int(this_hour_list[-i]):
            if i == 1:
                return [str(int(now_hour) + 1), diagram_dict[str(int(now_hour) + 1)][0]]
            else:
                return [now_hour, diagram_dict[str(int(now_hour))][-(i - 1)]]
        elif i == len(this_hour_list):
            return [now_hour, diagram_dict[str(int(now_hour))][-i]]
        else:
            continue



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window1 = init_ul()
    window2 = init_ul()


    def reset(window, place):
        contents = train_desplay(window)

        h1 = contents[0]
        timer_label = contents[1]
        timer = contents[2]
        to_place1 = contents[3]
        to_place2 = contents[4]
        text1 = contents[5]
        text2 = contents[6]

        if place == "jr":
            desplay_place = "JR"
            next_train_1 = next_train(jr_diagram1)
            next_train_2 = next_train(jr_diagram2)
            to_list = jr_to_list
        if place == "sanyou":
            desplay_place = "山陽"
            next_train_1 = next_train(sanyou_diagram1)
            next_train_2 = next_train(sanyou_diagram2)
            to_list = sanyou_to_list
        h1.setText("<h1> {0} </h1> <h2> 次の電車 </h2>".format(desplay_place))
        timer_label.setText("現在時刻")
        timer.setText(str_num2_2(str(get_real_time.now_time_datetime().hour)) + ":" + str_num2_2(str(get_real_time.now_time_datetime().minute)))
        to_place1.setText(to_list[0])
        to_place2.setText(to_list[1])
        text1.setText(
            "{0}行き{1}{2}:{3}".format(next_train_1[1][0], " " * 1, next_train_1[0], str_num2_2(next_train_1[1][1])))
        text2.setText(
            "{0}行き{1}{2}:{3}".format(next_train_2[1][0], " " * 1, next_train_2[0], str_num2_2(next_train_2[1][1])))

        window.showMaximized()

    while True:
        reset(window1, "ir")
        #QTimer.singleShot(5000, reset(window1, "jr"))
        #sys.exit(app.exec_())
        #QTimer.singleShot(5000, reset(window2, "sanyou"))

        sys.exit(app.exec_())

"""
        map_list_text_and_evals = [[h1, "<h1> {0} </h1> <h2> 次の電車 </h2>".format(desplay_place)],
                                   [timer_label, "現在時刻"],
                                   [timer, str_num2_2(str(get_real_time.now_time_datetime().hour)) + ":" + str_num2_2(str(get_real_time.now_time_datetime().minute))],
                                   [to_place1, to_list[0]],
                                   [to_place2, to_list[1]],
                                   [text1, "{0}行き{1}{2}:{3}".format(next_train_1[1][0], " " * 4, next_train_1[0],str_num2_2(next_train_1[1][1]))],
                                   [text2, "{0}行き{1}{2}:{3}".format(next_train_2[1][0], " " * 4, next_train_2[0],str_num2_2(next_train_2[1][1]))]]
        def hoge_set(hoge, text):
            hoge.setText(text)
        QTimer.singleShot(5000, lambda hoge=h1, text="hoge": hoge_set(hoge, text))#map(lambda text_and_eval: text_and_eval[0].setText(text_and_eval[1]), map_list_text_and_evals))
        #h1.setText("<h1> {0} </h1> <h2> 次の電車 </h2>".format(desplay_place))
        timer_label.setText("現在時刻")
        timer.setText(str_num2_2(str(get_real_time.now_time_datetime().hour)) + ":" + str_num2_2(
            str(get_real_time.now_time_datetime().minute)))
        to_place1.setText(to_list[0])
        to_place2.setText(to_list[1])
        text1.setText(
            "{0}行き{1}{2}:{3}".format(next_train_1[1][0], " " * 4, next_train_1[0], str_num2_2(next_train_1[1][1])))
        text2.setText(
            "{0}行き{1}{2}:{3}".format(next_train_2[1][0], " " * 4, next_train_2[0], str_num2_2(next_train_2[1][1])))

        window.showMaximized()

        info = reset_text("jr")
        desplay_place = info[0]
        next_train_1 = info[1]
        next_train_2 = info[2]
        to_list = info[3]
        map_list_text_and_evals = [[h1, "<h1> {0} </h1> <h2> 次の電車 </h2>".format(desplay_place)],
                                   [timer_label, "現在時刻"],
                                   [timer, str_num2_2(str(get_real_time.now_time_datetime().hour)) + ":" + str_num2_2(str(get_real_time.now_time_datetime().minute))],
                                   [to_place1, to_list[0]],
                                   [to_place2, to_list[1]],
                                   [text1, "{0}行き{1}{2}:{3}".format(next_train_1[1][0], " " * 4, next_train_1[0], str_num2_2(next_train_1[1][1]))],
                                   [text2, "{0}行き{1}{2}:{3}".format(next_train_2[1][0], " " * 4, next_train_2[0],str_num2_2(next_train_2[1][1]))]]

        #QTimer.singleShot(5000, map(lambda text_and_eval: text_and_eval[0].setText(text_and_eval[1]), map_list_text_and_evals))
        QTimer.singleShot(5000, lambda hoge=h1, text="hoge": hoge_set(hoge, text))#map(lambda text_and_eval: text_and_eval[0].setText(text_and_eval[1]), map_list_text_and_evals))
        #h1.setText("<h1> {0} </h1> <h2> 次の電車 </h2>".format(desplay_place))
        timer_label.setText("現在時刻")
        timer.setText(str_num2_2(str(get_real_time.now_time_datetime().hour)) + ":" + str_num2_2(
            str(get_real_time.now_time_datetime().minute)))
        to_place1.setText(to_list[0])
        to_place2.setText(to_list[1])
        text1.setText(
            "{0}行き{1}{2}:{3}".format(next_train_1[1][0], " " * 4, next_train_1[0], str_num2_2(next_train_1[1][1])))
        text2.setText(
            "{0}行き{1}{2}:{3}".format(next_train_2[1][0], " " * 4, next_train_2[0], str_num2_2(next_train_2[1][1])))


        window.showMaximized()

        """"""
        h1.setText("<h1> {0} </h1> <h2> 次の電車 </h2>".format(desplay_place))
        timer_label.setText("現在時刻")
        timer.setText(str_num2_2(str(get_real_time.now_time_datetime().hour)) + ":" + str_num2_2(str(get_real_time.now_time_datetime().minute)))
        to_place1.setText(to_list[0])
        to_place2.setText(to_list[1])
        text1.setText("{0}行き{1}{2}:{3}".format(next_train_1[1][0], " " * 4, next_train_1[0], str_num2_2(next_train_1[1][1])))
        text2.setText("{0}行き{1}{2}:{3}".format(next_train_2[1][0], " " * 4, next_train_2[0], str_num2_2(next_train_2[1][1])))
        """

"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    """"""desktop_size = app.primaryScreen().availableGeometry()
    height = desktop_size.height()
    width = desktop_size.width()""""""

    window = init_ul()
    now_weather = QLabel(None, window)
    now_weather.setPixmap(QPixmap("./now_weather.gif"))
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(20)
    hoge = QLabel(None, window)
    hoge.setText("<h1> hoge </h1>")
    hoge.move(100, 100)
    hoge.setFont(font)
    window.showMaximized()

    def hoge_set(hoge, text):
        hoge.setText(text)
        hoge.move(200, 200)


    QTimer.singleShot(5000, lambda hoge=hoge, text="<h1> nyan </h1>": hoge_set(hoge, text))
    window.showMaximized()
    sys.exit(app.exec_())
"""
