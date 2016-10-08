class Params(object):
    volume = 0.5
    fs = 44100
    duration = 0.1
    f=440
    play = True

    # The class "constructor" - It's actually an initializer 
    def __init__(self, volume, fs, duration, f):
        self.volume = volume
        self.fs = fs
        self.duration = duration
        self.f  = f 
        self.play = True