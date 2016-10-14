import threading

import generator
import parameters
import controller
import os
threadLock = threading.Lock()
threads = []
os.system('amixer sset PCM 90%')
os.system('amixer sset PCM unmute')
Parameters = parameters.Params(0.9,44100,1,440)
generatorThread = generator.Generator(Parameters,threadLock)
controllerThread = controller.Controller(Parameters,threadLock)

generatorThread.start()
controllerThread.start()

# Add threads to thread list
threads.append(generatorThread)
threads.append(controllerThread)

# Wait for all threads to complete
for t in threads:
    t.join()

generatorThread.stop()
print("Exiting Main Thread")

