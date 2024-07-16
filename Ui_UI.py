# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\data\test code\python\qt\lcd_debug\UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.screen_index = QtWidgets.QComboBox(self.centralwidget)
        self.screen_index.setGeometry(QtCore.QRect(150, 70, 87, 22))
        self.screen_index.setCurrentText("")
        self.screen_index.setObjectName("screen_index")
        self.fps_list = QtWidgets.QComboBox(self.centralwidget)
        self.fps_list.setGeometry(QtCore.QRect(150, 120, 87, 22))
        self.fps_list.setObjectName("fps_list")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 70, 81, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 110, 81, 31))
        self.label_2.setObjectName("label_2")
        self.hs_mode = QtWidgets.QCheckBox(self.centralwidget)
        self.hs_mode.setGeometry(QtCore.QRect(390, 120, 91, 19))
        self.hs_mode.setObjectName("hs_mode")
        self.code_pack = QtWidgets.QCheckBox(self.centralwidget)
        self.code_pack.setGeometry(QtCore.QRect(480, 120, 91, 19))
        self.code_pack.setObjectName("code_pack")
        self.sync_te = QtWidgets.QCheckBox(self.centralwidget)
        self.sync_te.setEnabled(False)
        self.sync_te.setGeometry(QtCore.QRect(560, 120, 91, 19))
        self.sync_te.setInputMethodHints(QtCore.Qt.ImhNone)
        self.sync_te.setCheckable(True)
        self.sync_te.setObjectName("sync_te")
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setEnabled(False)
        self.checkBox_4.setGeometry(QtCore.QRect(280, 120, 101, 19))
        self.checkBox_4.setObjectName("checkBox_4")
        self.adb_devices_Info = QtWidgets.QComboBox(self.centralwidget)
        self.adb_devices_Info.setGeometry(QtCore.QRect(150, 20, 87, 22))
        self.adb_devices_Info.setCurrentText("")
        self.adb_devices_Info.setObjectName("adb_devices_Info")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(60, 20, 81, 31))
        self.label_6.setObjectName("label_6")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(50, 580, 861, 371))
        self.groupBox.setObjectName("groupBox")
        self.debug_window = QtWidgets.QTextBrowser(self.groupBox)
        self.debug_window.setGeometry(QtCore.QRect(10, 20, 721, 341))
        self.debug_window.setObjectName("debug_window")
        self.clear_debug_window = QtWidgets.QPushButton(self.groupBox)
        self.clear_debug_window.setGeometry(QtCore.QRect(750, 40, 93, 28))
        self.clear_debug_window.setObjectName("clear_debug_window")
        self.get_code_Button = QtWidgets.QPushButton(self.groupBox)
        self.get_code_Button.setEnabled(True)
        self.get_code_Button.setGeometry(QtCore.QRect(750, 90, 93, 28))
        self.get_code_Button.setObjectName("get_code_Button")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(50, 260, 861, 311))
        self.groupBox_2.setObjectName("groupBox_2")
        self.r_code = QtWidgets.QTextEdit(self.groupBox_2)
        self.r_code.setGeometry(QtCore.QRect(10, 20, 721, 281))
        self.r_code.setObjectName("r_code")
        self.replace_code = QtWidgets.QPushButton(self.groupBox_2)
        self.replace_code.setGeometry(QtCore.QRect(750, 90, 93, 28))
        self.replace_code.setObjectName("replace_code")
        self.transform_code = QtWidgets.QPushButton(self.groupBox_2)
        self.transform_code.setGeometry(QtCore.QRect(750, 40, 93, 28))
        self.transform_code.setObjectName("transform_code")
        self.restore_code = QtWidgets.QPushButton(self.groupBox_2)
        self.restore_code.setGeometry(QtCore.QRect(750, 140, 93, 28))
        self.restore_code.setObjectName("restore_code")
        self.restore_all_code = QtWidgets.QPushButton(self.groupBox_2)
        self.restore_all_code.setEnabled(False)
        self.restore_all_code.setGeometry(QtCore.QRect(750, 190, 93, 28))
        self.restore_all_code.setObjectName("restore_all_code")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(920, 50, 971, 381))
        self.groupBox_3.setObjectName("groupBox_3")
        self.listWidget = QtWidgets.QListWidget(self.groupBox_3)
        self.listWidget.setGeometry(QtCore.QRect(10, 20, 831, 351))
        self.listWidget.setObjectName("listWidget")
        self.open_dir_button = QtWidgets.QPushButton(self.groupBox_3)
        self.open_dir_button.setGeometry(QtCore.QRect(860, 90, 93, 28))
        self.open_dir_button.setObjectName("open_dir_button")
        self.import_file_button = QtWidgets.QPushButton(self.groupBox_3)
        self.import_file_button.setGeometry(QtCore.QRect(860, 150, 93, 28))
        self.import_file_button.setObjectName("import_file_button")
        self.import_file_button_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.import_file_button_2.setEnabled(False)
        self.import_file_button_2.setGeometry(QtCore.QRect(860, 210, 93, 28))
        self.import_file_button_2.setObjectName("import_file_button_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(920, 450, 971, 501))
        self.groupBox_4.setObjectName("groupBox_4")
        self.preview_window = QtWidgets.QTextEdit(self.groupBox_4)
        self.preview_window.setGeometry(QtCore.QRect(10, 20, 831, 471))
        self.preview_window.setObjectName("preview_window")
        self.json_to_code_button = QtWidgets.QPushButton(self.groupBox_4)
        self.json_to_code_button.setGeometry(QtCore.QRect(860, 80, 93, 28))
        self.json_to_code_button.setObjectName("json_to_code_button")
        self.save_file_button = QtWidgets.QPushButton(self.groupBox_4)
        self.save_file_button.setGeometry(QtCore.QRect(860, 180, 93, 28))
        self.save_file_button.setObjectName("save_file_button")
        self.save_as_button = QtWidgets.QPushButton(self.groupBox_4)
        self.save_as_button.setEnabled(False)
        self.save_as_button.setGeometry(QtCore.QRect(860, 230, 93, 28))
        self.save_as_button.setObjectName("save_as_button")
        self.restore_code_in_json = QtWidgets.QPushButton(self.groupBox_4)
        self.restore_code_in_json.setEnabled(False)
        self.restore_code_in_json.setGeometry(QtCore.QRect(860, 130, 93, 28))
        self.restore_code_in_json.setObjectName("restore_code_in_json")
        self.enable_debug_log_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.enable_debug_log_checkbox.setGeometry(QtCore.QRect(280, 70, 131, 19))
        self.enable_debug_log_checkbox.setObjectName("enable_debug_log_checkbox")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(280, 20, 151, 31))
        self.label_4.setObjectName("label_4")
        self.all_cmd_type_state = QtWidgets.QComboBox(self.centralwidget)
        self.all_cmd_type_state.setGeometry(QtCore.QRect(440, 20, 87, 22))
        self.all_cmd_type_state.setObjectName("all_cmd_type_state")
        self.all_cmd_type_state.addItem("")
        self.all_cmd_type_state.addItem("")
        self.all_cmd_type_state.addItem("")
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setGeometry(QtCore.QRect(50, 150, 861, 101))
        self.groupBox_6.setObjectName("groupBox_6")
        self.cmd_type_list = QtWidgets.QComboBox(self.groupBox_6)
        self.cmd_type_list.setGeometry(QtCore.QRect(100, 20, 631, 22))
        self.cmd_type_list.setObjectName("cmd_type_list")
        self.search_lineedit = QtWidgets.QLineEdit(self.groupBox_6)
        self.search_lineedit.setGeometry(QtCore.QRect(750, 20, 91, 21))
        self.search_lineedit.setObjectName("search_lineedit")
        self.label_3 = QtWidgets.QLabel(self.groupBox_6)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 201, 31))
        self.label_3.setObjectName("label_3")
        self.dump_code_enable = QtWidgets.QPushButton(self.groupBox_6)
        self.dump_code_enable.setGeometry(QtCore.QRect(210, 60, 93, 28))
        self.dump_code_enable.setObjectName("dump_code_enable")
        self.dump_code_disable = QtWidgets.QPushButton(self.groupBox_6)
        self.dump_code_disable.setGeometry(QtCore.QRect(320, 60, 93, 28))
        self.dump_code_disable.setObjectName("dump_code_disable")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(670, 20, 211, 31))
        self.label_5.setObjectName("label_5")
        self.groupBox_4.raise_()
        self.groupBox_3.raise_()
        self.screen_index.raise_()
        self.fps_list.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.hs_mode.raise_()
        self.code_pack.raise_()
        self.sync_te.raise_()
        self.checkBox_4.raise_()
        self.adb_devices_Info.raise_()
        self.label_6.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.enable_debug_log_checkbox.raise_()
        self.label_4.raise_()
        self.all_cmd_type_state.raise_()
        self.groupBox_6.raise_()
        self.label_5.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "屏幕"))
        self.label_2.setText(_translate("MainWindow", "帧率"))
        self.hs_mode.setText(_translate("MainWindow", "hs_mode"))
        self.code_pack.setText(_translate("MainWindow", "打包"))
        self.sync_te.setText(_translate("MainWindow", "sycn TE"))
        self.checkBox_4.setText(_translate("MainWindow", "全帧率替换"))
        self.label_6.setText(_translate("MainWindow", "手机"))
        self.groupBox.setTitle(_translate("MainWindow", "DEBUG窗口"))
        self.debug_window.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.clear_debug_window.setText(_translate("MainWindow", "清空"))
        self.get_code_Button.setToolTip(_translate("MainWindow", "获取手机实时的code，可验证code是否替换成功"))
        self.get_code_Button.setText(_translate("MainWindow", "获取code"))
        self.groupBox_2.setTitle(_translate("MainWindow", "在这里替换code"))
        self.r_code.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.replace_code.setText(_translate("MainWindow", "替换code"))
        self.transform_code.setText(_translate("MainWindow", "转换code"))
        self.restore_code.setToolTip(_translate("MainWindow", "还原单个code"))
        self.restore_code.setText(_translate("MainWindow", "还原code"))
        self.restore_all_code.setToolTip(_translate("MainWindow", "一键还原所有的code"))
        self.restore_all_code.setText(_translate("MainWindow", "一键还原"))
        self.groupBox_3.setTitle(_translate("MainWindow", "文件夹"))
        self.open_dir_button.setText(_translate("MainWindow", "打开文件夹"))
        self.import_file_button.setText(_translate("MainWindow", "文件预览"))
        self.import_file_button_2.setText(_translate("MainWindow", "一键替换"))
        self.groupBox_4.setTitle(_translate("MainWindow", "预览窗口"))
        self.preview_window.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.json_to_code_button.setText(_translate("MainWindow", "一键替换"))
        self.save_file_button.setText(_translate("MainWindow", "文件保存"))
        self.save_as_button.setText(_translate("MainWindow", "文件另存为"))
        self.restore_code_in_json.setToolTip(_translate("MainWindow", "一键还原所有的code"))
        self.restore_code_in_json.setText(_translate("MainWindow", "一键还原"))
        self.enable_debug_log_checkbox.setText(_translate("MainWindow", "开启debug日志"))
        self.label_4.setText(_translate("MainWindow", "all cmd type state"))
        self.all_cmd_type_state.setCurrentText(_translate("MainWindow", "off"))
        self.all_cmd_type_state.setItemText(0, _translate("MainWindow", "off"))
        self.all_cmd_type_state.setItemText(1, _translate("MainWindow", "lp_mode"))
        self.all_cmd_type_state.setItemText(2, _translate("MainWindow", "hs_mode"))
        self.groupBox_6.setTitle(_translate("MainWindow", "cmd type"))
        self.label_3.setText(_translate("MainWindow", "dump code in kernel log"))
        self.dump_code_enable.setText(_translate("MainWindow", "enable"))
        self.dump_code_disable.setText(_translate("MainWindow", "disable"))
        self.label_5.setText(_translate("MainWindow", "咨询与投诉：黄昌畅/00018334"))
