from enum import Enum
import os

cardName = "'HPOUT2 Digital'"   # Use for Cirrus Audio Card
#cardName = 'PCM'               # Use for internal audio

class signalType(Enum):
    sine = 1
    pink_noise = 2

class Params(object):
    #volume = 50
    volume=os.system('amixer sget '+ cardName)
    #volume = os.system('amixer sget '+ cardName)
    fs = 44100
    frames = 8820
    f=440
    pause = 0       #1 - pause, 0 - play
    play = True
    signal = signalType.pink_noise

    # The class "constructor" - It's actually an initializer 
    def __init__(self, volume, fs, frames, f):
        self.volume = volume
        self.fs = fs
        self.f  = f
        self.frames = frames
        self.play = True
