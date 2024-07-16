from PyQt5.QtCore import QUrl, Qt, QObject
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMessageBox

from MyLog import logger
import version

class VersionChecker(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        # 创建 QNetworkAccessManager 实例
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.on_finished)
        self.MainWindow = parent

    def get_version(self):
        self.local_version = version.version
        self.MainWindow.setWindowTitle(f"MainWindow {self.local_version}")

    def check_for_updates(self):
        self.get_version()

        # 发送 GET 请求获取版本信息
        url = QUrl("https://raw.githubusercontent.com/mynameishcc/lcd_debug_version/main/version.txt")  # 替换为实际的版本检查URL
        request = QNetworkRequest(url)
        self.manager.get(request)

    def on_finished(self, reply):
        # 处理响应
        if reply.error():
            QMessageBox.critical(self, "错误", f"版本检查失败: {reply.errorString()}")
        else:
            response = reply.readAll().data().decode()
            latest_version = response.split("=")[1].strip()  # 假设响应是一个简单的版本号字符串

            logger.info(f"latest_version: {latest_version}, local_version: {self.local_version}")

            if float(latest_version) > float(self.local_version):
                self.show_update_dialog(latest_version)

    def show_update_dialog(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("版本更新")
        msg_box.setText(f"可用版本{message}<br><a href='https://w3.hihonor.com/weshare/community/#/topic-detail?topicId=963616788427227136'>点击这里更新</a>")
        msg_box.setTextFormat(Qt.RichText)  # 允许使用富文本格式
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()