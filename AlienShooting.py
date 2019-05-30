import pygame
import sys
from pygame.locals import *
from pygame import *
from tracker.centroidtracker import CentroidTracker
from tracker.trackableobject import TrackableObject
import random
import math
import gamelib
import time
import numpy as np
import cv2 as cv
import imutils

from Target import *
from Bullet import *

# cap = cv.VideoCapture(r'C:\Users\Nuttaphon\Documents\NerfGun\TestWithLogitech_31_03_19\2.mp4')
# cap = cv.VideoCapture(1 + cv.CAP_DSHOW)
cap = cv.VideoCapture(1)
#Decrease frame size
# cap.set(3, 1920)
# #cv2.CAP_PROP_FRAME_WIDTH
# cap.set(4, 1080)
cap.set(cv.CAP_PROP_FPS, 90)

# cap.set(5, 90)
# 137 175
# 1369 141
# 144 811
# 1362 876
ix,iy = -1,-1
# frame = cv.warpPerspective(frame, matrix, (1920, 1080))
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
RED = ( 120, 0, 0)
ct = CentroidTracker()
CoordinatePoints = []

def minSum(a):
    max = 200000 
    dmax = (0,0)
    for i in range(len(a)):
        if (a[i][0]+a[i][1] < max):
            dmin = a[i]
            max = a[i][0]+a[i][1]
    return dmin

def maxSum(a):
    min = 0 
    dmax = (0,0)
    for i in range(len(a)):
        if (a[i][0]+a[i][1] > min):
            dmax = a[i]
            min = a[i][0]+a[i][1]
    return dmax

def GetPoint(event,x,y,flags,param):
    if (event == cv.EVENT_LBUTTONDBLCLK):
        CoordinatePoints.append((x,y))
        print(str(x) +" " +str(y))

# def nothing(x):
#     pass

# cv.namedWindow("Trackbars")

# cv.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
# cv.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
# cv.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
# cv.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
# cv.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
# cv.createTrackbar("U - V", "Trackbars", 255, 255, nothing)


class AlienShooting(gamelib.NerfGunGame):
    WHITE = pygame.Color('white')
    BLACK = pygame.Color('black')
    def __init__(self):
        super(AlienShooting, self).__init__('Protect the world from aliens!!', WHITE)
        self.setTimeIntervalTarget = 0
        self.setTimeIntervalBullet = 0
        self.score = 0
        self.totalHit = 0
        self.GameOver = False
        self.Ready = False 
        self.HaveCoordinatePoints = False
        self.Coor = []
        self.Bullets = []
        self.Targets = []
        self.Coor_rect = np.zeros((4, 2), dtype = "float32")
        self.ret =[]
        self.frame=[]
        self.PT_frame=[]
        self.ContourFrame = []
        self.rects = []
        self.num_frame = 0
        self.trackableObjects = {}
        self.fps = 0
        self.fgbg = cv.createBackgroundSubtractorMOG2()
        self.kernel_dil = np.ones((20,20),np.uint8)
        self.kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))

    def init(self):
        super(AlienShooting, self).init()
        self.render_score()

    def update(self):
        self.ret, self.frame = cap.read()
        self.renderDetection()

        # self.fps = cap.get(cv.CAP_PROP_FPS)
        # print("fps = " + str(self.fps))
        if not(self.HaveCoordinatePoints):
            self.GetCoordinate()
        else:
            pts1 = np.float32([self.Coor_rect[0], self.Coor_rect[1], self.Coor_rect[2], self.Coor_rect[3]])
            pts2 = np.float32([[0, 0], [1920, 0], [0, 1080], [1920, 1080]])
            # pts1 = np.float32([[137,175], [1369,141], [144,811], [1362,876]])
            # pts2 = np.float32([[0, 0], [1920, 0], [0, 1080], [1920, 1080]])
            matrix = cv.getPerspectiveTransform(pts1, pts2)

            self.PT_frame = cv.warpPerspective(self.frame, matrix, (1920, 1080))
            if not(self.Ready):
                self.renderPerspectiveTranform()
            if self.is_key_pressed(K_SPACE):
                self.Ready = True
                self.addTarget()
            if (self.Ready):
                self.updateTarget()
                ############################## Perspective Tranform Part ##################################
                # pts1 = np.float32([[137,175], [1369,141], [144,811], [1362,876]])
                # pts2 = np.float32([[0, 0], [1920, 0], [0, 1080], [1920, 1080]])
                # matrix = cv.getPerspectiveTransform(pts1, pts2)

                # self.frame = cv.warpPerspective(self.frame, matrix, (1920, 1080))
                ############################################################################################
                # self.frame = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
                # _, threshold = cv.threshold(self.frame, 70, 100, cv.THRESH_BINARY)
                # _, contours = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                # ratio = self.frame.shape[0] / 400.0
                # orig = self.frame.copy()
                # self.frame = imutils.resize(self.frame, height = 400)
                # gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
                # gray = cv.bilateralFilter(gray, 11, 17, 17)
                # edged = cv.Canny(gray, 30, 200)

                ############################################################################################
                # cnts = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                # cnts = imutils.grab_contours(cnts)
                # cnts = sorted(cnts, key = cv.contourArea, reverse = True)[:10]
                # screenCnt = None
                # for c in contours:
                # #     # approximate the contour
                #     # peri = cv.arcLength(c, True)
                #     approx = cv.approxPolyDP(c, 0.01, True)
                #     cv.drawContours(self.frame, [c], -1, (0, 255, 0), 3)
                #     # if our approximated contour has four points, then
                #     # we can assume that we have found our screen
                #     if len(approx) == 4:
                #         screenCnt = approx
                #         break

                ############################################################################################

                rects = []


                self.fgmask = self.fgbg.apply(self.PT_frame)
                # 0 26 86
                # 43 222 255

                # lower_blue = np.array([21, 66, 87])
                # upper_blue = np.array([81, 114,164])


                # l_h = cv.getTrackbarPos("L - H", "Trackbars")
                # l_s = cv.getTrackbarPos("L - S", "Trackbars")
                # l_v = cv.getTrackbarPos("L - V", "Trackbars")
                # u_h = cv.getTrackbarPos("U - H", "Trackbars")
                # u_s = cv.getTrackbarPos("U - S", "Trackbars")
                # u_v = cv.getTrackbarPos("U - V", "Trackbars")

                # lower_blue2 = np.array([l_h, l_s, l_v])
                # upper_blue2 = np.array([u_h, u_s, u_v])


                # mask = cv.inRange(self.PT_frame, lower_blue, upper_blue)
                # mask2 = cv.inRange(self.PT_frame, lower_blue2, upper_blue2) 
                # # self.fgmask = self.fgmask - mask
                # self.fgmask = self.fgmask - mask2
                self.fgmask[self.fgmask==127]=0
                self.fgmask = cv.morphologyEx(self.fgmask, cv.MORPH_OPEN, self.kernel)

                self.ContourFrame = self.fgmask
                cv.namedWindow('Contour',cv.WINDOW_NORMAL)
                cv.imshow('Contour',self.ContourFrame)
                dilation = cv.dilate(self.fgmask,self.kernel_dil,iterations=1)
                (contours,hierarchy) = cv.findContours(dilation,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
                for pic,contour in enumerate(contours):
                    area = cv.contourArea(contour)
                    if(area> 1500 and area < 5500):
                        print("area size: " + str(area))
                        x,y,w,h = cv.boundingRect(contour)
                        # rects.append(cv.boundingRect(contour))
                        # print("x and y: "+ str(x) +" "+ str(y))
                        w = w*2
                        h = h*2
                        self.rects.append((x,y,w,h))
                        img = cv.rectangle(self.PT_frame,(x,y),(x+w,y+h),(0,0,255),2)
                        roi_bullet = self.PT_frame[y:y-10+h+5,x:x-8+w+10]
                    pass

                objects = ct.update(self.rects)

                # cv.rectangle(self.frame, (200, 200), (900, 600),(0,255,0),2)
                for (objectID, centroid) in objects.items():
                    
                    TrackObject = self.trackableObjects.get(objectID, None)

                    if TrackObject is None:
                        TrackObject = TrackableObject(objectID, centroid)
                    else: 
                        y = [c[1] for c in TrackObject.centroids]
                        direction = centroid[1] - np.mean(y)
                        TrackObject.centroids.append(centroid)
                        if not TrackObject.counted:
                            # self.totalHit += 1
                            # TrackObject.counted = True
                            # print("x and y: "+ str(centroid[0]) +" "+ str(centroid[1]))
                            self.addBullet(centroid[0],centroid[1])
                            if  (self.checkCollisionTarget(centroid[0], centroid[1])) :
                                self.totalHit += 1
                                TrackObject.counted = True

                    self.trackableObjects[objectID] = TrackObject
                    text = "ID {}".format(objectID)
                    cv.putText(self.PT_frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv.circle(self.PT_frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                self.rects = []
                if not(self.GameOver):
                    self.checkCollisionTarget(ix,iy)
                    self.renderPerspectiveTranform()
                    self.render_score()
                    self.updateBullet()

    def GetCoordinate(self):
        if not(self.HaveCoordinatePoints):
            cv.setMouseCallback('Detection Process',GetPoint)
            if (len(CoordinatePoints) >= 4 ):

                self.Coor = CoordinatePoints  
                self.Coor_rect[0] = minSum(self.Coor)
                self.Coor_rect[3] = maxSum(self.Coor)
                self.Coor.remove(minSum(self.Coor))
                self.Coor.remove(maxSum(self.Coor))
                self.Coor = sorted(self.Coor, key=lambda x: x[1])

                self.Coor_rect[1] = self.Coor[0]
                self.Coor_rect[2] = self.Coor[1]
                self.HaveCoordinatePoints = True
                print("Success Get Coordinating Points")

    def checkCollisionTarget(self,x,y):
        for Target in self.Targets:
            Target.getrectTarget()
            if(Target.getrectTarget().collidepoint(x,y)):
                self.score += 1
                # self.Targets.remove(Target)
                return True
            else:
                return False

    def addBullet(self,pos_x,pos_y):    
        self.Bullets += [Bullet(x = pos_x , y = pos_y)]   

    def updateBullet(self):
        deltatime = pygame.time.get_ticks() / 10000
        if deltatime > self.setTimeIntervalBullet :
            self.setTimeIntervalBullet = deltatime
            for Bullet in self.Bullets :
                self.Bullets.remove(Bullet)
        # print("Delta Time: " + str(deltatime))
        # print("setTimeIntervalBullet: " + str(self.setTimeIntervalBullet))            
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

        # for x in range(len(self.Targets), int(deltatime - len(self.Targets))) :
        #         self.addTarget()
        for Target in self.Targets :
            Target.update()

    def renderDetection(self):
        cv.namedWindow('Detection Process',cv.WINDOW_NORMAL)
        cv.imshow('Detection Process',self.frame)

    def renderPerspectiveTranform(self):
        cv.namedWindow('Perspective Tranformed',cv.WINDOW_NORMAL)
        cv.imshow('Perspective Tranformed',self.PT_frame)

        # cv.imwrite(str(self.num_frame)+'.png',self.PT_frame)
        # self.num_frame +=1

    def render_score(self):
        self.score_image = self.font.render("Score = %d" % self.score, 0,AlienShooting.BLACK)
        # print(self.score)
    
    def render(self, surface):
        self.renderTarget(surface)
        self.renderBullet(surface)
        surface.blit(self.score_image, (10,10))
        if self.GameOver == True :
            self.GameOver_image = self.font.render("Game Over!!!", 0,AlienShooting.BLACK)
            surface.blit(self.GameOver_image,(500,300))

def main():
    game = AlienShooting()
    game.run()
if __name__ == '__main__':
    main()  