import pyaudio
import threading
import numpy as np
import wave
import struct
from parameters import Params, signalType

class Generator(threading.Thread):

    def __init__(self, params, lock):
        threading.Thread.__init__(self)
        self.p = pyaudio.PyAudio()
        self.name = "player"
        self.lock = lock
        self.params = params
        self.noise = wav_to_npFloat('szumrozowy.wav')

        with self.lock:
            self.fs=getattr(self.params,"fs");
            self.duration = getattr(self.params,"duration")

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=getattr(Params,"fs"),
                        output=True)
        return

    def run(self):
        print("Starting " + self.name)
        while self.params.play:
            self.play()

        print("Exiting " + self.name)
        return

    def play(self):
        with self.lock:
            f = getattr(self.params,"f")
            volume = getattr(self.params,"volume")

        if self.params.signal == signalType.sine:
            # generate samples, note conversion to float32 array
            samples = (np.sin(2*np.pi*np.arange(self.fs*self.duration)*f/self.fs)).astype(np.float32)
            # play. May repeat with different volume values (if done interactively) 
            self.stream.write(volume*samples)

        elif self.params.signal == signalType.pink_noise:
            self.stream.write(volume*self.noise)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return

def wav_to_npFloat(wave_file):
    w = wave.open(wave_file)
    #astr = w.readframes(w.getnframes())
    astr = w.readframes(44100*3)
    # convert binary chunks to short 
    #a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
    a = struct.unpack("%ih" % (44100*3* w.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    return np.asarray(a).astype(np.float32)
