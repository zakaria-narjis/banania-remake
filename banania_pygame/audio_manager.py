# audio_manager.py
import pygame
from config import DEFAULT_VOLUME

class AudioManager:
    """A dedicated class to handle loading and playing sounds and music."""
    def __init__(self):
        try:
            pygame.mixer.init()
            self.sounds = {}
            self.volume = DEFAULT_VOLUME
            self.sound_enabled = True
            print("Audio Manager initialized.")
        except pygame.error as e:
            self.sounds = None
            print(f"Error initializing audio manager: {e}. Sound will be disabled.")

    def load_sound(self, name, file_path):
        """Loads a sound effect and stores it in the library."""
        if not self.sounds: return
        try:
            self.sounds[name] = pygame.mixer.Sound(file_path)
        except pygame.error as e:
            print(f"Could not load sound '{name}' from {file_path}: {e}")

    def play_sound(self, name):
        """Plays a loaded sound effect if sound is enabled."""
        if not self.sounds or not self.sound_enabled: return
        if name in self.sounds:
            self.sounds[name].set_volume(self.volume)
            self.sounds[name].play()
        else:
            print(f"Warning: Sound '{name}' not found.")

    def set_volume(self, volume_level):
        """Sets the master volume for all sound effects."""
        if not self.sounds: return
        # Clamp volume between 0.0 and 1.0
        self.volume = max(0.0, min(1.0, volume_level))
    
    def toggle_sound(self, enabled):
        """Enables or disables sound playback."""
        self.sound_enabled = enabled