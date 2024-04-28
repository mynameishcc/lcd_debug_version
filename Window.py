import inspect
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from Ui_UI import Ui_MainWindow
from Panel import Panel
from ADBMonitor import ADBMonitor
from MyLog import MyLog
from Json_process import Json_process

class CustomOutput:
    def __init__(self, stdout, text_widget):
        self.stdout = stdout
        self.text_widget = text_widget
 
    def write(self, message):
        self.text_widget.append(message)

    def flush(self):
        pass

class Window(QtWidgets.QWidget):
    def __init__(self, panel: Panel, adb_cmd: ADBMonitor, json_pro: Json_process):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.replace_code.clicked.connect(self.replace_code)
        self.ui.clear_debug_window.clicked.connect(self.clear_debug_window)
        self.ui.save_file_button.clicked.connect(self.save_file)
        self.ui.import_file_button.clicked.connect(self.import_json_file)
        self.ui.json_to_code_button.clicked.connect(self.json_to_code)
        self.ui.open_dir_button.clicked.connect(self.open_dir)
        #self.redirect_stdout()

        self.adb_cmd = adb_cmd
        adb_cmd.win = self
        self.panel = panel

        self.adb_cmd.refresh_device_list()
        self.ui.adb_devices_Info.currentTextChanged.connect(self.adb_cmd.refresh_device_list__)
        self.ui.screen_index.currentTextChanged.connect(self.on_screen_change)
        self.ui.fps_list.currentTextChanged.connect(self.on_fps_list_info_change)
        self.ui.cmd_type_list.currentTextChanged.connect(self.on_cmd_type_change)

        self.ui.hs_mode.stateChanged.connect(self.on_hs_speed_change)
        self.ui.code_pack.stateChanged.connect(self.on_code_pack_change)
        self.ui.sync_te.stateChanged.connect(self.on_sync_te_change)

        self.ui.listWidget.itemDoubleClicked.connect(self.import_json_file)
        self.json_pro = json_pro
        json_pro.win = self

        json_pro.json_file_init()

        self.MainWindow.show()

    def open_dir(self):
        # 弹出文件夹选择对话框
        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Select a JSON File", "", "JSON Files (*.json)", options=option)
        self.json_pro.open_dir(filePath)


    def json_to_code(self):
        self.json_pro.json_to_code()

    def import_json_file(self):
        self.json_pro.import_file()

    def save_file(self):
        self.json_pro.save_file(self)

    def clear_debug_window(self):
        self.ui.debug_window.clear()

    @MyLog.print_function_name
    def on_cmd_type_change(self, text):
        self.panel.current_cmd_type = text
        MyLog.cout(self.ui.debug_window, "change current cmd type to " + text)
        print("current cmd type" + self.panel.current_cmd_type)
        #self.refresh_screen_cmd_type()        

    @MyLog.print_function_name
    def on_sync_te_change(self, state):
        if state == QtCore.Qt.Checked:
            pass

    @MyLog.print_function_name
    def on_hs_speed_change(self, state):
        if state == QtCore.Qt.Checked:
            pass

    @MyLog.print_function_name
    def code_process(self, code_pack_flag, sync_te_flag):
        ret = ''
        text = self.ui.r_code.toPlainText()
        text = text.split('\n')
        #print(text)
        for line_index, line in enumerate(text):
            line = line.split()
            for i, j in enumerate(line):
                if i == 3 and line_index != len(text) - 1:
                    j = int(j, base=16)
                    if code_pack_flag and line_index != len(text) - 1:
                        j |= 0x40
                        print(j)
                    elif not code_pack_flag:
                        j &= ~0x40
                        print(j)
                    # if sync_te_flag and :
                    #     j |= 0x20
                    # else:
                    #     j &= ~0x20
                    j = format(j, '0>2X')
                ret += j
                if i != len(line):
                    ret += ' '
            if line_index != len(text) - 1:
                ret += '\n'
        self.ui.r_code.clear()
        self.ui.r_code.append(ret)

    @MyLog.print_function_name
    def on_code_pack_change(self, state):
        if state == QtCore.Qt.Checked:
            self.code_process(True, self.ui.sync_te.isChecked())
        else:
            self.code_process(False, self.ui.sync_te.isChecked())
        #MyLog.cout(self.ui.debug_window, state)

    @MyLog.print_function_name
    def on_screen_change(self, text):
        self.panel.current_screen = text
        MyLog.cout(self.ui.debug_window, "change current screen to " + text)
        print("current_screen" + self.panel.current_screen)
        self.refresh_screen_fps()

    @MyLog.print_function_name
    def on_fps_list_info_change(self, text):
        self.panel.current_fps = text
        MyLog.cout(self.ui.debug_window, "change current fps to " + text + "line"+ str(inspect.currentframe().f_back.f_lineno))

    @MyLog.print_function_name
    def clear_combo_box(self, combo_box):
        combo_box.blockSignals(True)  # 阻止信号发射
        combo_box.clear()
        combo_box.blockSignals(False)  # 恢复信号发射

    @MyLog.print_function_name
    def refresh_screen_cmd_type(self):
        self.clear_combo_box(self.ui.cmd_type_list)
        self.adb_cmd.adb_shell(f"cat /sys/class/graphics/fb{self.panel.current_screen}/lcdkit_cmd_type")
        self.adb_cmd.adb("pull /data/lcdkit_cmd_type.txt .")
        self.panel.cmd_type_list = self.panel.get_cmd_type_list("lcdkit_cmd_type.txt")

        for index, cmd_type in enumerate(self.panel.cmd_type_list):
            self.ui.cmd_type_list.blockSignals(True)
            print(cmd_type)
            self.ui.cmd_type_list.addItem(f"{index}:{cmd_type}")
            self.ui.cmd_type_list.blockSignals(False)
        
        self.panel.current_cmd_type = self.ui.cmd_type_list.currentText()

    @MyLog.print_function_name
    def refresh_screen_fps(self):
        self.clear_combo_box(self.ui.fps_list)
        ret = self.adb_cmd.adb_shell(f"cat /sys/class/graphics/fb{self.panel.current_screen}/lcd_fps_scence")
        fps_list = self.panel.get_fps_list(ret)

        for fps in fps_list:
            self.ui.fps_list.blockSignals(True)
            self.ui.fps_list.addItem(fps)
            self.ui.fps_list.blockSignals(False)
        
        self.panel.current_fps = self.ui.fps_list.currentText()

    @MyLog.print_function_name
    def refresh_screen_number(self):
        print("The function ============", inspect.currentframe().f_code.co_name, "====================")
        self.panel.screen_num = 0
        self.clear_combo_box(self.ui.screen_index)

        ret = self.adb_cmd.adb_shell("cat proc/cmdline")
        #print(ret)
        ret = ret.split()
        for cmdline in ret:
            if "msm_drm.dsi_display" in cmdline:
                self.panel.screen_num += 1

        for i in range(self.panel.screen_num):
            self.ui.screen_index.blockSignals(True)
            self.ui.screen_index.addItem(f"{i}")
            self.ui.screen_index.blockSignals(False)

        self.panel.current_screen = self.ui.screen_index.currentText()
        print("current_screen" + self.ui.screen_index.currentText())

        self.refresh_screen_fps()

    @MyLog.print_function_name
    def redirect_stdout(self):
        sys.stdout = CustomOutput(sys.stdout, self.ui.debug_window)
        #sys.stderr = CustomOutput(sys.stderr, self.ui.debug_window)

    @MyLog.print_function_name
    def replace_code(self, *args, **kwargs):
        r_code = self.ui.r_code.toPlainText()
        hs_mode = 1 if self.ui.hs_mode.isChecked() else 0
        type_index = int(self.panel.current_cmd_type.split(':')[0])

        self.replace_code_(r_code, self.panel.current_screen, self.panel.current_fps, type_index, hs_mode)

        self.json_pro.update(r_code)

    def replace_code_(self, code, screen, fps, type_index, hs_mode):
        with open('lcd_param_config.xml', 'w') as wf:
            wf.write("<PanelCommand>\n")
            wf.write(code)
            wf.write("\n")
            wf.write("</PanelCommand>")
        self.adb_cmd.adb('push lcd_param_config.xml /data/')
        self.adb_cmd.adb_shell(f'echo set_param_config:{type_index} dsi:{screen} fps:{fps} hs_mode:{hs_mode} > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg')
        MyLog.cout(self.ui.debug_window, f"cmd type: {type_index} dsi:{screen} fps:{fps} hs_mode:{hs_mode} replace code successfully")
        #print(self.panel.cmd_type_list[type_index])
        if self.panel.cmd_type_list[type_index] == "qcom,mdss-dsi-debug-commands":
            self.adb_cmd.adb("pull /data/lcdkit_result.txt .")
            with open("lcdkit_result.txt", 'r') as rf:
                result = rf.readlines()
                for line in result:
                    self.ui.debug_window.append(line.strip())