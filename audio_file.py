import pygame

# Initialize the mixer globally

class AudioManager:
    def __init__(self):
        self.current_sound = None
        self.sounds = {
            "light": "waves.mp3", 
            "dark": "rain.mp3"
        }

    def play_theme(self, theme: str):
        if self.current_sound:
            # fades out over 2 seconds
            pygame.mixer.music.fadeout(2000)  

        sound_path = self.sounds.get(theme)
        if sound_path:
            pygame.mixer.music.load(omni_dir(sound_path))
             # Set theme-specific volume
              # Rain super loud so decrease volume

            pygame.mixer.music.play(-1, fade_ms=2000)  # loop forever, fade in
