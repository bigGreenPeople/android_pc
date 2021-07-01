import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebSockets import *
from PyQt5 import QtWebSockets, QtNetwork
import json


class MyServer(QObject):
    def __init__(self, parent, ex, status):
        super(QObject, self).__init__(parent)

        self.status = status
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
        self.ex.setConnected(True)
        self.status.showMessage('设备已连接')

    def sendMessage(self, message):
        self.clientConnection.sendTextMessage(message)

    def processTextMessage(self, message):
        if (self.clientConnection):
            message = json.loads(message)
            if message['type'] == "LAYOUT":
                layout_info = json.loads(message["message"])
                self.ex.saveLayout(layout_info)
                self.ex.updateActivitys(layout_info.keys())
            elif message['type'] == "GET_LAYOUT_IMG_END":
                self.ex.imgGetEnd()
                # 显示左后的布局
                # if len(layout_info.keys()) >= 1:
                #     self.ex.updateTree(layout_info[list(layout_info.keys())[0]])

    def processBinaryMessage(self, message):
        if (self.clientConnection):
            # print("接收图片")
            # 清空当前图片
            self.ex.saveImg(message)
            # self.ex.updateImg(message)
            # self.clientConnection.sendBinaryMessage(message)

    def socketDisconnected(self):
        if (self.clientConnection):
            self.clients.remove(self.clientConnection)
            self.clientConnection.deleteLater()
            self.ex.setConnected(False)
            self.status.showMessage('设备已断开')
