#coding = 'utf-8'
import sys

from PyQt5 import QtWidgets

from Panel import Panel
from Window import Window
from ADBMonitor import ADBMonitor
from Json_process import Json_process

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    adb = ADBMonitor()
    panel = Panel()
    json_pro = Json_process()
    win= Window(panel, adb, json_pro)
    sys.exit(app.exec_())