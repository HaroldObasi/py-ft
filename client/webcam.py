import cv2
from PIL import Image
from ascii import covertImageToAscii, print_aimg
import os

# Open a connection to the webcam (0 is the default camera)

def start_webcam():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # change frame to PIL image
        # OpenCV uses BGR format, convert to RGB for Pillow
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to Pillow Image
        pil_image = Image.fromarray(rgb_frame)

        # convert pill image to ascii
        frame = pil_image.convert('L')
        converted_frame = covertImageToAscii(frame, 100, 0.43, False)

        # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        print_aimg(converted_frame)


        # print("frame: ", frame)q

        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the resulting frame
        # cv2.imshow('Webcam', frame)

        # Press 'q' to exit the video window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()