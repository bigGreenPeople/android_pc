import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebSockets import *
from PyQt5 import QtWebSockets, QtNetwork
import json


class MyServer(QObject):
    def __init__(self, parent, ex):
        super(QObject, self).__init__(parent)

        self.ex = ex
        self.clients = []
        self.server = QWebSocketServer(parent.serverName(), parent.secureMode(), parent)
        if self.server.listen(QtNetwork.QHostAddress.AnyIPv4, 9873):
            # 成功打印相关信息
            print('Connected: ' + self.server.serverName() + ' : ' + self.server.serverAddress().toString() + ':' + str(
                self.server.serverPort()))
        else:
            print('error')
        self.server.newConnection.connect(self.onNewConnection)

        print(self.server.isListening())

    def onNewConnection(self):
        self.clientConnection = self.server.nextPendingConnection()
        self.clientConnection.textMessageReceived.connect(self.processTextMessage)

        self.clientConnection.binaryMessageReceived.connect(self.processBinaryMessage)
        self.clientConnection.disconnected.connect(self.socketDisconnected)

        self.clients.append(self.clientConnection)

    def sendMessage(self, message):
        self.clientConnection.sendTextMessage(message)

    def processTextMessage(self, message):
        if (self.clientConnection):
            message = json.loads(message)
            if (message['type'] == "LAYOUT"):
                layout_info = json.loads(message["message"])
                self.ex.updateActivitys(layout_info.keys())
                if len(layout_info.keys()) >= 1:
                    self.ex.updateTree(layout_info[list(layout_info.keys())[0]])

    def processBinaryMessage(self, message):
        if (self.clientConnection):
            self.ex.updateImg(message)
            # self.clientConnection.sendBinaryMessage(message)

    def socketDisconnected(self):
        if (self.clientConnection):
            self.clients.remove(self.clientConnection)
            self.clientConnection.deleteLater()
