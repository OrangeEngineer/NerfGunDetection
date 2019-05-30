import pygame
import math
from pygame.locals import *
import random

class Target(object):
   
    def __init__(self,health,height=500,width=500):
        # self.x = random.randint(0,800)
        # self.y = random.randint(0,600)
        self.x = 1920/2-250
        self.y = 1080/2-250
        # self.mouse_x = mousex
        # self.mouse_y = mousey
        self.width= width
        self.height= height
        self.move_x = 2
        self.move_y = 2
        self.TargetHealth = health
        self.image = pygame.image.load("C:/Users/Nuttaphon/Documents/NerfGun/Gaming/res/Target/Target.PNG")
        self.image = pygame.transform.scale(self.image, (500, 500))
        self.original=self.image
        # self.image = pygame.transform.rotate(self.image,30)
        print(str(self.x)+ " " +str(self.y)+ " " +str(self.width) + " " +str(self.height))
        self.rectTarget = pygame.Rect(self.x,self.y,self.width,self.height)

    def render(self,surface):
        pos = (int(self.x),int(self.y))
        surface.blit(self.image,pos)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getrectTarget(self):
        return self.rectTarget

    def getHealth(self):
        return self.TargetHealth

    def Die(self):
        self.TargetHealth -= 1

    def update(self):
        # self.mouse_x = x
        # self.mouse_y = y
        # self.degrees =  getAngle(self.x,self.y,self.mouse_x,self.mouse_y)
        # self.y += self.move_y
        # if(self.y <= 0 or self.y+self.height >= 1080):
        #     self.move_y = -self.move_y
        # self.x += self.move_x
        # if(self.x <= 0 or self.x+self.width >= 1920):
        #     self.move_x = -self.move_x
        self.rectZombie = pygame.Rect(self.x,self.y,self.width,self.height)
    