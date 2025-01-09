#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve, ServerConnection
from websockets.exceptions import ConnectionClosedOK
from room import Room
from typing import Dict

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.rooms: Dict[str, Room] = {}

    async def handler(self, websocket: ServerConnection):
        path = websocket.request.path

        try:
            if path.split("/")[-1] == "":
                await websocket.send("Error: please provide a pathname")
                await websocket.close()
                return

            room_name = path.split("/")[-1]
            if room_name not in self.rooms:
                self.rooms[room_name] = Room()
                self.rooms[room_name].add(websocket)
            else:
                self.rooms[room_name].add(websocket)

            print("Client: ", websocket, " connected to: ", room_name)

            while True:
                async for message in websocket:
                    target_room = self.rooms[room_name]
                    target_room.send_to_members(message)
                    
                    print(message)
        except ConnectionClosedOK:
            print("Client disconnected from path: ", path)

    async def start(self):
        async with serve(self.handler, self.host, self.port):
            print("ws server started on port: ", self.port)
            await asyncio.get_running_loop().create_future()



async def main():
    server = Server("localhost", 8001)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())