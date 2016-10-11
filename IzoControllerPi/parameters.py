from enum import Enum

class signalType(Enum):
    sine = 1
    pink_noise = 2

class Params(object):
    volume = 0.5
    fs = 44100
    duration = 0.1
    f=440
    play = True
    signal = signalType.pink_noise

    # The class "constructor" - It's actually an initializer 
    def __init__(self, volume, fs, duration, f):
        self.volume = volume
        self.fs = fs
        self.duration = duration
        self.f  = f 
        self.play = True