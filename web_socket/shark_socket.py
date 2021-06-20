import websockets
import asyncio
from PIL import Image
from io import BytesIO
import json

USERS = set()

STOP = False


class SharkSocket:
    def __init__(self, port):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        self.start_server = websockets.serve(main_logic, port=port)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_server)

        loop.run_forever()

    @staticmethod
    def close_all():

        print("closeAll")
        loop = asyncio.get_event_loop()
        # loop.call_soon_threadsafe(loop.stop())
        loop.stop()
        global STOP
        STOP = True
        print("STOP")
        # loop.close()
        print("loop.close()")

    @staticmethod
    def print_all_socket_connect():
        if len(USERS) == 0:
            print("连接数为0")
        [print(user) for user in USERS]


async def register(websocket):
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)


# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket, path):
    await register(websocket)
    try:
        await recv_msg(websocket)
    finally:
        await unregister(websocket)


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
# 当连接客户端断开时会抛出异常 从而退出循环 并且关闭连接
async def recv_msg(websocket):
    while not STOP:
        recv_text = await websocket.recv()

        # bytes_stream = BytesIO(recv_text)
        # roiimg = Image.open(bytes_stream)
        # roiimg.show()

        if isinstance(recv_text, str):
            print(recv_text)
            print(type(recv_text))
        elif isinstance(recv_text, bytes):
            bytes_stream = BytesIO(recv_text)
            roiimg = Image.open(bytes_stream)
            roiimg.show()

        # try:
        #     json_loads = json.loads(recv_text)
        # except ValueError as e:
        #     print(e)
        #     return

        # if json_loads['type'] == "TEXT":
        #     # print(json_loads['message'])
        #     bytes_data = json_loads['message'].encode("utf-8")
        #     # b = bytes(json_loads['message'])
        #     print(bytes_data)
        #     bytes_stream = BytesIO(bytes(bytes_data))
        #     roiimg = Image.open(bytes_stream)
        #     roiimg.show()
        # elif json_loads['type'] == "IMG":
        #     pass
        #     # print(type(json_loads['dataBuf']))
        #     # print("len: "+len(json_loads['dataBuf']))
        #     # data_bytes = bytes(json_loads['dataBuf'])
        #     # print(data_bytes)
        #     # bytes_stream = BytesIO(data_bytes)
        #     # roiimg = Image.open(bytes_stream)
        #     # roiimg.show()
