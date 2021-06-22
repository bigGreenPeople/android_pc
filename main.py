#!/usr/bin/python3
# -*- coding: utf-8 -*-

import adbutils
import web_socket
from web_socket.shark_socket import *
from web_socket.qt_websocket import *
from layout.QtLayout import *
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        # self.setGeometry(200, 200, 400, 200)
        self.setWindowTitle('创建主窗口')
        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage('就绪')
        ex = Example()
        self.setCentralWidget(ex)
        server = MyServer(serverObject, ex)

        self.resize(1200, 900)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    serverObject = QWebSocketServer('My Socket', QWebSocketServer.NonSecureMode)
    serverObject.closed.connect(app.quit)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
