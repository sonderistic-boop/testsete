import pygame as pg

class SoundManager:
    # This class is used to manage all the sounds in the game
    # OBJECTIVE 5.2 - SOUND DESIGN
    def __init__(self):
        self.sounds = {

        }
        self.sounds["music"] = pg.mixer.Sound("../shared/assets/audio/music.mp3")
        self.sounds["click"] = pg.mixer.Sound("../shared/assets/audio/click.mp3")
        self.sounds["alert"] = pg.mixer.Sound("../shared/assets/audio/alert.wav")
        self.sounds["leave"] = pg.mixer.Sound("../shared/assets/audio/leave.wav")

    

    def play(self, name):
        # This function is used to play a sound
        self.sounds[name].play()

    def setVolume(self,volume):
        # This function is used to set the volume of all the sounds
        for sound in self.sounds:
            self.sounds[sound].set_volume(volume)

    def playMusic(self):
        # This function is used to play the music
        self.sounds["music"].play(-1)
