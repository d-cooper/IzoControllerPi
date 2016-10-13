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
        
        with self.lock:
            self.fs=getattr(self.params,"fs");
            self.frames = self.params.frames

        self.noise = wav_to_npFloat('szumrozowy.wav', self.frames)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=2,
                        rate=self.params.fs,
                        output=True,
                        frames_per_buffer=self.frames)
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
            pause = getattr(self.params,"pause")

        if self.params.signal == signalType.sine:
            # generate samples, note conversion to float32 array
            samples = (np.sin(2*np.pi*np.arange(self.frames)*f/self.fs)).astype(np.float32)
            # play. May repeat with different volume values (if done interactively) 
            self.stream.write(pause*volume*samples)

        elif self.params.signal == signalType.pink_noise:
            self.stream.write(pause*volume*self.noise)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return

def wav_to_npFloat(wave_file, frames):
    w = wave.open(wave_file)
    #astr = w.readframes(w.getnframes())
    astr = w.readframes(frames)
    # convert binary chunks to short 
    #a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
    a = struct.unpack("%ih" % (frames* w.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    return np.asarray(a).astype(np.float32)
