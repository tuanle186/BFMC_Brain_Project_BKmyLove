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

class AverageCal:
    def __init__(self, max_size=5):
        self.max_size = max_size
        self.data = []

    
    def add_element(self, new_element):
        if len(self.data) == self.max_size:
            self.data.pop()
        self.data.insert(0, new_element)

    
    def calculate_average(self):
        if not self.data:
            return None
        return sum(self.data) / len(self.data)    


class ThreadVehicleControl(ThreadWithStop):
    def __init__(self, pipeRecv, pipeSend, queuesList, logger, debugger):
        super(ThreadVehicleControl, self).__init__()
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
                "To": {"receiver": "threadVehicleControl", "pipe": self.pipeSend},
            }
        )

    def stop(self):
        super(ThreadVehicleControl, self).stop()


    def run(self):
        while self._running:
            try:
                if self.pipeRecv.poll():
                    msg = self.pipeRecv.recv()
                    self.queuesList[SpeedMotor.Queue.value].put(
                        {
                            "Owner": SpeedMotor.Owner.value,
                            "msgID": SpeedMotor.msgID.value,
                            "msgType": SpeedMotor.msgType.value,
                            "msgValue": 30,
                        }
                    )
                    
                    steerAngle = 1*float(msg["value"])
                    if steerAngle > 20:
                        steerAngle = 25
                    elif steerAngle < -20:
                        steerAngle = -25
                    # else

                    self.queuesList[SteerMotor.Queue.value].put(
                        {
                            "Owner": SteerMotor.Owner.value,
                            "msgID": SteerMotor.msgID.value,
                            "msgType": SteerMotor.msgType.value,
                            "msgValue": steerAngle,
                        }
                    )
                    

            except Exception as e:
                print(e)

            if self.debugger:
                self.logger.warning("VehicleCtrl is running")

    def start(self):
        super(ThreadVehicleControl, self).start()
