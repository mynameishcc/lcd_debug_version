import sys
import subprocess as subpro

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer

from MyLog import MyLog

class ADBMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.adb_device = ''
        #self.win : Window = None
        self.current_devices = []

        self.timer = QTimer(self)
        self.timer.setInterval(3000)  # 每s秒检查一次
        self.timer.timeout.connect(self.refresh_device_list)
        self.timer.start()

        self.win = None
    
    @MyLog.print_function_name
    def refresh_device_list__(self, text):
        print(self.adb_device)
        self.adb_device = text
        if self.adb_device:
            MyLog.cout(self.win.ui.debug_window, "===========change current adb device to " + self.adb_device + "=============")
        self.adb_shell("mount -t debugfs none /d")
        self.win.refresh_screen_number()

    
    def on_adb_devices_info_change(self, text):
        self.refresh_device_list__(text)

    @MyLog.print_function_name
    def refresh_device_list_(self, devices):
        self.win.clear_combo_box(self.win.ui.adb_devices_Info)
        if not devices:
            MyLog.cout(self.win.ui.debug_window,'no devices connected')
        else:
            for adb_device in devices:
                self.win.ui.adb_devices_Info.blockSignals(True)
                self.win.ui.adb_devices_Info.addItem(adb_device)
                self.win.ui.adb_devices_Info.blockSignals(False)
        
        self.refresh_device_list__(self.win.ui.adb_devices_Info.currentText())

    def refresh_device_list(self):
        devices = self.get_adb_devices()
        print(devices)
        if devices != self.current_devices:
            self.current_devices = devices
            self.refresh_device_list_(devices)

    def adb_shell(self, cmd):
        str = f'adb -s {self.adb_device} shell  "{cmd}"'
        print(str)
        return subpro.getoutput(str)
    
    def adb(self, cmd):
        return subpro.getoutput(f'adb -s {self.adb_device} {cmd}')
    
    def get_adb_devices(self):
        result = subpro.run(['adb', 'devices'], stdout=subpro.PIPE, stderr=subpro.PIPE, text=True)
        lines = result.stdout.splitlines()
        devices = []
        for line in lines[1:]:  # 跳过第一行，它通常是"List of devices attached"
            if "\tdevice" in line:
                device_id = line.split("\t")[0]
                devices.append(device_id)
        return devices