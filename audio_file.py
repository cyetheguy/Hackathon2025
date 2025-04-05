import pygame

# Initialize the mixer globally
pygame.mixer.init()

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
            pygame.mixer.music.load(sound_path)
             # Set theme-specific volume
            if theme == "dark":
                pygame.mixer.music.set_volume(0.3)  # Rain super loud so decrease volume

            pygame.mixer.music.play(-1, fade_ms=2000)  # loop forever, fade in

    def stop(self):
        pygame.mixer.music.stop()
