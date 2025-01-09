from websockets.asyncio.server import ServerConnection, broadcast

class Room:
    def __init__(self):
        self.members = []

    def add(self, ws: ServerConnection):
        self.members.append(ws)

    def send_to_members(self, message: str):
        broadcast(self.members, message=message)