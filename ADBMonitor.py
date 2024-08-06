import subprocess as subpro

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal

from MyLog import MyLog, logger

class ADBMonitorThread(QThread):
    devices_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            devices = self.get_adb_devices()
            self.devices_changed.emit(devices)
            self.sleep(3)

    def get_adb_devices(self):
        result = subpro.run(['adb', 'devices'], stdout=subpro.PIPE, stderr=subpro.PIPE, text=True, creationflags=subpro.CREATE_NO_WINDOW)
        lines = result.stdout.splitlines()
        devices = []
        for line in lines[1:]:  # 跳过第一行，它通常是"List of devices attached"
            if "\tdevice" in line:
                device_id = line.split("\t")[0]
                devices.append(device_id)
        return devices

    def stop(self):
        self.running = False
        self.wait()

class ADBMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.adb_device = ''
        self.current_devices = []
        self.code_limit = 8000

        #启动后台线程
        self.monitor_thread = ADBMonitorThread()
        self.monitor_thread.devices_changed.connect(self.on_adb_devices_info_change)
        self.monitor_thread.start()

        self.win = None
    
    @MyLog.print_function_name
    def refresh_device_list__(self, text):
        logger.info(self.adb_device)
        self.adb_device = text
        if self.adb_device:
            MyLog.cout(self.win.ui.debug_window, "===========change current adb device to " + self.adb_device + "=============")
        self.adb_shell("mount -t debugfs none /d")
        self.win.refresh_screen_number()
        self.win.refresh_screen_cmd_type()
    
    def on_adb_devices_info_change(self, devices):
        self.refresh_device_list(devices)

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

    def refresh_device_list(self, devices):
        if devices != self.current_devices:
            logger.info(devices)
            self.current_devices = devices
            self.refresh_device_list_(devices)

    def adb_shell(self, cmd):
        str = f'adb -s {self.adb_device} shell  "{cmd}"'
        logger.info(str)
        return subpro.getoutput(str)
    
    def adb(self, cmd):
        logger.info(cmd)
        return subpro.getoutput(f'adb -s {self.adb_device} {cmd}')
    
    def adb_get_result(self):
        return self.adb_shell(f"cat /sys/kernel/debug/lcd-dbg/lcd_kit_dbg")