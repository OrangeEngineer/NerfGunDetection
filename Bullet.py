import pygame
import math
from pygame.locals import *


class Bullet(object):
   
    def __init__(self, x ,y,TimeStamp):
        self.x = x
        self.y = y
        self.TimeStamp = TimeStamp
        self.image = pygame.image.load("res/Target/bullet_hole.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rectBullet=pygame.Rect(self.x,self.y,1,1)

    def render(self,surface):
        pos = (int(self.x),int(self.y))
        surface.blit(self.image,pos)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
		
    def update(self):
        self.rectBullet=pygame.Rect(self.x,self.y,1,1)
    
    def getrectBullet(self):
        return self.rectBullet
