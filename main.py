#!/usr/bin/python3
# -*- coding: utf-8 -*-

import adbutils
import web_socket
from web_socket.shark_socket import *
from web_socket.qt_websocket import *
from layout.QtLayout import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    serverObject = QWebSocketServer('My Socket', QWebSocketServer.NonSecureMode)

    ex = Example()
    server = MyServer(serverObject, ex)
    serverObject.closed.connect(app.quit)

    sys.exit(app.exec_())
