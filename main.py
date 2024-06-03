import datetime
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from UI.main import Ui_Form
from utils.check import check_first_time, check_textEdit, check_button


class UI_Logic_Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UI_Logic_Window, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 绑定信号槽
        self.init_slots()

        # 检查是否为第一次使用该软件，并作相应处理
        check_first_time(self)

        # 初始化一个 QT 的定时器并绑定到 update_time 函数中，使其每秒更新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) # 1000 即为 1 秒，若需要 1 分钟更新一次可设置 60 * 1000，其它同理
        self.update_time()

        # 打开软件时更新 textEdit 的内容并检查 button 是否可用
        check_textEdit(self, "init")
        check_button(self)


    def init_slots(self):
        # button 按钮每次点击触发 clock_in 函数
        self.ui.button_clock_in.clicked.connect(self.clock_in)


    def clock_in(self):
        '''
        current_time：从系统时间中获取并格式化为 2024-06-03 15：00：00 的样式
        用 open 写入转换为 16 进制后的信息，每次点击按钮都即时将数据写入数据库，
        同时更新textEdit 和 button 的状态
        '''
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = "已于 " + str(current_time) + " 完成打卡\n"
        hex_message = message.encode().hex()
        with open('database', 'a') as f:
            f.write(hex_message)
        check_textEdit(self, "update")
        check_button(self)
        # 为了防止点击过快产生的奇怪bug，设置一个 0.2 秒的停顿
        time.sleep(0.2)


    def update_time(self):
        '''
        更新为当前系统时间，并显示在 label_time 中
        '''
        local_time = datetime.datetime.now()
        formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
        self.ui.label_time.setText(formatted_time)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_Logic_Window()
    ui.show()
    sys.exit(app.exec_())