import sys
from PyQt5 import QtWidgets, QtCore

q_application = QtWidgets.QApplication(sys.argv)
q_widget = QtWidgets.QWidget()
q_widget.resize(320, 240)
q_widget.setWindowTitle("Hello PyQt5")

q_widget.show()
sys.exit(q_application.exec_())
