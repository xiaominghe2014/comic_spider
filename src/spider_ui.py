#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: qt_ui.py
@time: 2018/4/18 下午5:18

"""
import os
import sys
import time

from PyQt5 import QtGui
from PyQt5.QtWidgets import *


class SpiderUi(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_main = QGridLayout()
        self.url_line = QLineEdit()
        self.url_btn = QPushButton("分析")
        self.down_line = QLineEdit()
        self.down_btn = QPushButton("浏览")
        self.down_title = QLabel('暂无')
        self.down_des = QLabel('暂无')
        self.down_des.setWordWrap(True)
        self.detail_list = QTextEdit()
        self.start_btn = QPushButton('开始下载')
        self.info = ''
        self.init_ui()

    def init_ui(self):
        self.setGeometry(400, 300, 800, 500)
        self.setWindowTitle('下载器')
        self.ui_layout()
        self.ui_url()
        self.ui_down()
        self.ui_des()
        self.ui_detail()
        self.ui_start()
        self.show()

    def ui_layout(self):
        self.setLayout(self.layout_main)

    def ui_url(self):
        des = QLabel('url地址:')
        self.url_line.setPlaceholderText('请输入 url地址')
        self.url_line.setTextMargins(200, 40, 0, 40)
        self.url_btn.clicked.connect(self.url_handler)
        self.layout_main.addWidget(des, 0, 0)
        self.layout_main.addWidget(self.url_line, 0, 1)
        self.layout_main.addWidget(self.url_btn, 0, 2)

    def ui_down(self):
        des = QLabel('下载路径:')
        self.down_line.setPlaceholderText('请点击浏览按钮选择本地地址')
        self.down_line.setTextMargins(200, 40, 0, 40)
        self.down_btn.clicked.connect(self.local_path)
        self.layout_main.addWidget(des, 1, 0)
        self.layout_main.addWidget(self.down_line, 1, 1)
        self.layout_main.addWidget(self.down_btn, 1, 2)

    def ui_des(self):
        title = QLabel('名称：')
        des = QLabel('简介: ')
        self.layout_main.addWidget(title, 2, 0)
        self.layout_main.addWidget(self.down_title, 2, 1, 1, 2)
        self.layout_main.addWidget(des, 3, 0)
        self.layout_main.addWidget(self.down_des, 3, 1, 1, 2)

    def ui_detail(self):
        # self.detail_list.setEnabled(False)
        self.detail_list.setReadOnly(True)
        self.layout_main.addWidget(self.detail_list, 4, 0, 1, 3)

    def ui_start(self):
        self.layout_main.addWidget(self.start_btn, 5, 2)
        self.start_btn.clicked.connect(self.on_start)

    def url_handler(self):
        url = self.url_line.text()
        print(url)

    def local_path(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        path = QFileDialog.getExistingDirectory(None, '请选择下载地址', current_dir)
        if path:
            self.down_line.setText(path)

    def on_start(self):
        self.next_detail(self.now())

    def next_detail(self, msg):
        self.detail_list.moveCursor(QtGui.QTextCursor.End)
        self.detail_list.append(msg)

    def closeEvent(self, event):
        self.question_dialog('', '确定退出程序吗?', event.accept, event.ignore)

    @staticmethod
    def question_dialog(title, msg, on_ok, on_cancel, txt_ok='确定', txt_cancel='取消'):
        dialog = QMessageBox(QMessageBox.NoIcon, title, msg)
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dialog.button(QMessageBox.Ok).setText(txt_ok)
        dialog.button(QMessageBox.Cancel).setText(txt_cancel)
        dialog.exec_()
        if txt_ok == dialog.clickedButton().text():
            on_ok()
        else:
            on_cancel()

    @staticmethod
    def now():
        return time.strftime("%H:%M:%S", time.localtime())


def main():
    app = QApplication(sys.argv)
    ui = SpiderUi()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


