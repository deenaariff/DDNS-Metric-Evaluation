import config

class Algorithm:

    def __init__(self):
        self.index = config.round

    def roundRobin(self):
        _tmp = self.index
        self.index = (_tmp+1) % (config.numServers) 
        return _tmp
