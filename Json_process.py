import json
import os

from PyQt5.QtWidgets import QFileDialog

from MyLog import MyLog

class Json_process(object):
    def __init__(self):
        self.data = dict()
        self.folderPath = ''
        self.current_filepath = ''

    def json_file_init(self):
        pass
    
    def open_dir(self, filePath):
        if filePath:
            # 清空当前列表
            folderPath = os.path.dirname(filePath)
            self.folderPath = folderPath
            self.win.ui.listWidget.clear()
            # 遍历文件夹中的所有文件
            for filename in os.listdir(folderPath):
                if filename.endswith('.json'):
                    # 将JSON文件添加到列表框中
                    self.win.ui.listWidget.addItem(filename)

    def panel_label_to_index(self, panel):
        return panel[len("panel"):]
    
    def fps_label_to_index(self, fps):
        return fps[len("fps"):]
    
    def cmd_type_lable_to_index(self, cmd_type):
        return int(cmd_type.split(':')[0])

    def json_to_code(self):
        self.data = self.get_data_dic_data_from_preview_window()
        for panel, _ in self.data.items():
            panel = self.panel_label_to_index(panel)
            for fps, _ in _.items():
                fps = self.fps_label_to_index(fps)
                for cmd_type, data in _.items():
                    cmd_type = self.cmd_type_lable_to_index(cmd_type)
                    code = '\n'.join(data[:-1])
                    hs_mode = 1 if data[-1] == "hs_mode" else 0
                    self.win.replace_code_(code, panel, fps, cmd_type, hs_mode)

    def import_file(self):
        # 获取当前选中的项
        currentItem = self.win.ui.listWidget.currentItem()
        if currentItem is not None:
            # 获取选中项的文本并更新标签
            selectedText = currentItem.text()
            MyLog.cout(self.win.ui.debug_window, f'Selected Text: {selectedText}')
        else:
            MyLog.cout(self.win.ui.debug_window, 'Selected Text: None')
            return

        try:
            with open(os.path.join(self.folderPath, selectedText), 'r') as rf:
                self.data = json.load(rf)
        except Exception as e:
            MyLog.cout(self.win.ui.debug_window, str(e))
            MyLog.cout(self.win.ui.debug_window, "import file failed")
            return
        self.win.ui.preview_window.clear()
        json_string_pretty = json.dumps(self.data, indent=4)
        self.win.ui.preview_window.append(json_string_pretty)
        MyLog.cout(self.win.ui.debug_window, "import file successfully")

    def save_file(self, win):
        self.data = self.get_data_dic_data_from_preview_window()
        if not self.data:
            MyLog.cout(self.win.ui.debug_window, "save file failed")
            return
        # 弹出文件夹选择对话框
        options = QFileDialog.Options()
        # 不使用系统自带的对话框
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(win, "save file", "", "JSON Files (*.json)", options=options)
        if fileName:
            if not fileName.endswith('.json'):
                fileName += '.json'
            # 用户选择了文件，写入内容
            with open(fileName, 'w') as wf:
                json.dump(self.data, wf, indent=4)
        MyLog.cout(self.win.ui.debug_window, f"save file {fileName} successfully")

    def get_data_dic_data_from_preview_window(self):
        ret = None
        data = self.win.ui.preview_window.toPlainText()
        #print(len(data))
        if data == "":
            return dict()
        try:
            ret = json.loads(data)
        except json.JSONDecodeError as e:
            MyLog.cout(self.win.ui.debug_window, "Please check the JSON format:" + str(e))
        except Exception as e:
            MyLog.cout(self.win.ui.debug_window, "An error occurred:" + str(e))

        return ret

    def update(self, r_code : str):
        self.data = self.get_data_dic_data_from_preview_window()
        if self.data is None:
            return
        panel = "panel" + self.win.panel.current_screen
        if panel not in self.data:
            self.data[panel] = dict()
            self.data = dict(sorted(self.data.items(), key=lambda x:int(self.panel_label_to_index(x[0]))))
        fps = "fps" + self.win.panel.current_fps
        if fps not in self.data[panel]:
            self.data[panel][fps] = dict()
            self.data[panel] = dict(sorted(self.data[panel].items(), key=lambda x:int(self.fps_label_to_index(x[0]))))

        cmd_type = self.win.panel.current_cmd_type

        self.data[panel][fps][cmd_type] = list()
        self.data[panel][fps] = dict(sorted(self.data[panel][fps].items(), key=lambda x:int(self.cmd_type_lable_to_index(x[0]))))
        self.data[panel][fps][cmd_type] += r_code.strip().split('\n')
        hs_mode = "hs_mode" if self.win.ui.hs_mode.isChecked() else "lp_mode"
        self.data[panel][fps][cmd_type].append(hs_mode)

        self.win.ui.preview_window.clear()
        json_string_pretty = json.dumps(self.data, indent=4)
        self.win.ui.preview_window.append(json_string_pretty)

    def remove(self):
        self.data = self.get_data_dic_data_from_preview_window()
        if self.data is None:
            return
        panel = "panel" + self.win.panel.current_screen
        if panel not in self.data:
            return
        fps = "fps" + self.win.panel.current_fps
        if fps not in self.data[panel]:
            return

        cmd_type = self.win.panel.current_cmd_type
        if cmd_type not in self.data[panel][fps]:
            return
        
        del self.data[panel][fps][cmd_type]
        if len(self.data[panel][fps]) == 0:
            del self.data[panel][fps]
            if len(self.data[panel]) == 0:
                del self.data[panel]

        self.win.ui.preview_window.clear()
        json_string_pretty = json.dumps(self.data, indent=4) if len(self.data) != 0 else ""
        self.win.ui.preview_window.append(json_string_pretty)