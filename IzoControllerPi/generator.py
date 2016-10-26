import pyaudio
import threading
import numpy as np
import wave
import struct
import os
import time
from parameters import Params, signalType

noisePath = '/home/pi/Desktop/IzoControllerPi/IzoControllerPi/szumrozowy.wav'
internalPlayer = False

class Generator(threading.Thread):

    def __init__(self, params, lock):
        threading.Thread.__init__(self)
        self.name = "player"
        self.params = params

        if internalPlayer:
            self.initInternalPlayer(lock)
        
        return

    def initInternalPlayer(self,lock):
        self.p = pyaudio.PyAudio()     
        self.lock = lock
                
        with self.lock:
            self.fs=getattr(self.params,"fs");
            self.frames = self.params.frames

        self.noise = wav_to_npFloat(noisePath, self.frames)

        #for paFloat32 sample values must be in range [-1.0, 1.0]
        self.stream = self.p.open(format=pyaudio.paFloat32,
                        channels=2,
                        rate=self.params.fs,
                        output=True,
                        frames_per_buffer=self.frames)
        return
        
    
    def run(self):
        print("Starting " + self.name)
        
        if internalPlayer:
            while self.params.play:
                self.playInternal()
        else:
            while self.params.play:
                #os.system('amixer sset PCM 90%')
                os.system('aplay -d 100 ' + noisePath)
        print("Exiting " + self.name)
        return

    def playInternal(self):
        with self.lock:
            f = getattr(self.params,"f")
            volume = getattr(self.params,"volume")
            pause = getattr(self.params,"pause")

        if pause == 1:
            time.sleep(0.1)     
        else:
            if self.params.signal == signalType.sine:
                # generate samples, note conversion to float32 array
                samples = (np.sin(2*np.pi*np.arange(2*self.frames)*f/self.fs)).astype(np.float32)
                # play. May repeat with different volume values (if done interactively) 
                self.stream.write(volume*samples)
            elif self.params.signal == signalType.pink_noise:
                self.stream.write(volume*self.noise)

    def stop(self):
        if internalPlayer:
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
