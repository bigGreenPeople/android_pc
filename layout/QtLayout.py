import json

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWebSockets, QtNetwork
from PyQt5.QtWebSockets import *
from adbutils import adb

DEVICES_SOCKET = {}
ADB_DEVICE = None


class Example(QWidget):

    def __init__(self):
        super().__init__()
        # 类名
        self.nameLineEdit = None
        # 文本
        self.textLineEdit = None
        # id
        self.idLineEdit = None
        # 描述
        self.describeLineEdit = None

        self.serve = None
        # 设备列表
        self.selectDeviceComboBox = None
        # 窗口列表
        self.activityComboBox = None

        self.treeGrouplayout = None
        # 布局数
        self.tree = None

        # 手机图像
        self.pixMap = None
        self.imgeLabel = None

        # 启动app
        self.appNameEdit = None
        self.layoutInfo = None
        self.rate = 1

        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.time)
        self.timerExec = True
        self.timer.start(1000)

        # 图片
        self.img_list = []
        self.layout_list = {}

        self.initUI()
        self.connected = False

    def setConnected(self, connected):
        self.connected = connected

    def setServe(self, serve):
        self.serve = serve

    def time(self):
        devices = adb.devices()
        if len(DEVICES_SOCKET) != len(devices):
            for d in devices:
                if d not in DEVICES_SOCKET:
                    self.selectDeviceComboBox.clear()
                    DEVICES_SOCKET.clear()
                    for d in devices:
                        self.selectDeviceComboBox.addItem(d.serial)
                        DEVICES_SOCKET[d.serial] = None
                    break

    def selectDeviceOnActivated(self, text):
        """
        下拉选择设备
        :param text:
        :return:
        """
        self.timerExec = True

    def selectActivityOnActivated(self, text):
        """
        下拉选择activity
        :param text:
        :return:
        """
        index = self.activityComboBox.currentIndex()
        self.updateImg(self.img_list[index])
        self.updateTree(self.layout_list[text])

    def initUI(self):
        self.createGridGroupBox()
        self.createTreeGroupBox()
        self.createImgGroupBox()
        all_box = QHBoxLayout(self)
        # all_box.addWidget(self.gridGroupBox)

        # # 实例化QSplitter控件并设置初始为水平方向布局
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.verticalSplitter)
        splitter.addWidget(self.treeGroupBox)
        splitter.addWidget(self.imgGroupBox)
        # splitter.setSizes([2, 3, 6])
        #
        all_box.addWidget(splitter)
        self.setLayout(all_box)

        self.cneter()

        # self.statusBar().showMessage('就绪')
        self.setWindowTitle('Shark Android布局查看')
        # self.show()

    def createGridGroupBox(self):
        self.verticalSplitter = QSplitter(Qt.Vertical)
        self.gridInfoGroupBox = QGroupBox("控件信息")
        self.gridConnectGroupBox = QGroupBox("连接")
        self.gridOpGroupBox = QGroupBox("操作")

        self.verticalSplitter.addWidget(self.gridInfoGroupBox)
        self.verticalSplitter.addWidget(self.gridConnectGroupBox)
        self.verticalSplitter.addWidget(self.gridOpGroupBox)

        self.verticalSplitter.setSizes([100, 200, 280])

        # 添加控件界面的控件
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        nameLabel = QLabel("类名")
        self.nameLineEdit = QLineEdit("")
        layout.addWidget(nameLabel, 1, 0)
        layout.addWidget(self.nameLineEdit, 1, 1)

        textLabel = QLabel("文本")
        self.textLineEdit = QLineEdit("")
        layout.addWidget(textLabel, 2, 0)
        layout.addWidget(self.textLineEdit, 2, 1)

        idLabel = QLabel("ID")
        self.idLineEdit = QLineEdit("")
        layout.addWidget(idLabel, 3, 0)
        layout.addWidget(self.idLineEdit, 3, 1)

        describeLabel = QLabel("描述")
        self.describeLineEdit = QLineEdit("")
        layout.addWidget(describeLabel, 4, 0)
        layout.addWidget(self.describeLineEdit, 4, 1)

        # 添加操作界面的控件
        layout2 = QGridLayout()
        layout2.setSpacing(15)
        layout2.setAlignment(Qt.AlignTop)

        selectDeviceLabel = QLabel("选 择 设 备")
        selectDeviceLabel.setAlignment(Qt.AlignBottom)

        self.selectDeviceComboBox = QComboBox()
        self.selectDeviceComboBox.activated[str].connect(self.selectDeviceOnActivated)

        self.selectDeviceComboBox.clear()
        for d in adb.devices():
            self.selectDeviceComboBox.addItem(d.serial)
            DEVICES_SOCKET[d.serial] = None
        # self.selectDeviceComboBox.clicked.connect(self.selectDeviceEditTextChanged)

        layout2.addWidget(selectDeviceLabel, 1, 0, 1, 1)
        layout2.addWidget(self.selectDeviceComboBox, 1, 1, 1, 2)

        appNameLabel = QLabel("应 用 名 称")
        appNameLabel.setAlignment(Qt.AlignBottom)

        self.appNameEdit = QLineEdit("")

        layout2.addWidget(appNameLabel, 2, 0, 1, 1)
        layout2.addWidget(self.appNameEdit, 2, 1, 1, 2)

        start_app_layout_but = QPushButton('启动app')
        layout2.addWidget(start_app_layout_but, 3, 0, 1, 3)
        start_app_layout_but.clicked.connect(self.startApp)

        # 添加操作界面的控件
        layout3 = QGridLayout()
        layout3.setSpacing(15)
        layout3.setAlignment(Qt.AlignTop)

        get_android_layout_but = QPushButton('获取布局信息')
        layout3.addWidget(get_android_layout_but, 4, 0, 1, 3)
        # 设置点击事件
        get_android_layout_but.clicked.connect(self.getDeviceLayoutInfo)

        activityLabel = QLabel("选 择 窗 口")
        activityLabel.setAlignment(Qt.AlignBottom)

        self.activityComboBox = QComboBox()
        self.activityComboBox.activated[str].connect(self.selectActivityOnActivated)

        layout3.addWidget(activityLabel, 5, 0, 1, 1)
        layout3.addWidget(self.activityComboBox, 5, 1, 1, 2)
        self.gridInfoGroupBox.setMaximumSize(300, QWIDGETSIZE_MAX)
        self.gridOpGroupBox.setLayout(layout3)
        self.gridConnectGroupBox.setLayout(layout2)
        self.gridInfoGroupBox.setLayout(layout)

    def createTreeGroupBox(self):
        self.treeGroupBox = QGroupBox("布局结构")
        self.treeGrouplayout = QVBoxLayout()

        self.tree = QTreeWidget()
        # 设置列数
        # self.tree.setColumnCount(1)
        # 设置树形控件头部的标题
        self.tree.setHeaderHidden(True)

        # 设置树形控件的列的宽度
        self.tree.setColumnWidth(0, 160)

        self.treeGrouplayout.addWidget(self.tree)
        # self.treeScroll = QScrollArea()
        # self.treeScroll.setWidgetResizable(True)
        # self.treeScroll.setWidget(self.tree)

        # self.treeGrouplayout.addWidget(self.tree)
        self.treeGroupBox.setLayout(self.treeGrouplayout)

    def createImgGroupBox(self):
        self.imgGroupBox = QGroupBox("手机图像")
        layout = QVBoxLayout()
        self.imgeLabel = MyLabel()

        self.pixMap = QPixmap("img/test.png")

        # self.imgeLabel.setScaledContents(True)
        # self.pixMap = self.pixMap.scaled(1, 800, Qt.KeepAspectRatio,
        #                                  Qt.SmoothTransformation)
        # self.imgeLabel.setPixmap(self.pixMap)
        self.imgeLabel.resize(410, 0)

        ##创建一个滚动条
        self.imgeLabelscroll = QScrollArea()
        # self.imgeLabelscroll.setBackgroundRole(QPalette.Dark)
        self.imgeLabelscroll.setWidget(self.imgeLabel)
        layout.addWidget(self.imgeLabelscroll)
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

    def connectDevice(self):
        self.statusBar().showMessage("连接设备中...")

    def getDeviceLayoutInfo(self):
        # self.statusBar().showMessage("获取布局信息中...")
        if not self.connected:
            qMessageBox = QMessageBox(QMessageBox.Warning, "警告", "设备未连接")
            # button = qMessageBox.button(QMessageBox.Yes)
            # button.setText("了解")
            Qyes = qMessageBox.addButton(self.tr("了解"), QMessageBox.YesRole)

            qMessageBox.exec_()

            # qMessageBox.information(self, "Text", "设备未连接", QMessageBox.Yes)
            return
        send_message = {
            "id": 0,
            "type": "GET_LAYOUT_IMG",
            "message": ""
        }
        send_message = json.dumps(send_message)
        self.serve.sendMessage(send_message)

    def saveImg(self, bytes):
        """
        存储客户端图片
        :return:
        """
        self.img_list.append(bytes)

    def saveLayout(self, layout):
        self.layout_list = layout
        for key in self.layout_list:
            self.reSizeLayout(self.layout_list[key])
        # 选择第一个
        self.updateImg(self.img_list[0])
        self.updateTree(list(self.layout_list.values())[0])

    def updateImg(self, bytes):
        """
        更新图片
        :param bytes:
        :return:
        """
        self.pixMap.loadFromData(bytes)
        self.pixMap = self.pixMap.scaled(QWIDGETSIZE_MAX, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.imgeLabel.setPixmap(self.pixMap)
        self.imgeLabel.setGeometry(QRect(0, 0, self.pixMap.width(), 800))

    def imgGetEnd(self):
        """
        图片发送完毕接收布局信息
        :return:
        """
        send_message = {
            "id": 0,
            "type": "GET_LAYOUT",
            "message": ""
        }
        send_message = json.dumps(send_message)
        self.serve.sendMessage(send_message)

    def updateViewInfo(self, data):
        self.textLineEdit.setText("")
        self.idLineEdit.setText("")
        self.describeLineEdit.setText("")
        self.nameLineEdit.setText("")
        # print(data["id"])
        # print(f"{data['x']}  {data['y']} ---- {data['width']}  {data['height']}")

        self.nameLineEdit.setText(data["className"])
        if "text" in data.keys():
            self.textLineEdit.setText(data["text"])
        if "id" in data.keys() and data['id'] != -1:
            self.idLineEdit.setText(str(hex(data["id"])))
        if "description" in data.keys():
            self.describeLineEdit.setText(data["description"])

    def updateDevices(self):
        devices = adb.devices()
        self.selectDeviceComboBox.clear()
        DEVICES_SOCKET.clear()
        for d in devices:
            self.selectDeviceComboBox.addItem(d.serial)
            DEVICES_SOCKET[d.serial] = None

    def updateActivitys(self, activitys):
        self.activityComboBox.clear()
        [self.activityComboBox.addItem(activity) for activity in activitys]

    def getChild(self, root, layout_info):
        self_child = QTreeWidgetItem(root)
        self_child.setText(0, layout_info["className"])
        self_child.setData(0, Qt.UserRole, layout_info)

        # self_child.clicked.connect(self.onClicked)

        if "childList" not in layout_info.keys() or len(layout_info) == 0:
            return self_child
        for child_layout in layout_info['childList']:
            self.getChild(self_child, child_layout)
        return self_child

    def updateTree(self, layout_info):
        # 这个是我选中其中的一个分支进行右键清空操作时进行的处理
        # print(layout_info)
        self.layoutInfo = layout_info
        layout = QVBoxLayout()

        self.treeGrouplayout.removeWidget(self.tree)
        self.tree = QTreeWidget()
        # 设置树形控件头部的标题
        self.tree.setHeaderHidden(True)
        self.tree.clicked.connect(self.itemClick)

        self.treeScroll.setWidget(self.tree)

        self.root_child = self.getChild(self.tree, layout_info)
        self.tree.expandAll()

        self.imgeLabel.setLayoutInfo(layout_info, self.tree)

    def itemClick(self, item_child):
        item = self.tree.currentItem()

        data = item.data(0, Qt.UserRole)
        # print(data)
        self.updateViewInfo(data)
        self.imgeLabel.setClickedNode(data)

    def updateImgLayout(self):
        pass

    def reSizeLayout(self, layoutInfo):
        """
        调整布局大小
        :return:
        """
        if "childList" in layoutInfo.keys():
            list_ = layoutInfo["childList"]
            self.top_height = list_[-1]["height"]
            layoutInfo["childList"] = list_[:2 - 1]
        #         self.rate = self.pixMap.width() / float(layoutInfo["width"])
        self.rate = 499 / float(layoutInfo["width"])
        # 调整布局大小
        self.reSizeNode(layoutInfo)

    def reSizeNode(self, child_info):
        if "width" in child_info.keys() and "height" in child_info.keys() and \
                child_info["width"] != 0 and child_info["height"] != 0:
            child_info['x'] = float(child_info["x"]) * self.rate
            child_info['y'] = float(child_info["y"] - self.top_height) * self.rate
            child_info['width'] = float(child_info["width"]) * self.rate
            child_info['height'] = float(child_info["height"]) * self.rate

        if "childList" not in child_info.keys() or len(child_info) == 0:
            return

        for child_layout in child_info['childList']:
            self.reSizeNode(child_layout)

    def startApp(self):
        # 获得选择的设备
        selectDevice = self.selectDeviceComboBox.currentText()
        # 获得启动的app
        print(selectDevice)
        appName = self.appNameEdit.text()
        print(appName)
        ADB_DEVICE = adb.device(serial=selectDevice)
        print(ADB_DEVICE)
        # 点亮唤醒屏幕
        if not ADB_DEVICE.is_screen_on():
            ADB_DEVICE.keyevent("26")
            window_size = ADB_DEVICE.window_size()
            ADB_DEVICE.swipe(window_size[0] / 2, window_size[1] - 200,
                             window_size[0] / 2, 200, 0.2)

        ADB_DEVICE.app_start("com.shark.uiautoapitest")
        # shell_cmd = "cd /data/local/tmp/;su -c ./SharkInject -f -n " + appName
        # print(shell_cmd)
        # device_shell = ADB_DEVICE.shell(shell_cmd)
        # print(device_shell)


class MyLabel(QLabel):
    layout_info = {}
    rate = 1.00
    top_height = 0
    select_node = {}
    click_node = {}
    treeWidget = None

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def setLayoutInfo(self, layout_info, treeWidget):
        self.layout_info = layout_info
        # print(self.layout_info)
        self.treeWidget = treeWidget
        self.select_node = {}
        self.click_node = {}
        # # 调整布局大小
        # self.reSizeLayOut(self.layout_info)
        self.update()

    def setSelectNode(self, node):
        """
        画出选择的node节点
        :param node:
        :return:
        """
        self.select_node = node
        self.update()

    def setClickedNode(self, node):
        """
        画出点击的node节点
        :param node:
        :return:
        """
        self.click_node = node
        self.update()

    def paintClickedChild(self):
        """
        绘制选择节点
        :return:
        """
        if not self.click_node:
            return
        self.painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

        rect = QRect(self.click_node["x"], self.click_node["y"],
                     self.click_node["width"], self.click_node["height"])
        self.painter.drawRect(rect)

    def paintSelectChild(self):
        """
        绘制选择节点
        :return:
        """
        if not self.select_node:
            return
        self.painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))

        rect = QRect(self.select_node["x"], self.select_node["y"],
                     self.select_node["width"], self.select_node["height"])
        self.painter.drawRect(rect)

    def paintEvent(self, event):
        super().paintEvent(event)
        self.painter = QPainter()
        self.painter.begin(self)

        self.painter.setPen(QPen(Qt.red, 1, Qt.DotLine))
        # 自定义绘制方法
        self.drawRect(self.layout_info, self.painter)
        self.paintSelectChild()
        self.paintClickedChild()
        self.painter.end()

    def drawRect(self, child_info, qp):
        # 绘制
        if "width" in child_info.keys() and "height" in child_info.keys() and \
                child_info["width"] != 0 and child_info["height"] != 0:
            # print(
            #     f"{child_info['id']}  {child_info['x']}  {child_info['y']} ---- {child_info['width']}  {child_info['height']}")
            rect = QRect(child_info["x"], child_info["y"],
                         child_info["width"], child_info["height"])
            qp.drawRect(rect)

        if "childList" not in child_info.keys() or len(child_info) == 0:
            return

        for child_layout in child_info['childList']:
            self.drawRect(child_layout, qp)

        # 重写鼠标单击事件

    def mousePressEvent(self, event):  # 单击
        if not self.layout_info:
            return
        x = event.x()
        y = event.y()

        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            data = item.data(0, Qt.UserRole)
            if "width" in data.keys() and "height" in data.keys() and \
                    data["width"] != 0 and data["height"] != 0:
                if self.isInRect(x, y, data):
                    # print(data)
                    self.treeWidget.setCurrentItem(item)
                    from_item = self.treeWidget.indexFromItem(item)
                    self.treeWidget.clicked.emit(from_item)
                    # self.setSelectNode(data)
            iterator.__iadd__(1)

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if not self.layout_info:
            return
        x = event.x()
        y = event.y()
        # print(f"x:{x} y:{y}")
        self.clickNodeItem(x, y)

    def clickNodeItem(self, x, y):
        iterator = QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            data = item.data(0, Qt.UserRole)
            if "width" in data.keys() and "height" in data.keys() and \
                    data["width"] != 0 and data["height"] != 0:
                if self.isInRect(x, y, data):
                    # print(data)
                    # self.treeWidget.setCurrentItem(item)
                    # from_item = self.treeWidget.indexFromItem(item)
                    # self.treeWidget.clicked.emit(from_item)
                    self.setSelectNode(data)

            iterator.__iadd__(1)

    def isInRect(self, x, y, child_info):
        """
        判断xy是否在此节点中
        :param x:
        :param y:
        :param child_info: 节点信息
        :return: bool
        """
        # 计算存在child_info x的范围
        if "width" in child_info.keys() and "height" in child_info.keys() and \
                child_info["width"] != 0 and child_info["height"] != 0:
            if child_info['x'] < x < (child_info['x'] + child_info['width']) \
                    and child_info['y'] < y < (child_info['y'] + child_info['height']):
                return True
        return False
