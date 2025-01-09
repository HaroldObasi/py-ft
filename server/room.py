from websockets.asyncio.server import ServerConnection

class Room:
    def __init__(self):
        self.members = []

    def add(self, ws: ServerConnection):
        self.members.append(ws)