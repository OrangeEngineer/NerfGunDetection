import cv2 as cv
from darkflow.net.build import TFNet
from tracker.centroidtracker import CentroidTracker
from tracker.trackableobject import TrackableObject
import numpy as np
import time
import imutils

def FindPoint(x1, y1, x2, y2, x, y) : 
    if (x > x1 and x < x2 and 
        y > y1 and y < y2) : 
        return True
    else : 
        return False

options = {
    'model': 'yolov2-tiny.cfg',
    'load': 'yolov2-tiny.weights',
    'threshold': 0.2,
    'gpu': 1.0
}

tfnet = TFNet(options)
colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]

ct = CentroidTracker()
trackableObjects = {}

totalHit = 0

# (H, W) = (1600, 869)
(H, W) = (None, None)

capture = cv.VideoCapture(0)
# capture = cv.VideoCapture(r'C:\Users\Nuttaphon\Documents\NerfGun\TestWithLogitech_31_03_19\2.mp4')
capture.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

fgbg = cv.createBackgroundSubtractorMOG2()
kernel_dil = np.ones((20,20),np.uint8)
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))

while True:
    stime = time.time()
    ret, frame = capture.read()

    rects = []
    TargetRects = []
    if ret == True:
        fgmask = fgbg.apply(frame)
        fgmask[fgmask==127]=0
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
        dilation = cv.dilate(fgmask,kernel_dil,iterations=1)
        (contours,hierarchy) = cv.findContours(dilation,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        for pic,contour in enumerate(contours):
            area = cv.contourArea(contour)
            if( area > 500 and area < 4000):
                print(area)
                x,y,w,h = cv.boundingRect(contour)
                w = w*2
                h = h*2
                rects.append((x,y,w,h))
                img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                roi_bullet = frame[y:y-10+h+5,x:x-8+w+10]
            pass

        objects = ct.update(rects)

        results = tfnet.return_predict(frame)
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            print("position: "+ str(tl)+" " + str(br))
            TargetRects.append((tl[0],tl[1],br[0],br[1]))
            label = result['label']
            confidence = result['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            frame = cv.rectangle(frame, tl, br, color, 5)
            frame = cv.putText(
                frame, text, tl, cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

        for (objectID, centroid) in objects.items():
            
            TrackObject = trackableObjects.get(objectID, None)

            if TrackObject is None:
                TrackObject = TrackableObject(objectID, centroid)
            else: 
                y = [c[1] for c in TrackObject.centroids]
                direction = centroid[1] - np.mean(y)
                TrackObject.centroids.append(centroid)
                if not TrackObject.counted:
                    # totalHit += 1
                    # TrackObject.counted = True
                    print("x and y: "+ str(centroid[0]) +" "+ str(centroid[1]))
                    for Target in TargetRects:
                        if  (FindPoint(Target[0], Target[1], Target[2], Target[3], centroid[0], centroid[1])) :
                            totalHit += 1
                            TrackObject.counted = True

            trackableObjects[objectID] = TrackObject
            text = "ID {}".format(objectID)
            cv.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
    
    info = [
		("Score: ", totalHit),
	]
    for (i, (k, v)) in enumerate(info):
        text = "{}: {}".format(k, v)
        cv.putText(frame, text, (10, 800 - ((i * 20) + 20)),cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv.imshow('frame', frame)
    print('FPS {:.1f}'.format(1 / (time.time() - stime)))
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()