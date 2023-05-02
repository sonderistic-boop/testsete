import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))


import pygame as pg
import subprocess
import configparser
import client.ui.screens as screens
from client.client import Client
from server.network import get_ip
from client.soundmanager import SoundManager

# design a pygame window, and set the window title as pyBall
pg.init()
pg.mixer.init()
pg.display.set_caption("pyBall")
screen = pg.display.set_mode((1600, 1000),pg.SRCALPHA)

# set up the clock
clock = pg.time.Clock()
soundManager = SoundManager()

# set up the main function for the game

# set up the main function for the game
# the main function will be used to run the game
# OBJECTIVE 1.1 - CREATING A SUITABLE ENVIRONMENT TO RUN THE CODE
def main():
    # set running as True
    # running indicates whether the game is running or not
    # if running is False, then the game will be closed
    # if running is True, then the game will be running
    running = True
    config = configparser.ConfigParser()
    
    config.read("../settings.ini")
    soundManager.setVolume(float(config["Settings"]["volume"])/100)
    soundManager.playMusic()


    # set the focus as Menu
    # focus indicates which screen the game is on
    # e.g if the focus is on Menu, then the game will be on the Menu screen
    focus = "Menu"
    newFocus= "Menu"
    # set the current screen as Menu
    current = screens.Menu(screen)

    
    # run the game
    while running:
        # set the FPS
        
        clock.tick(60)
        config.read("../settings.ini")
        # if the focus is changed, then change the current screen
        if focus != newFocus:
            
            match newFocus:
                # if the focus is on the game, then run the game
                case newFocus if newFocus[1] == "Game":
                    #if not others, then must be containing gamesettings as well as the checker from joinGame
                    soundManager.play("click")
                    focus = newFocus[1]
                    
                    # instantiates the client
                    # the client will be used to connect to the server
                    # the client will also be used to send and receive data from the server
                     
                    current = Client(screen,{"name" : newFocus[0]["username"],"team" : "neutral"},newFocus[0]["ip"],newFocus[0]["port"])
                    newFocus = newFocus[1]
                
                case newFocus if newFocus[1] == "Host":
                    soundManager.play("click")
                    # if the focus is on host, the start a subprocess for the server, and then host as a client to that server
                    
                    focus = newFocus[1]
                    server = subprocess.Popen([sys.executable, '../server/server.py', '--username', 'root'])

                    current = Client(screen,{"name" : newFocus[0]["username"],"team" : "neutral"},get_ip())
                    newFocus = newFocus[1]

                case newFocus if newFocus != "Exit" and isinstance(newFocus,str):
                    soundManager.play("click")
                    # if the focus is nothing else, then run the screen that is indicated by the focus
                    if focus == "Host":
                        try:
                            server.kill()
                        except:
                            pass
                    
                    focus = newFocus
                    current = getattr(screens,newFocus)(screen)
                case "Exit":
                    soundManager.play("leave")
                    
                    running = False
                    pg.quit()
                    sys.exit()
                
            

        info = {
            "mouse" : pg.mouse.get_pos(),
            "events" : pg.event.get(),
            "focus" : focus,
            "volume" : config["Settings"]["Volume"]
            }
        # set the maximum FPS
        
        soundManager.setVolume(float(config["Settings"]["volume"])/100)
        
        # get all the events
        for event in info["events"]:
            # if the event is to quit the game, then set running as False
            if event.type == pg.QUIT:
                running = False
                try:
                    server.kill()
                except:
                    pass

                pg.quit()
                sys.exit()
        
        output = current.main(info)
        if output is not None:
            newFocus = output



        pg.display.flip()
        
            
        
        
        
        # if the focus is on the menu, then run the menu
if __name__ == "__main__":
    main()

