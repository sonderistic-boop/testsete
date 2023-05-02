import pygame as pg



themeColours = {
    "red" : "#d14242",
    "green" : "#52d142",
    "blue" : "#426ad1",
    "yellow" : "#e1c16e",
    "cyan" : "#03b9b9",
    "magenta" : "#674ea7",
    "orange" : "#e69138"

}


#typical ball  is 20 diameter

class Ball(pg.sprite.Sprite):
    def __init__(self,surface,position,size):

        #inherits from sprite class, assigns all variables declared at initialisation
        super().__init__()
        self.surface = surface
        self.position =  pg.math.Vector2(position)
        self.initialPosition =  pg.math.Vector2(position).copy()

        #diameter of the ball
        self.size = size
        self.w,self.h = size
        self.radius =  ((self.w//2)**2 + (self.h//2)**2) ** 0.5


        #physics variables
        self.staticValue = True
        self.velocity = pg.math.Vector2(0,0)
        self.mass = 1
        self.inverseMass = 1/self.mass
        self.restitution = 0.5
        self.damping = 0.99
        self.colour = (255,255,255)


        #assigns the image and rect attributes to the ball

        self.image = pg.Surface((self.w,self.h),pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))
        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)
        
    #renders the ball, and updates the mask
    def render(self):
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))

        self.renderGraphics()
        #self.mask = pg.mask.from_surface(self.image)

        

        
        
        
    #renders the graphics of the ball, the outer circle and the inner circle
    def renderGraphics(self):
        pg.draw.circle(self.image,(0,0,0),(self.w//2,self.h//2),((self.w//2)))
        pg.draw.circle(self.image,(self.colour),(self.h//2,self.h//2),(0.915*(self.w//2)))

    def updatePhysics(self):
        
        if self.staticValue:
            self.position  +=  self.velocity
            self.velocity *= self.damping


        

    def reset(self):
        self.position = self.initialPosition.copy()
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))
        self.velocity = pg.math.Vector2(0,0)
    
    def getData(self):
        return {
            "position" : self.position
            }
    


