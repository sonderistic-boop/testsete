#creates a class for the goal
import pygame as pg
import pygame.gfxdraw as gfxdraw
from gameMultiplayer.entities.ball import Ball

themeColours = {
    "red" : "#d14242",
    "green" : "#52d142",
    "blue" : "#426ad1",
    "yellow" : "#e1c16e",
    "cyan" : "#03b9b9",
    "magenta" : "#674ea7",
    "orange" : "#e69138"

}

#94 pixels waide
class collidingGoal(pg.sprite.Sprite):
    def __init__(self,surface,position,height,team,orientation):
        super().__init__()
        self.surface = surface
        self.position =  pg.math.Vector2(position)
        self.size = pg.math.Vector2(94,height)
        self.team = team
        self.colour = (pg.Color(themeColours[team]))

        self.orientation = {
         "left" : True if orientation == "left" else False,
         "right" : True if orientation == "right" else False
         }


        #physics variables
        self.static = True
        self.mass = 1
        self.inverseMass = 1/self.mass
        self.restitution = 0.5
        self.damping = 0
        # creates the circles for the goal, if the ball hits the circles, it will bounce off
        self.circles = {
            "top" : Ball(self.surface,(self.position[0] + self.size[0]*self.orientation["left"],self.position[1]),(30,30)),
            "bottom" : Ball(self.surface,(self.position[0] + self.size[0]* self.orientation["left"],self.position[1]-30),(30,30))
        }
        for i in self.circles:
            # makes the circles static, so they don't move
            self.circles[i].staticValue = False
            self.circles[i].colour = self.colour
            self.circles[i].mass = 10000000


        self.image = pg.Surface((self.size[0],self.size[1]),pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))
        self.renderGraphics()
        self.image = pg.transform.flip(self.image,self.orientation["left"],False)
        self.mask = pg.mask.from_surface(self.image)
    

    def render(self):
        # renders the goal
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))
        self.image.fill((0,0,0,0))
        
        self.renderGraphics()
        self.renderCircles()
        # flips the goal if it is on the right side
        self.image = pg.transform.flip(self.image,self.orientation["left"],False)
        
        
        

    def renderGraphics(self):
        
     
        pg.draw.line(self.image,(0,0,0),(19,15),(self.size[0]-8,15),8)
        pg.draw.line(self.image,(0,0,0),(self.size[0]-4,12),(self.size[0]-4,self.size[1]-11),8)
        pg.draw.line(self.image,(0,0,0),(19,self.size[1]-15),(self.size[0]-8,self.size[1]-15),8)

        pg.draw.circle(self.image,(0,0,0),(15,15),((15)))
        pg.draw.circle(self.image,(self.colour),(15,15),(0.915*15))
        pg.draw.circle(self.image,(0,0,0),(15,self.size[1]-15),((15)))
        pg.draw.circle(self.image,(self.colour),(15,self.size[1]-15),(0.915*15))
    
    def renderCircles(self):
        for i in self.circles:
            self.circles[i].render()



    

class Goal(pg.sprite.Sprite):
    def __init__(self,surface,startPosition,endPosition,team):
        super().__init__()
        self.surface = surface
        self.startPosition =  pg.math.Vector2(startPosition)
        self.endPosition =  pg.math.Vector2(endPosition)        
        self.team = team


        self.colour = (pg.Color(themeColours[team]))
        self.size = (endPosition[0]-startPosition[0],endPosition[1]-startPosition[1])
    



        #PHYICS VARIABLES


        self.image = pg.Surface((self.size[0],self.size[1]),pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (self.startPosition[0],self.startPosition[1]))
        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)


    def render(self):
        self.rect = self.image.get_rect(topleft = (self.startPosition[0],self.startPosition[1]))

        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)
        
        

    def renderGraphics(self):
        
        pg.draw.rect(self.image,self.colour,(0,0,self.size[0],self.size[1]))

