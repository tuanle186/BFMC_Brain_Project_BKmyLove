# Code implemented by BKmyLove
# Created: 20th January 2024
# Author: Le Quoc Tuan

if __name__ == "__main__":
    import sys

    sys.path.insert(0, "../..")
from src.templates.workerprocess import WorkerProcess
from src.vehicleControl.threads.threadVehicleControl import threadVehicleControl
from multiprocessing import Pipe

class processVehicleControl(WorkerProcess):
    """
    """

    def __init__(self, queueList, logging, debugging=False):
        self.queuesList = queueList
        self.logging = logging
        pipeRecv, pipeSend = Pipe(duplex=False)
        self.pipeRecv = pipeRecv
        self.pipeSend = pipeSend
        self.debugging = debugging
        super(processVehicleControl, self).__init__(queueList)

    # ===================================== STOP ==========================================

    def stop(self):
        """Function for stopping threads and the process."""
        for thread in self.threads:
            thread.stop()
            thread.join()
        super(processVehicleControl, self).stop()

    # ===================================== RUN ===========================================
    def run(self):
        """Apply the initializing methods and start the threads."""
        super(processVehicleControl, self).run()

    # ===================================== INIT TH ==========================================
    def _init_threads(self):
        """Initializes the gateway thread."""
        vehicleControlThread = threadVehicleControl(self.queuesList, self.logger, self.debugging)
        self.threads.append(vehicleControlThread)


# =================================== EXAMPLE =========================================
#             ++    THIS WILL RUN ONLY IF YOU RUN THE CODE Owner HERE  ++
#                  in terminal:    python3 processVehicleControl.py

if __name__ == "__main__":
    print("Hello world!")