from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import sys


class MyLabel(QLabel):
    layout_info = {}

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        # 自定义绘制方法
        self.drawRect(event, painter)
        painter.end()

    def drawRect(self, event, qp):
        # 设置画笔的颜色
        qp.setPen(QColor(168, 34, 3))
        # 设置字体
        qp.setFont(QFont('SimSun', 20))
        # 绘制文字
        qp.drawRect(30, 30, 40, 40)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(675, 300)
        self.setWindowTitle('在label中绘制矩形')

        layout = QVBoxLayout()
        self.imgeLabel = MyLabel()  # 重定义的label
        self.pixMap = QPixmap("img/test.png")

        self.pixMap = self.pixMap.scaled(self.size().height(), 850, Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
        self.imgeLabel.setPixmap(self.pixMap)
        layout.addWidget(self.imgeLabel)

        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = Example()
    sys.exit(app.exec_())
