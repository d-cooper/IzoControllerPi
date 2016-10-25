import threading
import time
import RPi.GPIO as GPIO
import os
from parameters import Params, signalType

cardName = "'HPOUT2 Digital'"   # Use for Cirrus Audio Card
#cardName = 'PCM'               # Use for internal audio

params = None
lock = None

def initialize(_params,_lock):
    global params
    global lock
    params=_params
    lock=_lock
              
def togglePause():
    with lock:
        if params.pause == 0:
            params.pause = 1
            os.system('amixer sset '+ cardName +' toggle')
            print("Playback paused")
            time.sleep(1)
                
        elif params.pause == 1:
            params.pause = 0
            os.system('amixer sset '+ cardName +' toggle')
            print("Playback resumed")
            time.sleep(1)
        

def volUp():
    os.system('amixer sset '+ cardName +' 3dB+')
    #with lock:   
    #    params.volume += 0.05
    #print("Current volume is "+ str(params.volume))

def volDown():
    os.system('amixer sset '+ cardName +' 3dB-')
    #with lock:
    #    params.volume -= 0.05
    #print("Current volume is "+ str(params.volume))

def stopPlayback():
    #os.system('amixer sset PCM 0%%')
    params.play = False
    print("Playback stoped. Exiting")

def toogleSignal():
    with lock:
        if params.signal == signalType.pink_noise:
            params.signal = signalType.sine

        elif params.signal == signalType.sine:
            params.signal = signalType.pink_noise


################ Keyboard and remote controller ##############################

class Controller(threading.Thread):

    def __init__(self, params, lock):
        threading.Thread.__init__(self)
        self.name = "controller"

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
        
        while params.play:
            self.waitForPilotInput()
                 
        #while params.play:
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
            stopPlayback()

        elif keypressed == "a":
            volUp()

        elif keypressed == "z":
            volDown()

        elif keypressed == "t":
            toogleSignal
        
        elif keypressed == "p":
            togglePause()

    def waitForPilotInput(self):     
        ch0 = GPIO.input(self.chan_list[0])
        ch1 = GPIO.input(self.chan_list[1])
        ch2 = GPIO.input(self.chan_list[2])
        ch3 = GPIO.input(self.chan_list[3])

        if (ch3==1 and ch0==1):
            stopPlayback()
        if (ch0==1 and ch3==0):
            togglePause()
        if ch2==1:
            volUp()
        if ch1==1:
            volDown()  


        time.sleep(0.1)
