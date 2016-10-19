import threading
import time
import RPi.GPIO as GPIO
import os
from parameters import Params, signalType

cardName = "'HPOUT2 Digital'"   # Use for Cirrus Audio Card
#cardName = 'PCM'               # Use for internal audio    

class Controller(threading.Thread):

    def __init__(self, params, lock):
        threading.Thread.__init__(self)
        self.name = "controller"
        self.lock = lock
        self.params = params

        os.system('amixer sset '+ cardName +' 50%')
        os.system('amixer sset '+ cardName +' unmute')

        GPIO.setmode(GPIO.BCM)
        #self.chan_list = [5,6,12,26]
        self.chan_list = [26,12,6,5]
        #chan_list = [14,15,17,18]
        GPIO.setup(self.chan_list, GPIO.IN)
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
        ch0 = GPIO.input(self.chan_list[0])
        ch1 = GPIO.input(self.chan_list[1])
        ch2 = GPIO.input(self.chan_list[2])
        ch3 = GPIO.input(self.chan_list[3])

        if (ch3==1 and ch0==1):
            self.stopPlayback()
        if (ch0==1 and ch3==0):
            self.toglePause()
        if ch2==1:
            self.volUp()
        if ch1==1:
            self.volDown()  


        time.sleep(0.1)
           
    def toglePause(self):
        with self.lock:
            if self.params.pause == 0:
                self.params.pause = 1
                os.system('amixer sset '+ cardName +' toggle')
                print("Playback paused")
                time.sleep(1)
                
            elif self.params.pause == 1:
                self.params.pause = 0
                os.system('amixer sset '+ cardName +' toggle')
                print("Playback resumed")
                time.sleep(1)
        

    def volUp(self):
        os.system('amixer sset '+ cardName +' 3dB+')
        #with self.lock:   
            #self.params.volume += 0.05
        #print("Current volume is "+ str(self.params.volume))

    def volDown(self):
        os.system('amixer sset '+ cardName +' 3dB-')
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

