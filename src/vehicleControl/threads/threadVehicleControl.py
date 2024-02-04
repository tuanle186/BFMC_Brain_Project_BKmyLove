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
                            "msgValue": 10,
                        }
                    )
                    print(msg)
                    steerAngle = float(msg["value"])
                    if steerAngle > 25:
                        steerAngle = 25
                    elif steerAngle < -25:
                        steerAngle = -25
                    elif -10 < steerAngle < 10:
                        steerAngle = 0

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