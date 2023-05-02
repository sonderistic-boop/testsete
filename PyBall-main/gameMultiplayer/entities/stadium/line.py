import pygame as pg


#always start line with the left most point
class Line(pg.sprite.Sprite):
    def __init__(self,surface,collidesWithPlayer,collidesWithBall,startPosition,endPosition,colour = (255,255,255)):
        super().__init__()
        self.surface = surface
        self.startPosition =  pg.math.Vector2(startPosition)
        self.endPosition =  pg.math.Vector2(endPosition) 
        self.position =  pg.math.Vector2(endPosition[0]-startPosition[0],endPosition[1]-startPosition[1])   
        self.colour = colour

        
        self.w= pg.math.Vector2.magnitude(pg.math.Vector2(endPosition[0]-startPosition[0],endPosition[1]-startPosition[1]))
        self.h = pg.math.Vector2.magnitude(pg.math.Vector2(endPosition[0]-startPosition[0],endPosition[1]-startPosition[1]))


        
        self.bounds = {
            "x1":self.startPosition[0],
            "y1" :self.startPosition[1],

            "x2":self.endPosition[0],
            "y2":self.endPosition[1],
        }

        self.vertices = [
            (self.startPosition[0],self.startPosition[1]),
            (self.endPosition[0],self.startPosition[1]),
            (self.endPosition[0],self.endPosition[1]),
            (self.startPosition[0],self.endPosition[1])
        ]

        self.size = (endPosition[0]-startPosition[0],endPosition[1]-startPosition[1])
        

        #PHYICS
        self.staticValue = False
        self.collidesWith = {"player":collidesWithPlayer,"ball":collidesWithBall}
        self.velocity = pg.math.Vector2(0,0)
        self.mass = 1
        self.inverseMass = 1/self.mass
        self.restitution = 0.4
        self.damping = 0



        self.image = pg.Surface((self.size[0],self.size[1]),pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (self.startPosition[0],self.startPosition[1]))
        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)


    def render(self):
        self.rect = self.image.get_rect(topleft = (self.startPosition[0],self.startPosition[1]))

        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)

        


    def renderGraphics(self):
        self.image.fill(self.colour)

    def updatePhysics(self):
        if self.staticValue:
            self.bounds = {
                "x1":self.startPosition[0],
                "y1" :self.startPosition[1],

                "x2":self.endPosition[0],
                "y2":self.endPosition[1],
            }
