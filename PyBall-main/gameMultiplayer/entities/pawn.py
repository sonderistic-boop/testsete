import pygame as pg
import pygame.gfxdraw as gfxdraw

#this is a dictionary of colours, the keys are the names of the colours, and the values are the hex codes of the colours
themeColours = {
    "red" : "#d14242",
    "green" : "#52d142",
    "blue" : "#426ad1",
    "yellow" : "#e1c16e",
    "cyan" : "#03b9b9",
    "magenta" : "#674ea7",
    "orange" : "#e69138"

}
#when assigning  team parameter, make  sure you do  so in all caps, also positon should be a tuple

#typical haxball player has 30 diameter, 50 for the outer, 

#ball is two thirds the size of the player
class Pawn(pg.sprite.Sprite):
    def __init__(self,name,team,isPlayer,surface,position,size):

        #inherits from sprite class, assigns all variables declared at initialisation
        super().__init__()
        self.name = name
        self.team = team
        self.isPlayer = isPlayer
        self.surface = surface
        self.position =  pg.math.Vector2(position)
        self.initialPosition = pg.math.Vector2(position).copy()
        self.kicking = False

        #diameter of the pawn
        self.size = size
        self.w,self.h = size
        self.radius =  (((self.w//2)**2 + (self.h//2)**2) ** 0.5)*0.64
        #colour  of the pawn
        self.colour = pg.Color(themeColours[team])


        #physics variables
        self.staticValue = True
        self.velocity = pg.math.Vector2(0,0)
        self.maxVelocity =5
        self.mass = 2
        self.inverseMass = 1/self.mass
        self.restitution = 0.5
        self.acceleration = 0.1
        #self.deltav = pg.math.Vector2(0,0)
        self.damping = 0.96
        

        #assigns the image and rect attributes to the sprite

        self.image = pg.Surface((self.w,self.h),pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (position[0],position[1]))
        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)


        

    #renders the pawn, and updates the mask, if the pawn is the player, a circle is drawn around the pawn
    def render(self):
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))

        self.renderGraphics()
        #self.mask = pg.mask.from_surface(self.image)
        
        

        
        
    #renders the graphics of the pawn, the outer circle and the inner circle
    def renderGraphics(self):
        
        pg.draw.circle(self.image,(255&self.kicking,255&self.kicking,255&self.kicking),(self.w//2,self.h//2),(0.64*(self.w//2)))
        pg.draw.circle(self.image,self.colour,(self.h//2,self.h//2),(0.55*(self.w//2)))


    def updatePhysics(self):
        if self.staticValue:
            
            self.constrainvelocity()
            #self.wallcollide()
            self.position  +=  self.velocity
            self.velocity *= self.damping

    def wallcollide(self):
        if self.position[0] < 0:
            self.position[0] = 0
            self.velocity[0] *= -1
        if self.position[0] > 1200 - self.w:
            self.position[0] = 1200 - self.w
            self.velocity[0] *= -1
        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] *= -1
        if self.position[1] > 600 - self.h:
            self.position[1] = 600 - self.h
            self.velocity[1] *= -1

    #constrains the velocity of the pawn to the max velocity
    def constrainvelocity(self):
        self.velocity.scale_to_length(5) if self.velocity.magnitude() > self.maxVelocity else None


    #resets the pawn to its initial position
    def reset(self):
        self.position = self.initialPosition.copy()
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))
        self.velocity = pg.math.Vector2(0,0)

    def getData(self):
        return {
            "name" : self.name,
            "team" : self.team,
            "position" : self.position,
            "kicking" : self.kicking,
            "size" : self.size
            }

    def update(self,receivingClientData):
        
        self.kicking = receivingClientData["actions"]["kicked"]
        deltav = pg.math.Vector2(receivingClientData["actions"]["direction"])
        
        if deltav.length() != 0:
            deltav = deltav.normalize() * self.acceleration
            
            self.velocity += deltav
        







