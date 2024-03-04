import pygame
from pathlib import Path
import struct
class Sound:
    def init(self, file_path):
        self.sound = pygame.mixer.Sound(file_path)

    def play(self):
        pygame.mixer.Sound.play(self.sound)

    def set_volume(self, volume):
        self.sound.set_volume(volume)


class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        pygame.mixer.init()

        # Звуки для різних подій
        self.music_menu = Sound(Path('../assets/music/musicMenu.mp3'))
        self.music_game = Sound(Path('../assets/music/musicGame.mp3'))
        self.sound_button = Sound(Path('../assets/music/soundButton.mp3'))
        self.sound_crash = Sound(Path('../assets/music/soundCollision.mp3'))
        self.sound_win = Sound(Path('../assets/music/soundWin.mp3'))
        self.sound_lose = Sound(Path('../assets/music/soundLose.mp3'))


    def playMusicMenu(self):
        self.stop_all()
        self.music_menu.play()

    def playMusicGame(self):
        self.stop_all()
        self.music_game.play()

    def playSoundButton(self):
        self.sound_button.play()

    def playSoundCrash(self):
        self.sound_crash.play()

    def playSoundWin(self):
        self.sound_win.play()

    def playSoundLose(self):
        self.sound_lose.play()


    def setMusicVolume(self, volume):
        data = struct.pack('f', volume)
        with open("../assets/bin/volume.bin","wb") as f:
            f.write(data)
        self.music_game.set_volume(volume)
        self.music_menu.set_volume(volume)




    def stop_all(self):
        pygame.mixer.stop()


sound_manager = SoundManager()


