#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve, ServerConnection
from websockets.exceptions import ConnectionClosedOK


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def serve(self):
        pass


async def handler(websocket: ServerConnection):
    path = websocket.request.path
    print("Client connected to path: ", path)

    await websocket.send("Connected to room: " + path)
    while True:
        async for message in websocket:
            print(message)

            await websocket.send("Hello world!")



async def main():
    PORT = 8001
    async with serve(handler, "", PORT):
        print("ws server started on port: ", PORT)
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())