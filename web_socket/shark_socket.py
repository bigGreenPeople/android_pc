import websockets
import asyncio
from PIL import Image
from io import BytesIO
import json

USERS = set()

STOP = False


class SharkSocket:
    def __init__(self, port):
        self.port = port
        self._server = None
        self._task = None
        self.new_loop = None

    def start_server(self):
        self.new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.new_loop)
        print(self.port)
        self._server = websockets.serve(self.main_logic, port=self.port)
        # self._task = asyncio.ensure_future(self._server)
        asyncio.get_event_loop().run_until_complete(self._server)

        asyncio.get_event_loop().run_forever()
        # loop.run_until_complete(self._server)
        print("stop run_forever")

    def stop_server(self):
        # self._task.cancel()
        # print(asyncio.get_running_loop())
        print("stop_server")
        # self.new_loop.close()
        self.new_loop.stop()
        # asyncio.get_event_loop().stop()
        # asyncio.get_event_loop().close()
        # print(asyncio.get_event_loop().is_running())
        # print(asyncio.get_event_loop().is_closed())
        # print(self._task.cancelled())  # always False

    # 服务器端主逻辑
    # websocket和path是该函数被回调时自动传过来的，不需要自己传
    async def main_logic(self, websocket, path):
        await self.register(websocket)
        try:
            await self.recv_msg(websocket)
        finally:
            await self.unregister(websocket)

    @staticmethod
    def print_all_socket_connect():
        if len(USERS) == 0:
            print("连接数为0")
        [print(user) for user in USERS]

    async def register(self, websocket):
        USERS.add(websocket)

    async def unregister(self, websocket):
        USERS.remove(websocket)

    # 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
    # 当连接客户端断开时会抛出异常 从而退出循环 并且关闭连接
    async def recv_msg(self, websocket):
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
