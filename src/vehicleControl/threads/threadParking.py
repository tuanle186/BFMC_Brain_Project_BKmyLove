import threading

from multiprocessing import Pipe
from src.utils.messages.allMessages import (
    LaneDetect,
    SpeedMotor,
    SteerMotor,
    Control,
    Brake,
)
from src.templates.threadwithstop import ThreadWithStop

# class AverageCal:
#     def __init__(self, max_size=5):
#         self.max_size = max_size
#         self.data = []

    
#     def add_element(self, new_element):
#         if len(self.data) == self.max_size:
#             self.data.pop()
#         self.data.insert(0, new_element)

    
#     def calculate_average(self):
#         if not self.data:
#             return None
#         return sum(self.data) / len(self.data)    


class ThreadParking(ThreadWithStop):
    def __init__(self, pipeRecv, pipeSend, queuesList, logger, debugger):
        super(ThreadParking, self).__init__()
        self.queuesList = queuesList
        self.logger = logger
        self.pipeRecv = pipeRecv
        self.pipeSend = pipeSend
        self.debugger = debugger
        self.subscribe()

    def subscribe(self):
        self.queuesList["Config"].put(
            {
                "Subscribe/Unsubscribe": "subscribe",
                "Owner": LaneDetect.Owner.value,
                "msgID": LaneDetect.msgID.value,
                "To": {"receiver": "ThreadParking", "pipe": self.pipeSend},
            }
        )

    def stop(self):
        super(ThreadParking, self).stop()


    def run(self):
        if self._running:
            try:
                # if self.pipeRecv.poll():
                # msg = self.pipeRecv.recv()
                self.queuesList[Control.Queue.value].put(
                    {
                        "Owner": Control.Owner.value, 
                        "msgID": Control.msgID.value,
                        "msgType": Control.msgType.value,
                        "msgValue": {"Speed" : 30, "Time": 10, "Steer":25},
                    }
                )
                # self.queuesList[SteerMotor.Queue.value].put(
                #     {
                #         "Owner": SteerMotor.Owner.value,
                #         "msgID": SteerMotor.msgID.value,
                #         "msgType": SteerMotor.msgType.value,
                #         "msgValue": 25,
                #     }
                # )
                    

            except Exception as e:
                print(e)

            if self.debugger:
                self.logger.warning("VehicleCtrl is running")

    def start(self):
        super(ThreadParking, self).start()
