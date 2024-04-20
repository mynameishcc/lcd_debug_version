class Panel(object):
    def __init__(self):
        self.screen_num : int = 0
        self.current_screen : str = '0'
        self.current_fps : str = ''

    def get_fps_list(self, ret):
        ret = ret.split(';')
        for data in ret:
            if 'support_fps_list' in data:
                data = data.split(':')[1]
                data = data.split(',')
                return data
        return []