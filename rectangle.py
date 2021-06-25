from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import sys


class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.flag = False

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(675, 300)
        self.setWindowTitle('在label中绘制矩形')

        layout = QVBoxLayout()
        self.imgeLabel = QLabel()  # 重定义的label
        # self.imgeLabel.setGeometry(QRect(30, 30, 511, 541))
        self.pixMap = QPixmap("img/test.png")

        # self.imgeLabel.setScaledContents(True)
        self.pixMap = self.pixMap.scaled(self.size().height(), 850, Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
        # self.imgeLabel.setPixmap(self.pixMap)

        layout.addWidget(self.imgeLabel)

        q_rect = QRect(30, 30, 50, 50)
        painter = QPainter()
        painter.begin(self)
        # painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setPen(QColor(168, 34, 3))
        painter.setFont(QFont('SimSun', 20))

        self.setLayout(layout)
        self.show()

    def paintEvent(self, event):
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
        qp.drawRect(30,30,40,40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = Example()
    sys.exit(app.exec_())
