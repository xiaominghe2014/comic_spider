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
from PyQt5.QtCore import pyqtSignal
from get_comics import SpiderComic


class SpiderUi(QWidget):

    print_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.layout_main = QGridLayout()
        self.url_line = QLineEdit()
        self.url_btn = QPushButton("搜索")
        self.down_line = QLineEdit()
        self.down_btn = QPushButton("浏览")
        self.down_title = QLabel('暂无')
        self.down_title.setWordWrap(True)
        self.down_des = QLabel('暂无')
        self.down_des.setWordWrap(True)
        self.detail_list = QTextEdit()
        self.start_btn = QPushButton('开始下载')
        self.info = ''
        self.init_ui()
        self.print_signal.connect(self.next_detail)

    def emit_log(self, message):
        self.print_signal.emit(message)

    def init_ui(self):
        self.setGeometry(400, 300, 500, 500)
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
        des = QLabel('漫画名称:')
        self.url_line.setPlaceholderText('请输入 漫画名称')
        # self.url_line.setTextMargins(100, 40, 0, 40)
        self.url_btn.clicked.connect(self.url_handler)
        self.layout_main.addWidget(des, 0, 0)
        self.layout_main.addWidget(self.url_line, 0, 1)
        self.layout_main.addWidget(self.url_btn, 0, 2)

    def ui_down(self):
        des = QLabel('下载路径:')
        self.down_line.setPlaceholderText('请点击浏览按钮选择本地地址')
        # self.down_line.setTextMargins(100, 40, 0, 40)
        self.down_btn.clicked.connect(self.local_path)
        self.layout_main.addWidget(des, 1, 0)
        self.layout_main.addWidget(self.down_line, 1, 1)
        self.layout_main.addWidget(self.down_btn, 1, 2)

    def ui_des(self):
        title = QLabel('名称：')
        des = QLabel('简介: ')
        self.layout_main.addWidget(title, 2, 0, 1, 2)
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
        items = SpiderComic.get_list_by_book_name(url)
        res_name = ''
        res_des = '请选取一个具体搜索结果输入漫画名称进行下载'
        res_count = 0
        if 1 < len(items):
            for item in items:
                if 2 == len(item):
                    book_id = item[0]
                    book_name = item[1]
                    if book_name == url:
                        info = SpiderComic.get_list_video(book_id)
                        if 'brief_intrd' in info:
                            book_des = info['brief_intrd']
                            res_des = book_des
                        res_name = url
                        res_count = 1
                        break
                    else:
                        res_count += 1
                        res_name = '{}、{}'.format(res_name, book_name)
            if 1 != res_count:
                res_name = '\'{}\'共有{}个搜索结果:\n{}'.format(url, res_count, res_name)
            self.set_book_msg(res_name, res_des)
        else:
            if not url:
                self.next_detail('请先输入漫画名称')
            else:
                self.next_detail('未找到"{}"相应漫画信息'.format(url))

    def local_path(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        path = QFileDialog.getExistingDirectory(None, '请选择下载地址', current_dir)
        if path:
            self.down_line.setText(path)

    def on_start(self):
        spider = SpiderComic()
        path = self.down_line.text()
        if os.path.isdir(path):
            spider.set_save(path)
        spider.ui_call(self.set_book_msg)
        spider.down_comic(self.url_line.text(), self.emit_log)

    def set_book_msg(self, name, des):
        self.down_title.setText(name)
        self.down_des.setText(des)

    def next_detail(self, msg):
        self.detail_list.moveCursor(QtGui.QTextCursor.End)
        self.detail_list.append('{}:{}'.format(self.now(), msg))

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


