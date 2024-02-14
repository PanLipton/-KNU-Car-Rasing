import pygame
class Sound:
    def __init__(self, file_path):
        self.sound = pygame.mixer.Sound(file_path)

    def play(self):
        pygame.mixer.Sound.play(self.sound)

    def set_volume(self, volume):
        self.sound.set_volume(volume)

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        # Звуки для різних подій
        self.music_menu = Sound('../../assets/music/musicMenu.mp3')
        self.music_game = Sound('../../assets/music/musicGame.mp3')
        self.sound_button = Sound('../../assets/music/soundButton.mp3')
        self.sound_crash = Sound('../../assets/music/soundCollision.mp3')
        self.sound_car = Sound('../../assets/music/musicCarSound.mp3')
        self.sound_vroom = Sound('../../assets/music/musicCarVroom.mp3')

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

    def playSoundCar(self):
        self.sound_car.play()

    def playSoundVroom(self):
        self.sound_vroom.play()

    def setMusicMenuVolume(self, volume):
        self.music_menu.set_volume(volume)

    def stop_all(self):
        pygame.mixer.stop()