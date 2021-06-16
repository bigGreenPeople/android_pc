import websockets
import asyncio

USERS = set()


class SharkSocket:
    def __init__(self, port):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        self.start_server = websockets.serve(main_logic, port=port)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_server)
        loop.run_forever()

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
    while True:
        recv_text = await websocket.recv()
        print(recv_text)
