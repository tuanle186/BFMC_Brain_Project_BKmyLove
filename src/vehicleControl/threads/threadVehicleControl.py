import threading
import time

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
                    if msg["value"] == "parking":
                        print("threadParking is running")

                        message_values = [
                            {"Speed": 45, "Time": 0.8, "Steer": -23},
                            {"Speed": 40, "Time": 0.9, "Steer": 0},
                            {"Speed": 40, "Time": 0.5, "Steer": 23},
                            {"Speed": 0, "Time": 0.5, "Steer": -23},
                            {"Speed": -45, "Time": 0.6, "Steer": -23},  
                            {"Speed": 0, "Time": 2, "Steer": 0},
                            {"Speed": -40, "Time": 0.5, "Steer": 0},
                            {"Speed": 0, "Time": 1, "Steer": 23},
                            {"Speed": 45, "Time": 0.8, "Steer": 23},
                            {"Speed": 45, "Time": 1.3, "Steer": -23}
                        ]
                        #Parking slot in
                        for msg_value in message_values:
                            self.queuesList[Control.Queue.value].put(
                                {
                                    "Owner": Control.Owner.value,
                                    "msgID": Control.msgID.value,
                                    "msgType": Control.msgType.value,
                                    "msgValue": msg_value,
                                }
                            )
                            time.sleep(msg_value["Time"] + 0.1)
                    else:
                        self.queuesList[SpeedMotor.Queue.value].put(
                            {
                                "Owner": SpeedMotor.Owner.value,
                                "msgID": SpeedMotor.msgID.value,
                                "msgType": SpeedMotor.msgType.value,
                                "msgValue": 30,
                            }
                        )
                        
                        steerAngle = 1*float(msg["value"])
                        # if steerAngle > 60:
                        #     steerAngle = 25
                        # elif steerAngle < -60:
                        #     steerAngle = -25
                        # elif 40 < steerAngle < 60:
                        #     steerAngle = 20
                        # elif -60 < steerAngle < -40:
                        #     steerAngle = -20
                        # elif 20 < steerAngle < 40:
                        #     steerAngle = 15
                        # elif -40 < steerAngle < -20:
                        #     steerAngle = -15
                        # elif 0 < steerAngle < 20:
                        #     steerAngle = 5
                        # elif -20 < steerAngle < 0:
                        #     steerAngle = -5

                        if steerAngle > 20:
                            steerAngle = 25
                        elif steerAngle < -20:
                            steerAngle = -25

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
