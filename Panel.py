from MyLog import MyLog, logger

class Panel(object):
    def __init__(self):
        self.screen_num : int = 0
        self.current_screen : str = '0'
        self.current_fps : str = ''
        self.current_cmd_type : str = ''
        self.cmd_type_list = ''

    def get_fps_list(self, ret):
        ret = ret.split(';')
        for data in ret:
            if 'support_fps_list' in data:
                data = data.split(':')[1]
                data = data.split(',')
                return data
        return []
    
    def get_cmd_type_list(self, file):
        ret = []
        try:
            with open(file, 'r') as rf:
                ret = rf.readlines()
        except Exception as e:
            logger.exception(e)
        return [cmd_type.strip() for cmd_type in ret if cmd_type.strip()] # 去掉末尾的'\n'

    def get_panel_tips(self, index):
        dic = {
            "0":"内屏",
            "1":"外屏",
        }

        return dic[index] if index in dic else "异常屏幕"
