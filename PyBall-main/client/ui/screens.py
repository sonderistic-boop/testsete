import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import configparser
import pygame as pg
from client.ui.button import *
from shared.themeColours import *
# set up a menu class, with a themeColours green background, and a join server, host server, settings, credits, and exit button

# OBJECTIVE 4.1 - CREATING A MENU SYSTEM WHICH ALLOWS THE USER TO NAVIGATE THROUGH THE GAME
# OBJECTIVE 4.2 - CREATING CLASS INHERITANCE TO ALLOW FOR EASIER CODE MAINTENANCE
class Menu:
    def __init__(self,surface):
        
        # set up the surface
        self.surface = surface
        self.background = pg.transform.scale((pg.image.load("../shared/assets/background/background.png")),(120,120))
        self.logo = pg.image.load("../shared/assets/background/pyballlogo.png")
        self.backgroundX = []
        
       

        # set up the background
        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)
        
        
        
        # set up the buttons
        self.buttons = {}
        self.buttons["Join Game"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),300),(200,50),"Join Game","JoinGame")
        self.buttons["Host Game"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),400),(200,50),"Host Game","HostGame")
        self.buttons["Settings"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),500),(200,50),"Settings","Settings")
        self.buttons["Credits"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),600),(200,50),"Credits","Credits")             
        self.buttons["Exit"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),700),(200,50),"Exit","Exit")
    
    
    
    
        
    # event handler for the menu
    def eventHandler(self,info):
        for button in self.buttons:
            checker = self.buttons[button].eventHandler(info)
            if checker != None:
                return checker


    
    # render the background
    def renderSlidingBackground(self):
        for i in range(0,len(self.backgroundX)):
            if self.backgroundX[i] <= -120:
                self.backgroundX[i] = self.surface.get_width() + 120
            for j in range(0,(self.surface.get_height()+120),120):
                
                self.surface.blit(self.background,(self.backgroundX[i],j))
                
            self.backgroundX[i] -= 1

    # render the logo
      
    def renderLogo(self):
        self.surface.blit(self.logo,(((self.surface.get_width()/2)-(self.logo.get_width()/2)),100))
        
    
    def renderButtons(self):
        for button in self.buttons:
            self.buttons[button].render()
        
        
    
    def render(self):
       self.renderSlidingBackground()
       self.renderLogo()
       self.renderButtons()


    def main(self,events):
        checker = self.eventHandler(events)
        if checker != None:
            return checker
        self.render()



class JoinGame(Menu):
    def __init__(self,surface):
        super().__init__(surface)
        self.surface = surface
        self.backgroundX = []
        
        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)
        
        self.buttons = {}
        self.buttons["Back"] = MenuButton(self.surface,(((150),150)),(200,50),"Back","Menu")
        self.buttons["Join"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),700),(200,50),"Join","Game")
        self.buttons["Username"] = InputButton(self.surface,(((self.surface.get_width()/2)-100),300),(200,50))
        self.buttons["IP"] = InputButton(self.surface,(((self.surface.get_width()/2)-100),400),(200,50))
        self.buttons["Port"] = InputButton(self.surface,(((self.surface.get_width()/2)-100),500),(200,50))


        self.texts = {
            "IP" : {
                    "text":"IP:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.buttons["IP"].position[0]-100,400),
                    "textSize" : 30
                    },

            "Port" : {
                    "text":"Port:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.buttons["Port"].position[0]-100,500),
                    "textSize" : 30
                    },
            
            "Username" : {
                    "text":"Username:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.buttons["Username"].position[0]-200,300),
                    "textSize" : 30
                    }

            }
        

    def renderTexts(self):
        for text in self.texts:
            font = pg.font.SysFont(self.texts[text]["font"],self.texts[text]["textSize"])
            rendertext = font.render(self.texts[text]["text"],1,self.texts[text]["textColour"])
            self.surface.blit(rendertext,(self.texts[text]["position"]))

    
    
        
    def eventHandler(self,info):
        # if a button is pressed, return the button's name, which returns the name of the next screen
        for button in self.buttons:
            checker = self.buttons[button].eventHandler(info)
            if checker != None:
                return checker
            


    def renderSlidingBackground(self):
        for i in range(0,len(self.backgroundX)):
            if self.backgroundX[i] <= -120:
                self.backgroundX[i] = self.surface.get_width() + 120
            for j in range(0,(self.surface.get_height()+120),120):
                
                self.surface.blit(self.background,(self.backgroundX[i],j))
                
            self.backgroundX[i] -= 1


      


    def renderButtons(self):
        for button in self.buttons:
            self.buttons[button].render()
    
    def render(self):
        self.renderSlidingBackground()
        s = pg.Surface((self.surface.get_width()-200,self.surface.get_height()-200))
        s.set_alpha(220)                
        s.fill((0,0,0))
        self.surface.blit(s,(100,100))
        self.renderTexts()

        self.renderButtons()

    def main(self,events):
        checker = self.eventHandler(events)
        if checker == "Game":
            clientSettings = {
                "username" : self.buttons["Username"].text,
                "ip" : self.buttons["IP"].text,
                "port" : self.buttons["Port"].text
            }
            return clientSettings, checker
        elif checker != None:
            return checker
        self.render()
    













# CREATES THE GAME LOBBY
class GameLobby(Menu):
    def __init__(self,surface,clientSettings,ip):
        super().__init__(surface)
        self.surface = surface
        self.backgroundX = []
        self.clientSettings = clientSettings
        self.ip = ip

        
        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)
        
        self.buttons = {}
        self.buttons["Start"] = MenuButton(self.surface,((self.surface.get_width()-350),800),(200,50),"Start","startGame")
        self.buttons["Leave"] = MenuButton(self.surface,((150,150)),(200,50),"Leave","Exit")
        self.lists = {}
        self.lists["team1"] = ListButton(self.surface,((400,175)),(200,500),[])
        self.lists["team2"] = ListButton(self.surface,(((self.surface.get_width()-600),175)),(200,500),[])
        self.lists["neutral"] = ListButton(self.surface,(((self.surface.get_width()/2)-100),175),(200,500),[self.clientSettings["name"]])

        self.infoButtons = {}
        self.infoButtons["ip"] = InfoButton(self.surface,(400,800),(150,25),str(self.ip))
        self.datatoSend = {}


        self.texts = {
            "team1" : {
                    "text":"Red Team:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (400,125),
                    "textSize" : 30
                    },
            "team2" : {
                    "text":"Blue Team:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()-600,125),
                    "textSize" : 30
                    },
            "neutral" : {
                    "text":"Neutral:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : ((self.surface.get_width()/2)-100,125),
                    "textSize" : 30
            },
            "ip" : {
                    "text":"IP:",
                    "textColour": (255,255,255),
                    "font" : "Arial",
                    "position" : (375,800),
                    "textSize" : 20
            
            }
        }   

    def renderSlidingBackground(self):

        for i in range(0,len(self.backgroundX)):
            if self.backgroundX[i] <= -120:
                self.backgroundX[i] = self.surface.get_width() + 120
            for j in range(0,(self.surface.get_height()+120),120):
                
                self.surface.blit(self.background,(self.backgroundX[i],j))
                
            self.backgroundX[i] -= 1
    
    def eventHandler(self,info):
        for button in self.buttons:
            checker = self.buttons[button].eventHandler(info)
            if checker == "startGame":
                self.datatoSend["transferMode"] = "game"
            elif checker == "Exit":
                return checker
        for listButton in self.lists:
            checker = self.lists[listButton].eventHandler(info,self.lists)
            if checker != None:
                
                return checker
        
            

    

    def renderTexts(self):
        for text in self.texts:
            font = pg.font.SysFont(self.texts[text]["font"],self.texts[text]["textSize"])
            rendertext = font.render(self.texts[text]["text"],1,self.texts[text]["textColour"])
            self.surface.blit(rendertext,(self.texts[text]["position"]))

    def renderButtons(self):
        for button in self.buttons:
            self.buttons[button].render()
        for listButton in self.lists:
            self.lists[listButton].render()
        for infoButton in self.infoButtons:
            self.infoButtons[infoButton].render()


    def render(self):
        self.renderSlidingBackground()
        
        s = pg.Surface((self.surface.get_width()-200,self.surface.get_height()-200))
        s.set_alpha(220)                
        s.fill((0,0,0))
        self.surface.blit(s,(100,100))
        self.renderTexts()

        self.renderButtons()
    
    def updateLists(self,newLists):
        for listButton in self.lists:
            self.lists[listButton].updateItems(newLists[listButton])

    def getData(self):
        sendingData = {}
        # gets the team of the player who matches the username in the client settings
        for team in self.lists:
            for player in self.lists[team].list:
                if player == self.clientSettings["name"]:
                    sendingData["team"] = team
        
        if self.datatoSend != {}:
            for data in self.datatoSend:
                sendingData[data] = self.datatoSend[data]
            self.datatoSend = {}
        return sendingData

        

    def main(self,info,receivingData):
        #receivingData will contain a "players" key which contains a "team1", "team2" and "neutral" key
        
        self.updateLists(receivingData["players"])
        checker = self.eventHandler(info)
        if checker == "Exit":
            return "Exit"
        self.render()
        




class HostGame(Menu):
    def __init__(self,surface):
        super().__init__(surface)
        self.surface = surface
        self.backgroundX = []
        
        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)
        
        self.buttons = {}
        self.buttons["Back"] = MenuButton(self.surface,(((150),150)),(200,50),"Back","Menu")
        self.buttons["Host"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),700),(200,50),"Host","Host")
        self.buttons["Username"] = InputButton(self.surface,(((self.surface.get_width()/2)-100),300),(200,50))
        


        self.texts = {
            
            "Username" : {
                    "text":"Username:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.buttons["Username"].position[0]-200,300),
                    "textSize" : 30
                    }

            }
        

    def renderTexts(self):
        for text in self.texts:
            font = pg.font.SysFont(self.texts[text]["font"],self.texts[text]["textSize"])
            rendertext = font.render(self.texts[text]["text"],1,self.texts[text]["textColour"])
            self.surface.blit(rendertext,(self.texts[text]["position"]))

    
    
        
    def eventHandler(self,info):
        for button in self.buttons:
            checker = self.buttons[button].eventHandler(info)
            if checker != None:
                return checker
            


    def renderSlidingBackground(self):
        for i in range(0,len(self.backgroundX)):
            if self.backgroundX[i] <= -120:
                self.backgroundX[i] = self.surface.get_width() + 120
            for j in range(0,(self.surface.get_height()+120),120):
                
                self.surface.blit(self.background,(self.backgroundX[i],j))
                
            self.backgroundX[i] -= 1



    def renderButtons(self):
        for button in self.buttons:
            self.buttons[button].render()
    
    def render(self):
        self.renderSlidingBackground()
        s = pg.Surface((self.surface.get_width()-200,self.surface.get_height()-200))
        s.set_alpha(220)                
        s.fill((0,0,0))
        self.surface.blit(s,(100,100))
        self.renderTexts()

        self.renderButtons()

    def main(self,events):
        checker = self.eventHandler(events)
        if checker == "Host":
            if self.buttons["Username"].text == "":
                self.buttons["Username"].text = "Player"
            clientSettings = {
                "username" : self.buttons["Username"].text,
            }
            return clientSettings, checker
        elif checker != None:
            return checker
        self.render()







class Disconnect(Menu):
    def __init__(self,surface):
        super().__init__(surface)
        self.surface = surface
        self.backgroundX = []
        
        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)
        
        self.buttons = {}
        
        self.buttons["Menu"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),700),(200,50),"Menu","Menu")
        


        self.texts = {
            
            "Disconnect" : {
                    "text":"You were disconnected. Your name may have been taken,",
                    "textColour":(255,20,20),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()/2-200,self.surface.get_height()/2-30),
                    "textSize" : 20
                    },
            "Disconnect2" : {
                    "text":"the IP may be incorrect, an error has occured on the hosts end,",
                    "textColour":(255,20,20),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()/2-200,self.surface.get_height()/2),
                    "textSize" : 20
                    },
            "Disconnect3" : {
                    "text":"or the host has left. Please try again later",
                    "textColour":(255,20,20),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()/2-200,self.surface.get_height()/2+30),
                    "textSize" : 20
            }


        }
        

    def renderTexts(self):
        for text in self.texts:
            font = pg.font.SysFont(self.texts[text]["font"],self.texts[text]["textSize"])
            rendertext = font.render(self.texts[text]["text"],1,self.texts[text]["textColour"])
            self.surface.blit(rendertext,(self.texts[text]["position"]))

    
    
        
    def eventHandler(self,info):
        for button in self.buttons:
            checker = self.buttons[button].eventHandler(info)
            if checker != None:
                return checker
            


    def renderSlidingBackground(self):
        for i in range(0,len(self.backgroundX)):
            if self.backgroundX[i] <= -120:
                self.backgroundX[i] = self.surface.get_width() + 120
            for j in range(0,(self.surface.get_height()+120),120):
                
                self.surface.blit(self.background,(self.backgroundX[i],j))
                
            self.backgroundX[i] -= 1



    def renderButtons(self):
        for button in self.buttons:
            self.buttons[button].render()
    
    def render(self):
        self.renderSlidingBackground()
        s = pg.Surface((self.surface.get_width()-900,self.surface.get_height()-900))
        s.set_alpha(220)                
        s.fill((150,150,150))
        self.surface.blit(s,(self.surface.get_width()/2-s.get_width()/2,self.surface.get_height()/2-s.get_height()/2))
        self.renderTexts()

        self.renderButtons()

    def main(self,events):
        checker = self.eventHandler(events)
        if checker != None:
            return checker
        self.render()
    

class ScoreBoard:
    # This class is used to display the score board, as a UI element
    def __init__(self,surface,position,gameSettings):
        self.surface = surface
        self.screen = pg.surface.Surface((self.surface.get_width(),50))
        
        self.infoButtons = {}
        self.infoButtons["Time"] = InfoButton(self.screen,((self.screen.get_width()-120),10),(80,30),gameSettings["time"])
        self.infoButtons["leftTeamScore"] = InfoButton(self.screen,(85,10),(30,30),"0")
        self.infoButtons["rightTeamScore"] = InfoButton(self.screen,(115,10),(30,30),"0")

        for i in self.infoButtons:
            self.infoButtons[i].colour = (0,0,0)


        self.texts = {
            
            "Time" : {
                    "text":"Time:",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()-200,10),
                    "textSize" : 30
                    },
            "Dash1" : {
                    "text":"-",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (55,10),
                    "textSize" : 30
                },
            "Dash2" : {
                    "text":"-",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (150,10),
                    "textSize" : 30
                }
            }

        self.position = position

    def renderTexts(self):

        for text in self.texts:
            font = pg.font.SysFont(self.texts[text]["font"],self.texts[text]["textSize"])
            rendertext = font.render(self.texts[text]["text"],1,self.texts[text]["textColour"])
            self.screen.blit(rendertext,(self.texts[text]["position"]))
    
    def render(self):
        self.screen.fill((0,0,0))
        self.renderGraphics()
        self.renderTexts()
        self.renderButtons()
        self.surface.blit(self.screen,self.position)
    
    def renderButtons(self):
        for button in self.infoButtons:
            self.infoButtons[button].render()

    def updateButtons(self,gameInfo):
        self.infoButtons["Time"].info = gameInfo["time"]
        self.infoButtons["leftTeamScore"].info = gameInfo["leftTeamScore"]
        self.infoButtons["rightTeamScore"].info = gameInfo["rightTeamScore"]

    def renderGraphics(self):
        pg.draw.rect(self.screen,themeColours["red"],(10,10,30,30))
        pg.draw.rect(self.screen,themeColours["blue"],(180,10,30,30))


class Settings(Menu):
    def __init__(self,surface):
        super().__init__(surface)
        self.surface = surface
        self.backgroundX = []
        # sets up the config file to be read
        self.config = configparser.ConfigParser()
    
        self.config.read("../settings.ini")
        self.error = False
        
        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)
        
        self.buttons = {}
        
        self.buttons["Back"] = MenuButton(self.surface,((150,150)),(200,50),"Back","Menu")
        self.buttons["Apply"] = MenuButton(self.surface,(((self.surface.get_width()/2)-100),700),(200,50),"Apply","Apply")
        self.buttons["Volume"] = InputButton(self.surface,(((self.surface.get_width()/2)-50),((self.surface.get_height()/2)-100)),(100,50))
        self.buttons["Volume"].text = self.config["Settings"]["Volume"]
        


        self.texts = {
            

            "Volume" : {
                    "text":"Volume: ",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()/2-150,self.surface.get_height()/2-100),
                    "textSize" : 30
                },
            "Error" : {
                    "text":"Invalid Input, please try again",
                    "textColour":(255,20,20),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()/2-100,self.surface.get_height()/2+75),
                    "textSize" : 20
                    }

            }
        

    def renderTexts(self):
        for text in self.texts:
            if text == "Error":
                if self.error == True:
                  pass
                else:
                  continue
            font = pg.font.SysFont(self.texts[text]["font"],self.texts[text]["textSize"])
            rendertext = font.render(self.texts[text]["text"],1,self.texts[text]["textColour"])
            self.surface.blit(rendertext,(self.texts[text]["position"]))
            
                

    
    
        
    def eventHandler(self,info):
        for button in self.buttons:
            checker = self.buttons[button].eventHandler(info)
            if checker != None:
                return checker
            


    def renderSlidingBackground(self):
        for i in range(0,len(self.backgroundX)):
            if self.backgroundX[i] <= -120:
                self.backgroundX[i] = self.surface.get_width() + 120
            for j in range(0,(self.surface.get_height()+120),120):
                
                self.surface.blit(self.background,(self.backgroundX[i],j))
                
            self.backgroundX[i] -= 1



    def renderButtons(self):
        for button in self.buttons:
            self.buttons[button].render()
    
    def render(self):
        self.renderSlidingBackground()
        s = pg.Surface((self.surface.get_width()-200,self.surface.get_height()-200))
        s.set_alpha(220)                
        s.fill((0,0,0))
        self.surface.blit(s,(100,100))
        self.renderTexts()

        self.renderButtons()

    def main(self,info):
        checker = self.eventHandler(info)
        if checker != None:
            if checker == "Apply":
                # checks if the input is a number and if it is between 0 and 100
                if self.buttons["Volume"].text.isnumeric():
                    if int(self.buttons["Volume"].text) > 100 or int(self.buttons["Volume"].text) < 0:
                        self.error = True
                    else:
                        self.error = False
                        self.config["Settings"]["Volume"] = self.buttons["Volume"].text
                        with open("settings.ini","w") as f:
                            self.config.write(f)
                        return "Menu"
                else:
                    self.error = True
            else:
                return checker
        self.render()


class Credits(Menu):
    # this is the credits menu
    def __init__(self,surface):
        super().__init__(surface)
        self.surface = surface
        self.backgroundX = []
        self.buttons = {}
        self.buttons["Back"] = MenuButton(self.surface,((150,150)),(200,50),"Back","Menu")

        for i in range(-120,self.surface.get_width()+120,120):
            self.backgroundX.append(i)

        self.texts = {
            "Name1" : {
                    "text":"By Yusuf Tagari 13.4",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()/2-150,150),
                    "textSize" : 30
                },
            "Name2" : {
                    "text":"Wanstead High School",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()/2-150,250),
                    "textSize" : 30
                },
            "Name4" : {
                    "text":"Built with Python and Pygame",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()/2-150,450),
                    "textSize" : 30
                },
            "Name5" : {
                    "text":"For the A Level Computer Science Coursework",
                    "textColour":(255,255,255),
                    "font" : "Arial",
                    "position" : (self.surface.get_width()/2-150,550),
                    "textSize" : 30
                }
        }

    def renderTexts(self):
        for text in self.texts:
            font = pg.font.SysFont(self.texts[text]["font"],self.texts[text]["textSize"])
            rendertext = font.render(self.texts[text]["text"],1,self.texts[text]["textColour"])
            self.surface.blit(rendertext,(self.texts[text]["position"]))
    
    def renderButtons(self):
        super().renderButtons()
    
    def renderSlidingBackground(self):
        return super().renderSlidingBackground()
    
    def render(self):
        self.renderSlidingBackground()
        s = pg.Surface((self.surface.get_width()-200,self.surface.get_height()-200))
        s.set_alpha(220)                
        s.fill((0,0,0))
        self.surface.blit(s,(100,100))
        self.renderTexts()
        self.renderButtons()
    
    def eventHandler(self,info):
        return super().eventHandler(info)
    
    def main(self,info):
        checker = self.eventHandler(info)
        if checker != None:
            return checker
        self.render()

