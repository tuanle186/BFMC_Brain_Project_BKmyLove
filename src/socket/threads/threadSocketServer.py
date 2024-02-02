import socket, threading
from multiprocessing import Pipe

from src.templates.threadwithstop import ThreadWithStop
from src.utils.messages.allMessages import (
    mainCamera,
    serialCamera,
    Recording,
    Record,
    Config,
    LaneDetect
)
class Server(ThreadWithStop):
    def __init__(self, queueList, logger, debugger):
        super(Server, self).__init__()
        self.queueList = queueList
        self.logger = logger
        self.debugger = debugger
        self._init_server()

    def _init_server(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connections = {}

    # =============================== START ===============================================
    def start(self):
        try:
            with self.server_socket as s:
                s.bind((self.host, self.port))
                s.listen()
                print(f"Server is listening on {self.host}:{self.port}")

                while True:
                    conn, addr = s.accept()
                    client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                    client_thread.start()
        except OSError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("Server interrupted. Closing connections.")
            self.close_connections()

    def server_recv(self, server_socket, ip):
        while True:
            try:
                data = server_socket.recv(1024).decode("utf-8").strip()
                if not data:
                    break
                # print(data)
                self.queueList["Critical"].put(
                    {
                        "Owner": LaneDetect.Owner.value,
                        "msgID": LaneDetect.msgID.value,
                        "msgType": LaneDetect.msgType.value,
                        "msgValue": data,
                    }
                )
            except ConnectionResetError:
                break

        del self.client_connections[ip]
        print(f"Client {ip} disconnected")
        server_socket.close()

    def handle_client(self, server_socket, addr):
        ip = addr[0]
        print(f'Connected to {addr}')
        self.client_connections[ip] = server_socket
        threading.Thread(target=self.server_recv, args=(server_socket, ip), daemon=True).start()


    def close_connections(self):
        for client_socket in self.client_connections.values():
            client_socket.close()

if __name__ == "__main__":
    server = Server()

    # Start a thread for receiving messages
    # threading.Thread(target=server.server_input).start()
    server.start()
