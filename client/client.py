import asyncio
import cv2
import os
from ascii import covertImageToAscii
from websockets.asyncio.client import connect
from PIL import Image


class Client:
    def __init__(self, ws_url="ws://localhost:8001/room1"):
        self.ws_url = ws_url
        self.websocket = None
        self.connected = False

    async def connect_to_server(self):
        self.websocket = await connect(self.ws_url)
        

    async def handle_server(self):
        try:

            while self.connected:
                message = await self.websocket.recv()
                print(message)

                # os.system('cls' if os.name == 'nt' else 'clear')
                await asyncio.sleep(0.1)

        except: 
            print("Error recieving messages")

    async def handle_webcam(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open webcam")
            exit()

        try:
            while self.connected:
                ret, frame = cap.read()
                pil_image = Image.fromarray(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                )

                frame = pil_image.convert('L')
                converted_frame = covertImageToAscii(
                    frame,
                    100,
                    0.43,
                    False
                )

                
                frame = '\n'.join(converted_frame)

                # sends ascii frame to server
                await self.websocket.send(frame)


                await asyncio.sleep(0.033)  # About 30fps

                if not ret:
                    print("Error, could not read frame")
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release
            cap.destroyAllWindows()
        

    async def start(self):
        await self.connect_to_server()
        self.connected = True

        await asyncio.gather(
            self.handle_webcam(),
            self.handle_server(),
        )
