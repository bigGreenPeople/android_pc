#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we create a more 
complicated window layout using
the QGridLayout manager. 

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""
import adbutils
import web_socket
from web_socket.shark_socket import SharkSocket
import json
import threading
import requests
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.createGridGroupBox()
        self.createTreeGroupBox()
        self.createImgGroupBox()
        all_box = QHBoxLayout(self)
        # all_box.addWidget(self.gridGroupBox)

        # 实例化QFrame控件
        # self.op_frame = QFrame()
        # self.op_frame.setFrameShape(QFrame.StyledPanel)
        # self.tree_frame = QFrame()
        # self.tree_frame.setFrameShape(QFrame.StyledPanel)
        # self.img_frame = QFrame()
        # self.img_frame.setFrameShape(QFrame.StyledPanel)
        # # 实例化QSplitter控件并设置初始为水平方向布局
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.verticalSplitter)
        splitter.addWidget(self.treeGroupBox)
        splitter.addWidget(self.imgGroupBox)
        # splitter.setSizes([2, 3, 6])
        #
        all_box.addWidget(splitter)
        self.setLayout(all_box)

        self.resize(1600, 900)
        self.cneter()

        self.setWindowTitle('Shark Android布局查看')
        self.show()

    def createGridGroupBox(self):
        self.verticalSplitter = QSplitter(Qt.Vertical)
        self.gridInfoGroupBox = QGroupBox("控件信息")
        self.gridConnectGroupBox = QGroupBox("连接")
        self.gridOpGroupBox = QGroupBox("操作")

        self.verticalSplitter.addWidget(self.gridInfoGroupBox)
        self.verticalSplitter.addWidget(self.gridConnectGroupBox)
        self.verticalSplitter.addWidget(self.gridOpGroupBox)

        self.verticalSplitter.setSizes([100, 200, 300])

        # 添加控件界面的控件
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        nameLabel = QLabel("类名")
        nameLineEdit = QLineEdit("")
        layout.addWidget(nameLabel, 1, 0)
        layout.addWidget(nameLineEdit, 1, 1)

        textLabel = QLabel("文本")
        textLineEdit = QLineEdit("")
        layout.addWidget(textLabel, 2, 0)
        layout.addWidget(textLineEdit, 2, 1)

        idLabel = QLabel("ID")
        idLineEdit = QLineEdit("")
        layout.addWidget(idLabel, 3, 0)
        layout.addWidget(idLineEdit, 3, 1)

        describeLabel = QLabel("描述")
        describeLineEdit = QLineEdit("")
        layout.addWidget(describeLabel, 4, 0)
        layout.addWidget(describeLineEdit, 4, 1)

        # 添加操作界面的控件
        layout2 = QGridLayout()
        layout2.setSpacing(15)
        layout2.setAlignment(Qt.AlignTop)

        selectDeviceLabel = QLabel("选 择 设 备")
        selectDeviceLabel.setAlignment(Qt.AlignBottom)

        selectDeviceComboBox = QComboBox()
        selectDeviceComboBox.addItem("192.168.0.1:5555")
        selectDeviceComboBox.addItem("192.168.0.2:5555")
        selectDeviceComboBox.addItem("192.168.0.3:5555")

        layout2.addWidget(selectDeviceLabel, 1, 0, 1, 1)
        layout2.addWidget(selectDeviceComboBox, 1, 1, 1, 2)

        appNameLabel = QLabel("应 用 名 称")
        appNameLabel.setAlignment(Qt.AlignBottom)

        appNameEdit = QLineEdit("")

        layout2.addWidget(appNameLabel, 2, 0, 1, 1)
        layout2.addWidget(appNameEdit, 2, 1, 1, 2)

        start_app_layout_but = QPushButton('启动app')
        layout2.addWidget(start_app_layout_but, 3, 0, 1, 3)

        # 添加操作界面的控件
        layout3 = QGridLayout()
        layout3.setSpacing(15)
        layout3.setAlignment(Qt.AlignTop)

        get_android_layout_but = QPushButton('获取布局信息')
        layout3.addWidget(get_android_layout_but, 4, 0, 1, 3)

        activityLabel = QLabel("选 择 窗 口")
        activityLabel.setAlignment(Qt.AlignBottom)

        activityComboBox = QComboBox()
        activityComboBox.addItem("Activity1")
        activityComboBox.addItem("Activity2")

        layout3.addWidget(activityLabel, 5, 0, 1, 1)
        layout3.addWidget(activityComboBox, 5, 1, 1, 2)
        # layout.addWidget(imgeLabel, 0, 2, 4, 1)
        # layout.setColumnStretch(1, 10)
        # self.gridGroupBox.resize(100, 100)
        self.gridInfoGroupBox.setMaximumSize(300, QWIDGETSIZE_MAX)
        self.gridOpGroupBox.setLayout(layout3)
        self.gridConnectGroupBox.setLayout(layout2)
        self.gridInfoGroupBox.setLayout(layout)
        # self.setWindowTitle('Basic Layout')

    def createTreeGroupBox(self):
        self.treeGroupBox = QGroupBox("布局结构")
        layout = QVBoxLayout()

        self.tree = QTreeWidget()
        # 设置列数
        self.tree.setColumnCount(1)
        # 设置树形控件头部的标题
        self.tree.setHeaderHidden(True)
        # 设置根节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, 'root')
        # 设置树形控件的列的宽度
        self.tree.setColumnWidth(0, 160)

        # 设置子节点1
        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'child1')

        cccchild1 = QTreeWidgetItem(child1)
        cccchild1.setText(0, 'cccchild1')
        # 设置子节点2
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        # 设置子节点3
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, 'child3')

        self.tree.addTopLevelItem(root)
        # self.setCentralWidget(self.tree)
        self.tree.expandAll()
        layout.addWidget(self.tree)
        self.treeGroupBox.setLayout(layout)

    def createImgGroupBox(self):
        self.imgGroupBox = QGroupBox("手机图像")
        layout = QVBoxLayout()
        imgeLabel = QLabel()

        pixMap = QPixmap("img/phone.png")
        imgeLabel.setPixmap(pixMap)
        layout.addWidget(imgeLabel)
        self.imgGroupBox.setLayout(layout)

    def cneter(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), 30)

    # 添加一个退出事件
    def closeEvent(self, event):
        event.accept()
        # sys.exit(0)
        thread.closeAll()

class SocketThread(threading.Thread):
    def run(self):
        print(f"开启Socket线程：  {threading.current_thread().name} \n")
        self.socket = SharkSocket(9873)
        print("结束Socket线程： " + threading.current_thread().name + "\n")

    def closeAll(self):
        self.socket.close_all()




if __name__ == '__main__':
    thread = SocketThread()
    thread.start()

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    # thread.join()
    # print("主线程退出")
