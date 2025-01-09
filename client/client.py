import asyncio
from websockets.asyncio.client import connect
from webcam import start_webcam
import cv2
from PIL import Image
from ascii import covertImageToAscii, print_aimg
import os


class Client:
    def __init__(self, ws_url="ws://localhost:8001"):
        self.ws_url = ws_url
        self.websocket = None
        self.connected = False

    async def connect_to_server(self):
        self.websocket = await connect(self.ws_url)

    async def handle_server(self):
        while self.connected:
            message = await self.websocket.recv()
            print("message: ", message)

    async def handle_webcam(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open webcam")
            exit()

        try:
            while self.connected:
                await self.websocket.send("testing")

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

                os.system('cls' if os.name == 'nt' else 'clear')
                print_aimg(converted_frame)


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
            self.handle_server(),
            self.handle_webcam()
        )
