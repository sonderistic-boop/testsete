#make game class, with a run method, and a main method
#game should be 810x770 -- deprecated
#game will have a stadium, a ball, and two teams
#game will have a run method, which will run the game 
import pygame as pg
import math
import sys


from gameClient.entities.pawn import Pawn
from gameClient.entities.ball import Ball
import gameClient.entities.stadium.stadiums as stadiums
from client.ui.screens import ScoreBoard
from shared.themeColours import *


class Game():
    # this class is used to manage the game on the client side
    def __init__(self,parentScreen,players,gameSettings,username):
        self.size = (1600,950)
        #declares the parent screen, which is the screen that the game surface will be drawn on
        self.parentScreen = parentScreen
        #declares which stadium the game will be played on
        # gets all information from the server to construct the game class
        self.stadium = gameSettings["stadium"]
        self.username = username
        self.gameState = "gameStart"
        #declares how long the game will last
        self.time = gameSettings["time"]
        #declares the maximum score the game will be played to
        self.maxScore = gameSettings["maxScore"]

        self.colours = {
            "team1" : "red",
            "team2" : "blue"
        }
        # texts that can be displayed on the screen when an action occurs
        self.texts = {
            "goalTeam1" : {
                "text" : "GOAL! RED TEAM SCORES!",
                "textColour" : themeColours["red"],
                "font" : pg.font.SysFont("Arial", 120,bold=pg.font.Font.bold),
                "position" : (self.size[0]//2,self.size[1]//2)
                },
            "goalTeam2" : {
                "text" : "GOAL! BLUE TEAM SCORES!",
                "textColour" : themeColours["blue"],
                "font" : pg.font.SysFont("Arial", 120,bold=pg.font.Font.bold),
                "position" : (self.size[0]//2,self.size[1]//2)
                },
            
            "gameEndTeam1" : {
                "text" : "RED TEAM WINS!",
                "textColour" : themeColours["red"],
                "font" : pg.font.SysFont("Arial", 120,bold=pg.font.Font.bold),
                "position" : (self.size[0]//2,self.size[1]//2)
                },
            "gameEndTeam2" : {
                "text" : "BLUE TEAM WINS!",
                "textColour" : themeColours["blue"],
                "font" : pg.font.SysFont("Arial", 120,bold=pg.font.Font.bold),
                "position" : (self.size[0]//2,self.size[1]//2)
                },
            "gameEndDraw" : {
                "text" : "DRAW!",
                "textColour" : (255,255,255),
                "font" : pg.font.SysFont("Arial", 120,bold=pg.font.Font.bold),
                "position" : (self.size[0]//2,self.size[1]//2)
                },
        }

        self.leftTeam = {}
        self.rightTeam = {}

        self.leftTeamScore = 0
        self.rightTeamScore = 0

        
        
        
        #load game surface, load players, load ball, load stadium
        

        self.screen = pg.Surface((self.size),pg.SRCALPHA)
        self.scoreBoard = ScoreBoard(self.parentScreen,(0,0),gameSettings)
        
        self.stadiumType = getattr(stadiums,gameSettings["stadium"])
        #put stadium in the middle of the screen
        self.stadium = self.stadiumType(self.screen,(100,100),[self.colours["team1"],self.colours["team2"]])
        self.stadiumSize = (self.screen.get_width()//2-((self.stadium.bounds["x2"]-self.stadium.bounds["x1"])//2),self.screen.get_height()//2-((self.stadium.bounds["y2"]-self.stadium.bounds["y1"])//2))
        self.stadium = None
        self.stadium = self.stadiumType(self.screen,self.stadiumSize,[self.colours["team1"],self.colours["team2"]])
        
        self.ball = Ball(self.screen,(self.stadium.bounds["middle"][0],self.stadium.bounds["middle"][1]),(30,30))
        
        #load players, and add them to the left and right team dictionaries. initial position will be the middle-left of the stadium for the left team, and the middle-right of the stadium for the right team
        for i in players["team1"]:
            self.leftTeam[i] = Pawn(i,self.colours["team1"],(False | (self.username == i)),self.screen,(400,400),(70.3,70.3))          
        
        for i in players["team2"]:
            self.rightTeam[i] = Pawn(i,self.colours["team2"],(False | (self.username == i)),self.screen,(400,400),(70.3,70.3))   

        
        
        
        #add sprite groups for ball, players, stadium parts

        #self.ballGroup = pg.sprite.GroupSingle(self.ball)


        


       

        
           


    def render(self):
        #draw the stadium, draw the ball, draw the players

        self.screen.fill((136, 179, 120))
        self.stadium.render()
        for i in self.leftTeam:
            self.leftTeam[i].render()
        for i in self.rightTeam:
            self.rightTeam[i].render()
        self.ball.render()
        match self.gameState:
            case "gameEndTeam1":
                self.renderTexts(self.texts["gameEndTeam1"])
            case "gameEndTeam2":
                self.renderTexts(self.texts["gameEndTeam2"])
            case "gameEndDraw":
                self.renderTexts(self.texts["gameEndDraw"])
            case "goalScoredTeam1":
                self.renderTexts(self.texts["goalTeam1"])
            case "goalScoredTeam2":
                self.renderTexts(self.texts["goalTeam2"])
            
        self.scoreBoard.render()


        
        
        self.parentScreen.blit(self.screen,(0,50))

    

    
    
    #main function, takes the receivingData as a parameter, and then renders the items based on this
    # another function as well, getData() which getData() returns the position of the isMe player.
    def getData(self,info):
        #get the position of the player, and the direction of movement, and the kick action from the info dictionary
        data = {}
        data["actions"] = {
            "direction" : (0,0),
            "kicked" : False
            }
        """
        for player in self.leftTeam:
            if player.isPlayer is True:
                position = player.position
                
        for player in self.rightTeam:
            if player.isPlayer is True:
                position = player.position
           """
        


        #create a dictionary, with keys position, and actions. actions will have keys "kicked" and "direction" with a normalised vector of the direction of movement
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            data["actions"]["direction"] = (data["actions"]["direction"][0], data["actions"]["direction"][1] - 1)
        
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            data["actions"]["direction"] = (data["actions"]["direction"][0], data["actions"]["direction"][1] + 1)

        if keys[pg.K_a] or keys[pg.K_LEFT]:
            data["actions"]["direction"] = (data["actions"]["direction"][0] - 1, data["actions"]["direction"][1])

        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            data["actions"]["direction"] = (data["actions"]["direction"][0] + 1, data["actions"]["direction"][1])

        if keys[pg.K_x] or keys[pg.K_SPACE]:
            data["actions"]["kicked"] = True
                        
      
        
        return data
                    
                    
                    
                          
                        
                        
                  
            
        
         
        
    def update(self,receivingData):
        # update the game state, and then update the positions of the players, and the ball with the data from the server

        #update positions of every object
        #update the ball

        #update the players
        self.gameState = receivingData["gameData"]["gameState"]
        for player in self.leftTeam:
            self.leftTeam[player].update(receivingData["gameData"]["players"]["team1"][player])

            
        for player in self.rightTeam:
            self.rightTeam[player].update(receivingData["gameData"]["players"]["team2"][player]) 
        self.ball.update(receivingData["gameData"]["ball"])
        self.time = receivingData["gameData"]["timeRemaining"]
        self.leftTeamScore = receivingData["gameData"]["score"]["team1"]
        self.rightTeamScore = receivingData["gameData"]["score"]["team2"]
        self.scoreBoard.updateButtons({"time" : self.time, "leftTeamScore" : self.leftTeamScore, "rightTeamScore" : self.rightTeamScore})
        
    def main(self,info,receivingData):
        #check for collisions, check for goals, check for time, check for score
        #update the ball, update the players
        #render the stadium, render the ball, render the players
        self.update(receivingData)

        self.render()
           
        
        
     
    def renderTexts(self,textItem):
        font = textItem["font"]
        text = font.render(textItem["text"], True, textItem["textColour"])
        self.screen.blit(text, (textItem["position"][0]-text.get_width()//2,textItem["position"][1]-text.get_height()//2))
     

    




        
        

        
    