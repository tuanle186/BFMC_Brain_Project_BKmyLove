import socket, threading
from multiprocessing import Pipe

from src.templates.threadwithstop import ThreadWithStop
from src.utils.messages.allMessages import (
    LaneDetect
)
class threadClientSocket(ThreadWithStop):
    def __init__(self, queueList, logger, debugger):
        super(threadClientSocket, self).__init__()
        self.queueList = queueList
        self.logger = logger
        self.debugger = debugger
        self._init_socket()

        # self.Queue_Sending()
        # self.Configs()

        
    
    def subscribe(self, message):
        """This functin will add the pipe into the approved messages list and it will be added into the dictionary of sending
        Args:
            message(dictionary): Dictionary received from the multiprocessing queues ( the config one).
        """
        pass
        

    def client_send(self):
        pass

    def client_recv(self):
        while self._running:
            try:
                data = self.client_socket.recv(1024).decode("utf-8").strip()
                self.queueList["Critical"].put(
                    {
                        "Owner": LaneDetect.Owner,
                        "msgID": LaneDetect.msgID,
                        "msgType": LaneDetect.msgType,
                        "msgValue": data
                    }
                )
                if self.debugger:
                    print(data)
            except ConnectionResetError:
                break
        pass

    def _init_socket(self, server_ip='localhost', server_port = 12345):
        '''This function will init the socket, connect to the server ip camera, recv msg from server ip camera then pass it to process gateway'''
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

    # =============================== START ===============================================
    def start(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        self.client_recv()
        super(threadClientSocket,self).start()

    # =============================== STOP ================================================
    def stop(self):
        """Stop the client by closing the socket."""

        self._running = False
        try:
            if self.client_socket.fileno() != -1 and self.client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ACCEPTCONN) == 0:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
                print("Disconnect to server")
        except OSError as e:
            # Handle specific errors if needed
            print(f"Error stopping the client: {e}")
