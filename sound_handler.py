# sound_handler.py
import pygame
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def play_audio(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    finally:
        pygame.mixer.quit()
