
class Config:
    def __init__(self):
        self.BASE_TIME_SECONDS = 'seconds'
        self.BASE_TIME_MINUTES = 'minutes'
        self.BASE_TIME_HOURS = 'hours'
        self.DIRECTION_TON = 'ton'
        self.DIRECTION_TOFF = 'toff'
        
        self.LOGIC_STATE_UP = 1
        self.LOGIC_STATE_DOW = 0

        self.PULL_UP = 1
        self.PULL_DOWN = 0
    
config = Config()