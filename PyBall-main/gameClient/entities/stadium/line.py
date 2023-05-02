import pygame as pg


#always start line with the left most point
class Line(pg.sprite.Sprite):
    # OBJECTIVE 1.3 - CREATING CLASSES FOR ENTITIES IN THE GAME
    # line is a rectangle with a width of 8, and a height of the distance between the start and end points
    # it can collide with the ball and the player
    def __init__(self,surface,collidesWithPlayer,collidesWithBall,startPosition,endPosition,colour = (255,255,255)):
        super().__init__()
        self.surface = surface
        self.startPosition =  pg.math.Vector2(startPosition)
        self.endPosition =  pg.math.Vector2(endPosition) 
        self.position =  pg.math.Vector2(endPosition[0]-startPosition[0],endPosition[1]-startPosition[1])   
        self.colour = colour

        
        self.w= 8
        self.h = pg.math.Vector2.magnitude(pg.math.Vector2(endPosition[0]-startPosition[0],endPosition[1]-startPosition[1]))


        
        self.bounds = {
            "x1":self.startPosition[0],
            "y1" :self.startPosition[1],

            "x2":self.endPosition[0],
            "y2":self.endPosition[1],
        }
       
        self.size = (endPosition[0]-startPosition[0],endPosition[1]-startPosition[1])


        #PHYSICS
        self.staticValue = False
        # determines if the object is static or not
        self.collidesWith = {"player":collidesWithPlayer,"ball":collidesWithBall}
        # determines what the object collides with
        self.velocity = pg.math.Vector2(0,0)
        self.mass = 4
        self.inverseMass = 1/self.mass
        self.restitution = 0.99
        self.damping = 0



        self.image = pg.Surface((self.size[0],self.size[1]),pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (self.startPosition[0],self.startPosition[1]))
        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)


    def render(self):
        self.rect = self.image.get_rect(topleft = (self.startPosition[0],self.startPosition[1]))

        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)

        self.surface.blit(self.image,(self.startPosition[0],self.startPosition[1]))


    def renderGraphics(self):
        pg.draw.rect(self.image,self.colour,(0,0,self.size[0],self.size[1]))

    def updatePhysics(self):
        if self.Static:
            self.bounds = {
                "x1":self.startPosition[0],
                "y1" :self.startPosition[1],

                "x2":self.endPosition[0],
                "y2":self.endPosition[1],
            }
