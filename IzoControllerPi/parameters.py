from enum import Enum

class signalType(Enum):
    sine = 1
    pink_noise = 2

class Params(object):
    volume = 0.5
    fs = 44100
    frames = 8820
    f=440
    pause = 0       #1 - pause, 0 - play
    play = True
    signal = signalType.sine

    # The class "constructor" - It's actually an initializer 
    def __init__(self, volume, fs, frames, f):
        self.volume = volume
        self.fs = fs
        self.f  = f
        self.frames = frames
        self.play = True
