#coding = 'utf-8'
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from Panel import Panel
from ADBMonitor import ADBMonitor
from Window import Window
from ADBMonitor import ADBMonitor

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    adb = ADBMonitor()
    panel = Panel()
    win= Window(panel, adb)
    sys.exit(app.exec_())