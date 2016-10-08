import pyaudio
import threading
import numpy as np
from parameters import Params

class Generator(threading.Thread):

    def __init__(self, params, lock):
        threading.Thread.__init__(self)
        self.p = pyaudio.PyAudio()
        self.name = "player"
        # for paFloat32 sample values must be in range [-1.0, 1.0]
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=getattr(Params,"fs"),
                        output=True)
        self.lock = lock
        self.params = params
        return

    def run(self):
        print("Starting " + self.name)
        while self.params.play:
            self.play()

        print("Exiting " + self.name)
        return

    def play(self):
        with self.lock:
            fs=getattr(self.params,"fs");
            duration = getattr(self.params,"duration")
            f = getattr(self.params,"f")
            volume = getattr(self.params,"volume")

        # generate samples, note conversion to float32 array
        samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

        # play. May repeat with different volume values (if done interactively) 
        self.stream.write(volume*samples)


    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return
