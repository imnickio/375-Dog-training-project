import pygame
import time

# play audio function:

def play_audio(file_path):
    pygame.mixer.init()
    
    sound = pygame.mixer.Sound(file_path)
    
    print(f"Playing: {file_path}")
    sound.play()
    
    while pygame.mixer.get_busy():
        time.sleep(0.1)

if __name__ == "__main__":
    play_audio("test.wav")
