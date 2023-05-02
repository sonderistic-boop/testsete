import pygame as pg
import pygame.gfxdraw as gfxdraw


class Arc(pg.sprite.Sprite):
    def __init__(self,surface,position,radius,angle,colour = (0,0,0)):
        super().__init__()
        self.surface = surface
        self.position =  pg.math.Vector2(position)
        self.radius = radius
        self.size = pg.math.Vector2(radius*3,radius*3)
        #start and end angle at angle[0] and angle[1] respectively
        self.angle = pg.math.Vector2(angle)

        self.colour = colour

        self.image = pg.Surface((self.size[0],self.size[1]),pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))
        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)
    
    def render(self):
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))
        self.renderGraphics()
        self.mask = pg.mask.from_surface(self.image)
        

    
    def renderGraphics(self):
        pg.draw.arc(self.image,self.colour,self.rect,0,1,8)


        
