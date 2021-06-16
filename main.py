import adbutils
import web_socket
from web_socket.shark_socket import SharkSocket
import json
import threading
import requests


class SocketThread(threading.Thread):
    def run(self):
        print(f"开启Socket线程：  {threading.current_thread().name} \n")
        socket = SharkSocket(9873)
        print("结束Socket线程： " + threading.current_thread().name + "\n")


def input_fun():
    print("input text:\n")
    s = input()

    if s == "all":
        SharkSocket.print_all_socket_connect()


thread = SocketThread()
thread.start()
while True:
    input_fun()
thread.join()
print("主线程退出")
