import threading

from multiprocessing import Pipe
# from src.utils.messages.allMessages import (
#     mainCamera,
#     serialCamera,
#     Recording,
#     Record,
#     Config,
# )
from src.templates.threadwithstop import ThreadWithStop


class ThreadCtrlMethod(ThreadWithStop):
    def __init__(self, pipeRecv, pipeSend, queuesList, logger, debugger):
        super(ThreadCtrlMethod, self).__init__()
        self.queuesList = queuesList
        self.logger = logger
        self.pipeRecv = pipeRecv
        self.pipeSend = pipeSend
        self.debugger = debugger
        self.subscribe()

    def subscribe(self):
        # Subscribe to receive message from imageProcessingModule
        return 0

    def stop(self):
        super(ThreadCtrlMethod, self).stop()

    def run(self):
        while self._running:
            try:
                print("Hello World!")
                # Your logic for handling vehicle control goes here

            except Exception as e:
                print(e)

            if self.debugger:
                self.logger.warning("VehicleCtrlMethod is running")

    def start(self):
        super(ThreadCtrlMethod, self).start()