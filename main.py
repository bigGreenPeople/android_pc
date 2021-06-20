import sys

import adbutils
import web_socket
from web_socket.shark_socket import SharkSocket
import json
import threading
import requests
import ctypes
import inspect


class SocketThread(threading.Thread):
    def run(self):
        print(f"开启Socket线程：  {threading.current_thread().name} \n")
        self.socket = SharkSocket(9873)
        print("结束Socket线程： " + threading.current_thread().name + "\n")

    def closeAll(self):
        SharkSocket.close_all()


def input_fun():
    while True:
        print("input text:\n")
        s = input()

        if s == "all":
            SharkSocket.print_all_socket_connect()
        elif s == "stop":
            thread.closeAll()
            stop_thread(thread)
            # sys.exit()
            # return


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            # pass
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)


def stop_thread(thread):
    """终止线程"""
    _async_raise(thread.ident, SystemExit)

thread = SocketThread()
thread.start()

input_fun()
# thread.join()
print("主线程退出")
