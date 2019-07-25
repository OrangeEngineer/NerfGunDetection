import pygame
import sys
from pygame.locals import *
from pygame import *
from tracker.centroidtracker import CentroidTracker
from tracker.trackableobject import TrackableObject
from tracker.perspectivematching import PerspectiveMatching
from imutils.video import WebcamVideoStream
import random
import math
import gamelib
import time
import numpy as np
import cv2 as cv
import imutils

from Target import *
from Bullet import *

vertical_cap = WebcamVideoStream(src=2).start()

horizontal_cap = WebcamVideoStream(src=3).start()

ix,iy = -1,-1

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
RED = ( 120, 0, 0)
BLUE = (30,144,255)

VerticalPoints = []
HorizontalPoints = []

fgbg = cv.createBackgroundSubtractorMOG2()
kernel_dil = np.ones((20,20),np.uint8)
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))

def GetPointsVertical(event,x,y,flags,param):
    if (event == cv.EVENT_LBUTTONDBLCLK):
        # if len(VerticalPoints)<= 2 :
        VerticalPoints.append(x)
        print(str(x) +" " +str(y))

def GetPointsHorizontal(event,x,y,flags,param):
    if (event == cv.EVENT_LBUTTONDBLCLK):
        # if len(HorizontalPoints)<= 2 :
        HorizontalPoints.append(x)
        print(str(x) +" " +str(y))

def FindCentroid(rect):
    return (((rect[0]*rect[2])/2),((rect[1]*rect[3])/2))


class AlienShooting(gamelib.NerfGunGame):
    WHITE = pygame.Color('white')
    BLACK = pygame.Color('black')
    def __init__(self):
        super(AlienShooting, self).__init__('Protect the world from aliens!!', WHITE)
        self.setTimeIntervalTarget = 0
        self.setTimeIntervalBullet = 5
        self.setTimeIntervalRect = 0
        
        self.speed = 2

        self.score = 0
        self.totalHit = 0
        self.GameOver = False
        self.Ready = False 
        self.HaveCoordinatePoints = False

        self.Bullets = []
        self.Targets = []

        self.BulletsList = []
        self.BulletsAndTime = []

        self.v_ret =[]
        self.v_frame=[]
        self.h_ret =[]
        self.h_frame=[]
        
        self.VerticalRects = []
        self.HorizontalRects = []

        self.VerticalBaseLine = int((480*29)/30)
        self.HorizontalBaseLine = int((480*29)/30)

        self.num_frame = 0
        self.VerticalTrackableObjects = {}
        self.HorizontalTrackableObjects = {}
        self.VerticalObject = []
        self.HorizontalObject = []

        self.VerticalHitRect = []
        self.HorizontalHitRect = []
        self.HitObjects = []

    def init(self):
        super(AlienShooting, self).init()
        self.hit  = pygame.mixer.Sound('res/sound/correct.wav')
        self.miss = pygame.mixer.Sound('res/sound/wrong.wav')
        self.border_image = pygame.image.load("res/text/border.png")
        self.border_image = pygame.transform.scale(self.border_image, (300, 100))
        self.render_score()

    def update(self):
        self.v_frame = vertical_cap.read()

        self.h_frame = horizontal_cap.read()

        cv.line(self.v_frame, (0, self.VerticalBaseLine), (640, self.VerticalBaseLine), (0, 255, 255), 2)
        cv.line(self.h_frame, (0, self.VerticalBaseLine), (640, self.VerticalBaseLine), (0, 255, 255), 2)

        if not(self.HaveCoordinatePoints):
            self.renderDetection()
            self.GetCoordinate()
        else:

            for Point in VerticalPoints:
                cv.line(self.v_frame, (Point, 0), (Point, 1920), (0, 255, 255), 2)
            for Point in HorizontalPoints:
                cv.line(self.h_frame, (Point, 0), (Point, 1920), (0, 255, 255), 2)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
            if self.is_key_pressed(K_SPACE):
                self.Ready = True
                self.addTarget()
            if (self.Ready):
                self.updateTarget()
                rects = []


                self.VerticalRects = self.ContourFinding(self.v_frame,0)
                self.HorizontalRects = self.ContourFinding(self.h_frame,1)

                if (len(self.VerticalHitRect) > 0) and (len(self.HorizontalHitRect) > 0):
                    Overlap = False
                    V_cts = []
                    H_cts = []
                    for Rect in self.VerticalHitRect:
                        V_cts.append(((VerticalPoints[1] - (Rect[0]+Rect[2]/2))/(VerticalPoints[1] - VerticalPoints[0]))*1080)
                        print("V_ct = " + str((Rect[0]+Rect[2]/2))+ " Ver[1] = " + str(VerticalPoints[1]) + " Ver[0] = " + str(VerticalPoints[0]) )

                    for Rect in self.HorizontalHitRect:
                        H_cts.append(((HorizontalPoints[1] - (Rect[0]+Rect[2]/2))/(HorizontalPoints[1] - HorizontalPoints[0]))*1920)
                        print("H_ct = " + str((Rect[0]+Rect[2]/2))+ " Hor[1] = " + str(HorizontalPoints[1]) + " Hor[0] = " + str(HorizontalPoints[0]) )

                    # min_length = min(len(self.VerticalHitRect),len(self.HorizontalHitRect))
                    # for index in range(0,min_length):
                    point = (H_cts[0],V_cts[0])
                    time = pygame.time.get_ticks() / 1000

                    print("time: " + str(time))
                    # for Bullet in  self.Bullets :
                    #     if((H_cts[0] > Bullet.x - 10 or H_cts[0] < Bullet.x + 10) and (V_cts[0] > Bullet.y - 10 or V_cts[0] < Bullet.y + 10) ):
                    #         Overlap = True
                    # if not Overlap:
                    if (len(self.BulletsList) == 0) or not (point in self.BulletsList):
                        self.addBullet(H_cts[0],V_cts[0])
                        self.checkCollisionTarget(point)
                    else:
                        if (not self.CheckBulletOverlapped(H_cts[0],V_cts[0])):
                            self.addBullet(H_cts[0],V_cts[0])
                            self.checkCollisionTarget(point)        
                    
                    self.VerticalHitRect = []
                    self.HorizontalHitRect = []


                self.VerticalHitRect = []
                self.HorizontalHitRect = []

                self.VerticalRects = []
                self.HorizontalRects = []

                if not(self.GameOver):
                    self.render_score()
                    self.updateBullet()

        self.renderDetection()

    def GetCoordinate(self):
        if not(self.HaveCoordinatePoints):
            
            VerticalPoints.append(469)
            VerticalPoints.append(14)
            
            HorizontalPoints.append(593)
            HorizontalPoints.append(45)
            
            if (len(VerticalPoints) >= 2) and (len(HorizontalPoints) >= 2)  :
                self.HaveCoordinatePoints = True
                VerticalPoints.sort()
                print(str(VerticalPoints))
                HorizontalPoints.sort()
                print(str(HorizontalPoints))
                print("Success Get Coordination Line")

    def FindDistance(self, RectA,RectB):
        ct_A = FindCentroid(RectA)
        ct_B = FindCentroid(RectB)
        return math.sqrt(((ct_A[0]-ct_B[0])**2)+((ct_A[1]-ct_B[1])**2))

    def ContourFinding(self,frame,perspective):
        rects = []

        fgmask = fgbg.apply(frame)
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)

        dilation = cv.dilate(fgmask,kernel_dil,iterations=1)
        ____,contours,hierarchy = cv.findContours(dilation,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        for pic,contour in enumerate(contours):
            area = cv.contourArea(contour)
            if(area> 800):
                x,y,w,h = cv.boundingRect(contour)
                # rects.append(cv.boundingRect(contour))
                # print("x and y: "+ str(x) +" "+ str(y))
                rects.append((x,y,w,h))
                if perspective == 0: 
                    if y+h > self.VerticalBaseLine  and x+w >= HorizontalPoints[0] and x+w <= HorizontalPoints[1]:
                        self.VerticalHitRect.append((x,y,w,h))                                                                                                                                
                if perspective == 1: 
                    if y+h > self.HorizontalBaseLine  and x+w >= HorizontalPoints[0] and x+w <= HorizontalPoints[1]:    
                        self.HorizontalHitRect.append((x,y,w,h))

                # img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                
            pass
        return rects

    def ObjectTracker(self,objects,perspective):
        # cv.rectangle(self.frame, (200, 200), (900, 600),(0,255,0),2)
        for (objectID, centroid) in objects.items():
            if perspective == 0:
                TrackObject = self.VerticalTrackableObjects.get(objectID, None)
            elif perspective == 1:
                TrackObject = self.HorizontalTrackableObjects.get(objectID, None)
            
            if TrackObject is None:
                TrackObject = TrackableObject(objectID, centroid)
            else: 
                if perspective == 0:
                    for centroid in TrackObject.centroids:
                        cv.circle(self.v_frame, (centroid[0] , centroid[1]), 6, (0, 255, 255), -1)
                elif perspective == 1:
                    for centroid in TrackObject.centroids:
                        cv.circle(self.h_frame, (centroid[0] , centroid[1]), 6, (0, 255, 255), -1)
                
                y = [c[1] for c in TrackObject.centroids]
                direction = centroid[1] - np.mean(y)    
                TrackObject.centroids.append(centroid)

            if perspective == 0:
                self.VerticalTrackableObjects[objectID] = TrackObject
                text = "ID {}".format(objectID)
                cv.putText(self.v_frame, text, (centroid[0] - 10, centroid[1] - 10),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv.circle(self.v_frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            elif perspective == 1:
                self.HorizontalTrackableObjects[objectID] = TrackObject
                text = "ID {}".format(objectID)
                cv.putText(self.h_frame, text, (centroid[0] - 10, centroid[1] - 10),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv.circle(self.h_frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
           

    def checkCollisionTarget(self, point):
        for Target in self.Targets:
            Target.getrectTarget()
            if(Target.getrectTarget().collidepoint(point)):
                # if(not(point) in self.BulletsList):
                print("Hit at: "+str(point) + "\n")
                self.score += 1
                # self.speed += self.score / 10
                # for Target in self.Targets:
                #     Target.ChangeSpeed(self.speed)
                self.hit.play()
            else:
                self.miss.play()
                # self.Targets.remove(Target)

    def CheckBulletOverlapped(self,x,y):
        for Bullet in self.Bullets:
            distance = math.sqrt( ((Bullet.x - x)**2)+((Bullet.y - y)**2) )
            if distance <= 3:
                return True

        return False

    def addBullet(self,pos_x,pos_y):    
        timestamp = int(pygame.time.get_ticks() / 1000)
        self.Bullets += [Bullet(x = pos_x , y = pos_y,TimeStamp = timestamp)]   

    def updateBullet(self):
        deltatime = int(pygame.time.get_ticks() / 1000)

        print("deltatime: "+str(deltatime))
        # if deltatime > self.setTimeIntervalBullet :
        #     self.setTimeIntervalBullet = deltatime
        #     self.setTimeIntervalBullet += 3
        if(len(self.Bullets) > 0 ):
            for Bullet in self.Bullets :
                if (Bullet.TimeStamp + 2 <= deltatime):
                    self.Bullets.remove(Bullet)
                    pass


        for Bullet in self.Bullets :
            Bullet.update()

    def renderBullet(self, surface):
        for Bullet in self.Bullets :
            Bullet.render(surface)

    def addTarget(self):    
        self.Targets += [Target(health = 2)]    
    
    def renderTarget(self, surface):
        for Target in self.Targets :
            Target.render(surface)

    def updateTarget(self):
        deltatime = pygame.time.get_ticks() / 10000
        if deltatime > self.setTimeIntervalTarget :
            self.setTimeIntervalTarget = deltatime

        for Target in self.Targets :
            Target.update()

    def renderDetection(self):
        cv.imshow('Vertical_Perspective',self.v_frame)
        cv.imshow('Horizontal_Perspective',self.h_frame)

        if cv.waitKey(30) & 0xff ==ord("q"):
            cv.destroyAllWindows()
            vertical_cap.stop()
            horizontal_cap.stop()

    def render_score(self):
        # self.score_image_f = self.font.render("Score = %d" % self.score, 0, WHITE)
        self.score_image = self.font.render("Score = %d" % self.score, 0, WHITE)
        # print(self.score)
    
    def render(self, surface):
        self.renderTarget(surface)
        surface.blit(self.border_image, (30,45))
        surface.blit(self.score_image, (80,60))
        self.renderBullet(surface)
        if self.GameOver == True :
            self.GameOver_image = self.font.render("Game Over!!!", 0,AlienShooting.BLACK)
            surface.blit(self.GameOver_image,(500,300))

def main():
    game = AlienShooting()
    game.run()
if __name__ == '__main__':
    main()  