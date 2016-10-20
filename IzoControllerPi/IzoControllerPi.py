import threading

import generator
import parameters
import controller
import webGui
import os
threadLock = threading.Lock()
threads = []

Parameters = parameters.Params(0.9,44100,10*8810,440)

controller.initialize(Parameters,threadLock)
webGui.initialize(Parameters)
generatorThread = generator.Generator(Parameters,threadLock)
controllerThread = controller.Controller(Parameters,threadLock)
webGuiThread = webGui.webGui()

generatorThread.start()
controllerThread.start()
webGuiThread.start()

# Add threads to thread list
threads.append(generatorThread)
threads.append(controllerThread)

# Wait for all threads to complete
for t in threads:
    t.join()

generatorThread.stop()
print('Generator and controller stoped')
webGuiThread.stop()
webGuiThread.join()
print('Server stoped')

print("Exiting Main Thread")

