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
        raise ValueError("Слишком большое разрешение для ASCII-арта.")
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
        raise ValueError(f"Не удалось открыть видео: {video_path}")
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
    print("Добро пожаловать в ASCII Video!")
    print("Чтобы ваше видео превратилось в ASCII-арт, убедитесь, что следующие библиотеки установлены:")
    print("- opencv-python (pip install opencv-python)")
    print("- numpy (pip install numpy)")
    print("Видео должно находиться в одной папке с этим файлом.")
    print("Нажмите цифру (1), чтобы начать.")

def get_video_filename():
    while True:
        filename = input("Введите название файла с видео (например, BadApple.mp4) (обязательно с расширением!): ")
        if os.path.exists(filename):
            return filename
        else:
            print("Файл не найден. Убедитесь, что видео находится в той же папке, и введите название снова.")

if __name__ == "__main__":
    try:
        display_welcome_message()
        user_input = input()
        if user_input == "1":
            video_filename = get_video_filename()
            play_bad_apple(video_filename)
        else:
            print("Неверный ввод. Завершение программы.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        time.sleep(5)