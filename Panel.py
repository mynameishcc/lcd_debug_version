from MyLog import MyLog, logger

class Panel(object):
    def __init__(self):
        self.screen_num : int = 0
        self.current_screen : str = '0'
        self.current_fps : str = ''
        self.fps_list : list = []
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

    def get_real_fps(self, ret): # current_fps:120;default_fps:60;support_fps_list:60,120,10,1,90,40,30;current_index:1
        ret = ret.split(';')
        for i in ret:
            if 'current_fps' in i:
                return i.split(':')[1]


    def get_real_screen(self, ret):
        return ret.split(':')[1].strip() #panel_index:0 means内屏亮，1 means 外屏亮，2 means双屏同显，3 means都不亮
    
    def translate(self, screen):
        if screen == "0":
            return "内屏"
        elif screen == "1":
            return "外屏"
        elif screen == "2":
            return "双屏同显"
        elif screen == "3":
            return "灭屏"