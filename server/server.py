#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve, ServerConnection
from websockets.exceptions import ConnectionClosedOK
from room import Room


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.rooms = {}

    async def handler(self, websocket: ServerConnection):
        path = websocket.request.path
        print("Client connected to path: ", path)

        try:
            if path.split("/")[-1] == "":
                await websocket.send("Error: please provide a pathname")
                await websocket.close()
                return

            room_name = path.split("/")[-1]
            if room_name not in self.rooms:
                self.rooms[room_name] = Room()
                self.rooms[room_name].add(websocket)

            print("rooms: ", self.rooms)

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