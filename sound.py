import pygame
import os
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def play_audio(filename):
 
    
    file_path = os.path.join(BASE_DIR, filename)


    if not os.path.exists(file_path):
        print("Error: File not found at {file_path}")
        print("Make sure the file is inside the '375-Dog-training-project' folder.")
        return

   
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    try:
        print("Loading: {filename}...")
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        print("Playing...")
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        print("Playback finished.")

    except pygame.error as e:
        print("Pygame Error: {e}")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    # Test with your fixed file
    play_audio("sit_fixed.wav")
    play_audio("goodboy_fixed.wav")
