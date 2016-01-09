class Logger:
    'Logger class'
    level = 3
    # 4 = debug
    # 3 = info
    # 2 = warn
    # 1 = error
    # 0 = disabled

    def __init__(self, level):
        self.level = level

    def log(self,txt):
        print txt + "\n"

    def debug(self,txt):
        if (self.level >= 4):
            self.log(txt)
    def info(self,txt):
        if (self.level >= 3):
            self.log(txt)
    def warn(self,txt):
        if (self.level >= 2):
            self.log(txt)
    def error(self,txt):
        if (self.level >= 1):
            self.log(txt)
