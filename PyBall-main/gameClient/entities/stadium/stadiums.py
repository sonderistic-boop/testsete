#standard stadiums should be 24  pawns wide
import pygame as pg
from gameClient.entities.stadium.line import Line
from gameClient.entities.stadium.goal.goal import collidingGoal
from gameClient.entities.stadium.goal.goal import Goal

tiles = {
    "field" : pg.transform.scale((pg.image.load("../shared/assets/tiles/fieldtiles/fieldtile.png")),(300,300))
    
}
class Stadium():
    # This class is used to manage the stadium
    def __init__(self,screen,position,size):
        # This function is used to initialise the stadium


        self.screen = screen
        self.position = position
        self.size = size
        self.w,self.h = size
        self.pawns = []
        self.teams = []
        self.ball = None
        self.tile = None
        
        #Objects
        self.lines = {}
        self.collidingGoals = {}
        self.goals = {}
        self.arcs = {}
        # Bounds
        self.bounds = {
         "x1" : self.position[0],
         "x2" : self.position[0]+self.size[0],
         "y1" : self.position[1],
         "y2" : self.position[1]+self.size[1],
         "y3" : self.position[1]+(0.325*self.size[1]),
         "y4" : self.position[1]+self.size[1]-(0.325*self.size[1]),
         "middle" : (self.position[0]+(0.5*self.size[0]),self.position[1]+(0.5*self.size[1])),
         "goalheight" : 0.35*self.size[1],
         "xleftmiddle" : self.position[0]+(0.25*self.size[0]),
         "xrightmiddle" : self.position[0]+(0.75*self.size[0])
        }




        

        self.image = pg.Surface((self.w,self.h),pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (position[0],position[1]))
        self.mask = pg.mask.from_surface(self.image)

    def render(self):
        self.renderGraphics()
        
    
    def renderGraphics(self):
        self.image.fill((0,0,0,0))

        self.stamping()

        for line in self.lines:
            self.lines[line].render()

        for goal in self.goals:
            self.goals[goal].render()

        for collidingGoal in self.collidingGoals:
            self.collidingGoals[collidingGoal].render()
         
        for arc in self.arcs:
            self.arcs[arc].render()
            
            
            
    def stamping(self):
        # This function is used to stamp the tiles
        for i in range(self.bounds["x1"],self.bounds["x2"],300):
            for j in range(self.bounds["y1"],self.bounds["y2"],300):
                self.screen.blit(self.tile,(i,j))






class smallStadium(Stadium):
    # This class is used to construct a small stadium
    # it is 24 pawns wide and inherits from the stadium class
    

    def __init__(self,screen,position,teams):
        super().__init__(screen,position,(1200,600))
        
        self.teams = teams
        self.tile = tiles["field"]

        

        #goal should be 210 down from top and 210 up from bottom
        self.lines = {
            "top" : Line(self.screen,False,True,(self.bounds["x1"]-4,self.bounds["y1"]-4),(self.bounds["x2"]+4,self.bounds["y1"]+4)),
            "bottom" : Line(self.screen,False,True,(self.bounds["x1"]-4,self.bounds["y2"]-4),(self.bounds["x2"]+4,self.bounds["y2"]+4)),


            "left1" : Line(self.screen,False,True,(self.bounds["x1"]-4,self.bounds["y1"]),(self.bounds["x1"]+4,self.bounds["y3"])),
            "left2" : Line(self.screen,False,True,(self.bounds["x1"]-4,self.bounds["y4"]),(self.bounds["x1"]+4,self.bounds["y2"])),
            "right1" : Line(self.screen,False,True,(self.bounds["x2"]-4,self.bounds["y1"]),(self.bounds["x2"]+4,self.bounds["y3"])),
            "right2" : Line(self.screen,False,True,(self.bounds["x2"]-4,self.bounds["y4"]),(self.bounds["x2"]+4,self.bounds["y2"])),


            "middle" : Line(self.screen,False,False,(self.bounds["middle"][0]-4,self.bounds["y1"]),(self.bounds["middle"][0]+4,self.bounds["y2"])),
        }
        

        print(self.lines["top"].startPosition)
        print(self.lines["top"].bounds["y1"])
        # the goals that can be collided with in the stadium
        self.collidingGoals = {
    
            "left": collidingGoal(self.screen,(self.bounds["x1"]-79,self.bounds["y3"]),self.bounds["goalheight"],self.teams[0],"left"),
            "right": collidingGoal(self.screen,(self.bounds["x2"]-15,self.bounds["y3"]),self.bounds["goalheight"],self.teams[1],"right")
        }
        # This is the goals for the stadium
        self.goals = {
            "left": Goal(self.screen,(self.bounds["x1"]-2,self.bounds["y3"]),(self.bounds["x1"]+2,self.bounds["y4"]),self.teams[0]),
            "right": Goal(self.screen,(self.bounds["x2"]-2,self.bounds["y3"]),(self.bounds["x2"]+2,self.bounds["y4"]),self.teams[1])
        }


