import threading

import generator
import parameters
import controller
import webGui
import os
threadLock = threading.Lock()
threads = []

Parameters = parameters.Params(0.9,44100,10*4410,500)

controller.initialize(Parameters,threadLock)
webGui.initialize(Parameters)
generatorThread = generator.Generator(Parameters,threadLock)
controllerThread = controller.Controller(Parameters,threadLock)

generatorThread.start()
controllerThread.start()
webGui.run()

# Add threads to thread list
threads.append(generatorThread)
threads.append(controllerThread)

# Wait for all threads to complete
for t in threads:
    t.join()

generatorThread.stop()
print('Generator and controller stoped')
webGui.shutdown_server()
print('Server stoped')

print("Exiting Main Thread")

