import cv2
import numpy as np
frameWidth=640
frameHeight= 480

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

myColors=[[135,84,0,173,231,198],
          [0,0,0,93,0,93],
          [96,131,25,115,255,141]]
 

#BGR
myColorValues=[[85,8,85], 
               [17,17,238],
               [225,225,10]]

Points= [] #[x,y,colorId]

def findColor(img, myColors,myColorValues):
    imgHSV= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    i=0
    newPoints=[]
    for color in myColors:
        lower=np.array(color[0:3])
        upper=np.array(color[3:6])
        mask=cv2.inRange(imgHSV, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y), 10, myColorValues[i], cv2.FILLED)
        #cv2.imshow(str(i), mask)
        if x!=0 and y!=0:
            newPoints.append([x,y,i])
        i+=1
    return newPoints
        
def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def drawonCanvas(Points, myColorValues):
    for point in Points:
         cv2.circle(imgResult,(point[0],point[1]), 10, myColorValues[point[2]], cv2.FILLED)
        
while True:
    success, img= cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors,myColorValues)
    
    if len(newPoints)!=0:
        for newP in newPoints:
            Points.append(newP)
    
    if len(Points)!=0:
        drawonCanvas(Points,myColorValues)
    
    cv2.imshow("Webcam", imgResult)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break