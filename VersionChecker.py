from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QWidget, QMessageBox

from MyLog import logger
import version

class VersionChecker(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.MainWindow = parent

    def get_version(self):
        self.local_version = version.version
        self.MainWindow.setWindowTitle(f"MainWindow {self.local_version}")

    def check_for_updates(self):
        self.get_version()

        # 读取共享文件中的版本信息
        shared_file_path = r"\\10.167.19.50\lcd_debug\version.py"
        try:
            with open(shared_file_path, 'r') as file:
                response = file.read()
                latest_version = response.split("=")[1].strip()  # 假设响应是一个简单的版本号字符串

                logger.info(f"latest_version: {latest_version}, local_version: {self.local_version}")

                if float(latest_version) > float(self.local_version):
                    self.show_update_dialog(latest_version)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"版本检查失败: {str(e)}")

    def show_update_dialog(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("版本更新")
        msg_box.setText(f"可用版本{message}<br><a href='https://w3.hihonor.com/weshare/community/#/topic-detail?topicId=963616788427227136'>点击这里更新</a>")
        msg_box.setTextFormat(Qt.RichText)  # 允许使用富文本格式
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()