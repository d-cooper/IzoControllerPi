import threading
import time
from parameters import Params, signalType

class Controller(threading.Thread):

    def __init__(self, params, lock):
        threading.Thread.__init__(self)
        self.name = "controller"
        self.lock = lock
        self.params = params
        return

    def run(self):
        print("Starting " + self.name)   
        while self.params.play:
            self.waitForInput()
        print("Exiting " + self.name)
        return

    def waitForInput(self):
        print("Press 'e' to exit")
        print("Press 'a' to increase the frequecy")
        print("Press 'z' to decrease the frequecy")
        print("Press 't' to togle sine and noise")

        keypressed = input("Pressed key is: ")
        print(keypressed)
        if keypressed == "e":
            with self.lock:
                self.params.play = False

        elif keypressed == "a":
            with self.lock:
                self.params.f += 10
            print("Current frequency is "+ str(self.params.f))

        elif keypressed == "z":
            with self.lock:
                self.params.f -= 10
            print("Current frequency is "+ str(self.params.f))

        elif keypressed == "t":
            with self.lock:
                if self.params.signal == signalType.pink_noise:
                    self.params.signal = signalType.sine

                elif self.params.signal == signalType.sine:
                    self.params.signal = signalType.pink_noise