import cv2
import numpy as np
import time
import os

def convert_frame_to_ascii(frame, cols=80, scale=0.43):
    height, width = frame.shape
    cell_width = width / cols
    cell_height = 2 * cell_width
    rows = int(height / cell_height)
    if cols > width or rows > height:
        raise ValueError("The resolution is too high for ASCII art.")
    ascii_frame = ""
    for i in range(rows):
        for j in range(cols):
            x = int(j * cell_width)
            y = int(i * cell_height)
            brightness = frame[y, x]
            ascii_frame += get_ascii_char(brightness)
        ascii_frame += "\n"
    return ascii_frame

def get_ascii_char(brightness):
    ascii_chars = "@%#*+=-:. "
    index = int(brightness / 255 * (len(ascii_chars) - 1))
    return ascii_chars[index]

def play_bad_apple(video_path, cols=80):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Couldn't open the video: {video_path}")
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small_frame = cv2.resize(gray_frame, (cols, int(cols * 0.5)))
            ascii_frame = convert_frame_to_ascii(small_frame, cols)
            print("\033[H" + ascii_frame, end="")
            time.sleep(1 / 30)
    finally:
        cap.release()

def display_welcome_message():
    print(r"""
    
░█▀▀█ ▒█▀▀▀█ ▒█▀▀█ ▀█▀ ▀█▀ 　 ▒█░░▒█ ▀█▀ ▒█▀▀▄ ▒█▀▀▀ ▒█▀▀▀█ 
▒█▄▄█ ░▀▀▀▄▄ ▒█░░░ ▒█░ ▒█░ 　 ░▒█▒█░ ▒█░ ▒█░▒█ ▒█▀▀▀ ▒█░░▒█ 
▒█░▒█ ▒█▄▄▄█ ▒█▄▄█ ▄█▄ ▄█▄ 　 ░░▀▄▀░ ▄█▄ ▒█▄▄▀ ▒█▄▄▄ ▒█▄▄▄█

    """)
    print("Welcome to ASCII Video!")
    print("To turn your video into ASCII art, make sure that the following libraries are installed:")
    print("- opencv-python (pip install opencv-python)")
    print("- numpy (pip install numpy)")
    print("The video must be in the same folder as this file.")
    print("Press the number (1) to start.")

def get_video_filename():
    while True:
        filename = input("Enter the name of the video file (for example, BadApple.mp4) (with the extension required!): ")
        if os.path.exists(filename):
            return filename
        else:
            print("The file was not found. Make sure that the video is in the same folder and enter the title again.")

if __name__ == "__main__":
    try:
        display_welcome_message()
        user_input = input()
        if user_input == "1":
            video_filename = get_video_filename()
            play_bad_apple(video_filename)
        else:
            print("Incorrect input. Completion of the program.")
    except Exception as e:
        print(f"An error has occurred: {e}")
    finally:
        time.sleep(5)