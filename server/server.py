#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve, ServerConnection
from websockets.exceptions import ConnectionClosedOK


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def handler(self, websocket: ServerConnection):
        path = websocket.request.path
        print("Client connected to path: ", path)

        try:
            await websocket.send("Connected to room: " + path)
            while True:
                async for message in websocket:
                    print(message)

                    await websocket.send("Hello world!")
        except ConnectionClosedOK:
            print("Client disconnected from path: ", path)

    async def start(self):
        async with serve(self.handler, self.host, self.port):
            print("ws server started on port: ", self.port)
            await asyncio.get_running_loop().create_future()


async def handler(websocket: ServerConnection):
    path = websocket.request.path
    print("Client connected to path: ", path)

    await websocket.send("Connected to room: " + path)
    while True:
        async for message in websocket:
            print(message)

            await websocket.send("Hello world!")



async def main():
    server = Server("localhost", 8001)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())