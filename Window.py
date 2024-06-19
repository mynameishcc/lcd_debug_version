import inspect
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from Ui_UI import Ui_MainWindow
from Panel import Panel
from ADBMonitor import ADBMonitor
from MyLog import MyLog, logger
from Json_process import Json_process
from parseCode import lines2codes

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

        logger.info('\n\n\nstart init')

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.replace_code.clicked.connect(self.replace_code)
        self.ui.clear_debug_window.clicked.connect(self.clear_debug_window)
        self.ui.save_file_button.clicked.connect(self.save_file)
        self.ui.import_file_button.clicked.connect(self.import_json_file)
        self.ui.json_to_code_button.clicked.connect(self.json_to_code)
        self.ui.open_dir_button.clicked.connect(self.open_dir)
        self.ui.transform_code.clicked.connect(self.transform_code)
        self.ui.get_code_Button.clicked.connect(self.get_code)
        self.ui.dump_code_enable.clicked.connect(self.dump_code_enable)
        self.ui.dump_code_disable.clicked.connect(self.dump_code_disable)
        self.ui.restore_code.clicked.connect(self.restore_code)
        self.ui.restore_all_code.clicked.connect(self.restore_all_code)
        #self.redirect_stdout()

        self.adb_cmd = adb_cmd
        adb_cmd.win = self
        self.panel = panel
        panel.win = self

        self.ui.adb_devices_Info.currentTextChanged.connect(self.adb_cmd.refresh_device_list__)
        self.ui.screen_index.currentTextChanged.connect(self.on_screen_change)
        self.ui.fps_list.currentTextChanged.connect(self.on_fps_list_info_change)
        self.ui.cmd_type_list.currentTextChanged.connect(self.on_cmd_type_change)
        self.ui.all_cmd_type_state.currentTextChanged.connect(self.on_all_cmd_type_state_change)

        self.ui.enable_debug_log_checkbox.stateChanged.connect(self.on_debug_log_level_change)
        self.ui.hs_mode.stateChanged.connect(self.on_hs_speed_change)
        self.ui.code_pack.stateChanged.connect(self.on_code_pack_change)
        self.ui.sync_te.stateChanged.connect(self.on_sync_te_change)

        self.ui.listWidget.itemDoubleClicked.connect(self.import_json_file)

        self.ui.search_lineedit.textChanged.connect(self.on_search_lineedit_change)
        self.json_pro = json_pro
        json_pro.win = self

        json_pro.json_file_init()

        logger.info('end init\n')

        self.MainWindow.show()

    def dump_code_enable_(self, enable):
        if enable and not self.ui.enable_debug_log_checkbox.isChecked():
            MyLog.cout(self.ui.debug_window, 'warning: please check "开启debug日志"')
        if self.panel.current_cmd_type:
            type_index = int(self.panel.current_cmd_type.split(':')[0])
            self.adb_cmd.adb_shell(f"echo dump_cmd_type:{type_index} enable:{enable} > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg")
            MyLog.cout(self.ui.debug_window, f'{"enable" if enable else "disable"} {self.panel.current_cmd_type}')
        else:
            MyLog.cout(self.ui.debug_window, 'cmd type error')

    def dump_code_enable(self):
        self.dump_code_enable_(1)

    def dump_code_disable(self):
        self.dump_code_enable_(0)

    def transform_code(self):
        text = self.ui.r_code.toPlainText()
        text = text.split('\n')
        MyLog.cout(self.ui.debug_window, '\n' + lines2codes(text))

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
    def on_search_lineedit_change(self, text):
        self.update_ui_cmd_type_list()

    def update_current_cmd_type(self, text):
        if text != self.panel.current_cmd_type:
            self.panel.current_cmd_type = text
            if text:
                MyLog.cout(self.ui.debug_window, "change current cmd type to " + text)
            else:
                MyLog.cout(self.ui.debug_window, "no cmd type deteced")

    def on_all_cmd_type_state_change(self, text):
        MyLog.cout(self.ui.debug_window, f"set all cmd type state to {text}")
        self.adb_cmd.adb_shell(f"echo set_all_cmd_type_state:{text} > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg")

    @MyLog.print_function_name
    def on_cmd_type_change(self, text):
        self.update_current_cmd_type(text)
        #self.refresh_screen_cmd_type()        

    @MyLog.print_function_name
    def on_sync_te_change(self, state):
        if state == QtCore.Qt.Checked:
            pass

    @MyLog.print_function_name
    def on_debug_log_level_change(self, state):
        if state == QtCore.Qt.Checked:
            debug_level = 4
        else:
            debug_level = 0
        self.adb_cmd.adb_shell(f"echo set_debug_level:{debug_level} > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg")

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
                        logger.info(j)
                    elif not code_pack_flag:
                        j &= ~0x40
                        logger.info(j)
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
        logger.info("current_screen" + self.panel.current_screen)
        self.refresh_screen_fps()

    @MyLog.print_function_name
    def on_fps_list_info_change(self, text):
        self.panel.current_fps = text
        MyLog.cout(self.ui.debug_window, "change current fps to " + text)

    @MyLog.print_function_name
    def clear_combo_box(self, combo_box):
        combo_box.blockSignals(True)  # 阻止信号发射
        combo_box.clear()
        combo_box.blockSignals(False)  # 恢复信号发射

    @MyLog.print_function_name
    def update_ui_cmd_type_list(self):
        self.clear_combo_box(self.ui.cmd_type_list)

        search_word = self.ui.search_lineedit.text().strip()
        self.ui.cmd_type_list.blockSignals(True)
        for cmd_type in self.panel.cmd_type_list_with_index:
            #print(search_word)
            if not search_word or search_word.lower() in cmd_type.lower():
                logger.info(cmd_type)
                self.ui.cmd_type_list.addItem(cmd_type)
        self.ui.cmd_type_list.blockSignals(False)

        self.update_current_cmd_type(self.ui.cmd_type_list.currentText())

    @MyLog.print_function_name
    def refresh_screen_cmd_type(self):
        self.adb_cmd.adb_shell(f"cat /sys/class/graphics/fb{self.panel.current_screen}/lcdkit_cmd_type")
        self.adb_cmd.adb("pull /data/lcdkit_cmd_type.txt .")
        self.panel.cmd_type_list = self.panel.get_cmd_type_list("lcdkit_cmd_type.txt")
        self.panel.cmd_type_list_with_index = [f"{i}:{v}" for i, v in enumerate(self.panel.cmd_type_list)]
        try:
            os.remove("lcdkit_cmd_type.txt")
        except Exception as e:
            logger.exception(e)

        self.update_ui_cmd_type_list()

    def check_panel_state(self):
        ret = self.adb_cmd.adb_shell(f"cat /sys/class/graphics/fb0/lcd_display_type")
        real_screen = self.panel.get_real_screen(ret)
        print(type(real_screen), type(self.panel.current_screen))
        if (real_screen != self.panel.current_screen):
            MyLog.cout(self.ui.debug_window, "[warning]:" + f"real screen state is {self.panel.translate(real_screen)}," +\
                       f" but config screen is {self.panel.translate(self.panel.current_screen)}")
            return
        ret = self.adb_cmd.adb_shell(f"cat /sys/class/graphics/fb{self.panel.current_screen}/lcd_fps_scence")
        real_fps = self.panel.get_real_fps(ret)
        print(type(real_fps), type(self.panel.current_fps))
        if real_fps != self.panel.current_fps:
            MyLog.cout(self.ui.debug_window, "[warning]:" + f"real fps is {real_fps}," + f" but config fps is {self.panel.current_fps}")
            return

    @MyLog.print_function_name
    def refresh_screen_fps(self):
        self.clear_combo_box(self.ui.fps_list)
        ret = self.adb_cmd.adb_shell(f"cat /sys/class/graphics/fb{self.panel.current_screen}/lcd_fps_scence")
        self.panel.fps_list = self.panel.get_fps_list(ret)

        for fps in self.panel.fps_list:
            self.ui.fps_list.blockSignals(True)
            self.ui.fps_list.addItem(fps)
            self.ui.fps_list.blockSignals(False)
        
        self.panel.current_fps = self.ui.fps_list.currentText()

    @MyLog.print_function_name
    def refresh_screen_number(self):
        #logger.info("The function ============", inspect.currentframe().f_code.co_name, "====================")
        self.panel.screen_num = 0
        self.clear_combo_box(self.ui.screen_index)

        ret = self.adb_cmd.adb_shell("cat proc/cmdline")
        #print(ret)
        ret = ret.split()
        for cmdline in ret:
            if "msm_drm.dsi_display" in cmdline:
                self.panel.screen_num += 1

        self.ui.screen_index.blockSignals(True)
        model = QStandardItemModel()
        for i in range(self.panel.screen_num):
            s = f"{i}"
            standard_item = QStandardItem(s)
            standard_item.setToolTip(self.panel.get_panel_tips(s))  # 设置工具提示
            model.appendRow(standard_item)
        self.ui.screen_index.setModel(model)
        self.ui.screen_index.blockSignals(False)

        self.panel.current_screen = self.ui.screen_index.currentText()
        logger.info("current_screen" + self.ui.screen_index.currentText())

        self.refresh_screen_fps()

    @MyLog.print_function_name
    def redirect_stdout(self):
        sys.stdout = CustomOutput(sys.stdout, self.ui.debug_window)
        #sys.stderr = CustomOutput(sys.stderr, self.ui.debug_window)

    @MyLog.print_function_name
    def replace_code(self, *args, **kwargs):
        self.check_panel_state()
        r_code = self.ui.r_code.toPlainText()
        hs_mode = 1 if self.ui.hs_mode.isChecked() else 0
        type_index = int(self.panel.current_cmd_type.split(':')[0])

        self.replace_code_(r_code, self.panel.current_screen, self.panel.current_fps, type_index, hs_mode)

        self.json_pro.update(r_code)

    def get_code(self):
        self.check_panel_state()
        type_index = int(self.panel.current_cmd_type.split(':')[0])
        screen = self.panel.current_screen
        fps = self.panel.current_fps

        self.adb_cmd.adb_shell(f"echo get_cmd:{type_index} dsi:{screen} fps:{fps} > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg")
        self.adb_cmd.adb("pull /data/lcdkit_code.txt .")
        self.adb_cmd.adb_shell("rm -rf /data/lcdkit_code.txt")

        try:
            with open("lcdkit_code.txt", 'r') as rf:
                code = rf.readlines()
                code = ''.join(code)
                MyLog.cout(self.ui.debug_window, '\n' + code)
            # self.ui.debug_window.append("\n")
            # for line in code:
            #     self.ui.debug_window.append(line)
        except Exception as e:
            MyLog.cout(self.ui.debug_window, "get code failed")
            logger.exception(e)
        # try:
        #     os.remove("lcdkit_code.txt")
        # except Exception as e:
        #     logger.exception(e)

    def replace_code_(self, code, screen, fps, type_index, hs_mode):
        with open('lcd_param_config.xml', 'w') as wf:
            wf.write("<PanelCommand>\n")
            wf.write(code)
            wf.write("\n")
            wf.write("</PanelCommand>")
        self.adb_cmd.adb('push lcd_param_config.xml /data/')
        self.adb_cmd.adb_shell(f'echo set_param_config:{type_index} dsi:{screen} fps:{fps} hs_mode:{hs_mode} > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg')
        MyLog.cout(self.ui.debug_window, f"replace cmd type: {type_index} dsi:{screen} fps:{fps} hs_mode:{hs_mode}")
        ret = self.adb_cmd.adb_get_result()
        if ret.strip():
            MyLog.cout(self.ui.debug_window, ret)
        #print(self.panel.cmd_type_list[type_index])
        if self.panel.cmd_type_list[type_index] == "qcom,mdss-dsi-debug-commands":
            self.adb_cmd.adb("pull /data/lcdkit_result.txt .")
            with open("lcdkit_result.txt", 'r') as rf:
                result = rf.readlines()
                for line in result:
                    self.ui.debug_window.append(line.strip())

    def restore_code_(self, screen, fps, type_index):
        self.adb_cmd.adb_shell(f'echo restore_cmd:{type_index} dsi:{screen} fps:{fps} > /sys/kernel/debug/lcd-dbg/lcd_kit_dbg')
        MyLog.cout(self.ui.debug_window, f"store cmd type: {type_index} dsi:{screen} fps:{fps}")

    def restore_code(self):
        type_index = int(self.panel.current_cmd_type.split(':')[0])
        self.restore_code_(self.panel.current_screen, self.panel.current_fps, type_index)

    def restore_all_code(self):
        cmd_num = len(self.panel.cmd_type_list)
        for screen in range(self.panel.screen_num):
            for fps in self.panel.fps_list:
                for type_index in range(cmd_num):
                    self.restore_code_(screen, fps, type_index)

        