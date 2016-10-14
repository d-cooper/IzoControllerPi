import threading
import time
import RPi.GPIO as GPIO
import os
from parameters import Params, signalType

class Controller(threading.Thread):

    def __init__(self, params, lock):
        threading.Thread.__init__(self)
        self.name = "controller"
        self.lock = lock
        self.params = params

        GPIO.setmode(GPIO.BCM)
        chan_list = [14,15,17,18]
        GPIO.setup(chan_list, GPIO.IN)
        return

    def run(self):
        print("Starting " + self.name)  
        
        while self.params.play:
            self.waitForPilotInput()
                 
        #while self.params.play:
        #    self.waitForKeyInput()

        print("Exiting " + self.name)
        return

    def waitForKeyInput(self):
        print("Press 'e' to exit")
        print("Press 'a' to increase the volume")
        print("Press 'z' to decrease the volume")
        print("Press 'p' to pause")
        print("Press 't' to togle sine and noise")
        keypressed = input("Pressed key is: ")
        if keypressed == "e":
            self.stopPlayback

        elif keypressed == "a":
            self.volUp

        elif keypressed == "z":
            self.volDown

        elif keypressed == "t":
            self.toogleSignal
        
        elif keypressed == "p":
            self.toglePause

    def waitForPilotInput(self):     
        ch14 = GPIO.input(14)
        ch15 = GPIO.input(15)
        ch17 = GPIO.input(17)
        ch18 = GPIO.input(18)

        if (ch18==1 and ch14==1):
            self.stopPlayback()
        if (ch14==1 and ch18==0):
            self.toglePause()
        if ch17==1:
            self.volUp()
        if ch15==1:
            self.volDown()  


        time.sleep(0.1)
           
    def toglePause(self):
        with self.lock:
            if self.params.pause == 0:
                self.params.pause = 1
                os.system('amixer sset PCM toggle')
                print("Playback paused")
                time.sleep(1)
                
            elif self.params.pause == 1:
                self.params.pause = 0
                os.system('amixer sset PCM toggle')
                print("Playback resumed")
                time.sleep(1)
        

    def volUp(self):
        os.system('amixer sset PCM 3dB+')
        #with self.lock:          
            #self.params.volume += 0.05
        #print("Current volume is "+ str(self.params.volume))

    def volDown(self):
        os.system('amixer sset PCM 3dB-')
        #with self.lock:
            #self.params.volume -= 0.05
        #print("Current volume is "+ str(self.params.volume))

    def stopPlayback(self):
        with self.lock:
            #os.system('amixer sset PCM 0%%')
            self.params.play = False
        print("Playback stoped. Exiting")

    def toogleSignal(self):
        with self.lock:
            if self.params.signal == signalType.pink_noise:
                self.params.signal = signalType.sine

            elif self.params.signal == signalType.sine:
                self.params.signal = signalType.pink_noise

