import threading
import time
from parameters import Params

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
        print("Press 'z' to decrese the frequecy")

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