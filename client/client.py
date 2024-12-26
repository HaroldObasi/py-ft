import asyncio
from websockets.asyncio.client import connect

class Client:
    def __init__(self, ws_url):
        self.ws_url = "ws://localhost:8001"

    # method that connects to ws server
    async def connect(self):
        async with connect(self.ws_url) as websocket:
            await websocket.send("Hello world!")
            message = await websocket.recv()
            print(message)