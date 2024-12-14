from ascii import covertImageToAscii
from video import get_video_info, video_to_pillow_frames
from webcam import start_webcam


def save_converted(img: list[any], id: str):

    file = open(f"ascii_{id}.txt", "w")

    for i, frame in enumerate(img):

        file.write(frame)
        file.write("\n")


def main():
    start_webcam()


if __name__ == "__main__":
    main()