import pygame
import os
import time

# --- PATH SETUP ---
# This finds the folder where THIS script is currently saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def play_audio(filename):
    """
    Plays an audio file located in the same folder as this script.
    Supports WAV (PCM 16-bit) and MP3.
    """
    # Create the full path to the file
    file_path = os.path.join(BASE_DIR, filename)

    # 1. Check if the file actually exists before trying to play it
    if not os.path.exists(file_path):
        print("Error: File not found at {file_path}")
        print("Make sure the file is inside the '375-Dog-training-project' folder.")
        return

    # 2. Initialize the mixer (Pre-init helps with high-quality WAVs)
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    try:
        print("Loading: {filename}...")
        # Use music.load instead of Sound() for better format support
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        print(f"Playing...")
        # Keep the script alive while the music plays
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        print("Playback finished.")

    except pygame.error as e:
        print("Pygame Error: {e}")
    finally:
        # Clean up the mixer so the file isn't "locked" by Windows
        pygame.mixer.quit()

if __name__ == "__main__":
    # Test with your fixed file
    play_audio("sit_fixed.wav")
    play_audio("goodboy_fixed.wav")
