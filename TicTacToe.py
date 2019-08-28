#last update 20190526 1831
import time

import cv2
import numpy as np
import configparser
from GetRectPos import FirstConfig

broad=[[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
#Find the maximum contour
def findmaxcontour(contours):
    maxarea = 0
    maxid = 0
    id = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > maxarea:
            maxid = id
            maxarea = area
        id = id + 1
    return maxid

#Find centre
def get_centre(chess):
    rect = cv2.minAreaRect(chess)   #find the minimum rectangle,[0]centre(x,y), [1][0]width, [1][1]height, [2]angle
    return rect[0]                  #find the centre only

#Find each chess coordinate
def get_pos(img, chesses):
    h, w, c = img.shape         #Find height(row), width(column) & BGR
    cords = []                  
    points = []
    posIndex=[]
    xstep = w / 3               #Divide the width by 3, use the quotient as step on x-asix
    ystep = h / 3               #Divide the height by 3, use the quotient as step on y-asix
    for chess in chesses:
        point = get_centre(chess)
        xid = int(point[0] / xstep)
        yid = int(point[1] / ystep)
        points.append(point)
        cords.append([xid, yid])
        posIndex.append(broad.index([xid, yid])) #获取对应的格子
    return points, cords,posIndex

#Find chess contour and its type
def find_chesses(imgsrc):
    (B, G, R) = cv2.split(imgsrc)                                                                                       #Split colour into BGR channels respectively
    h, w, c = imgsrc.shape                                                                                              #Find height(row), width(column) & BGR
    gray = R                                                                                                          #Use red as the chesses are red
    ret2, threshimg = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((5, 5), np.uint8)                                                                                  #Define a kernel full of ones, size is 5x5
    open_dst = cv2.morphologyEx(threshimg, cv2.MORPH_OPEN, kernel)                                                      #Morphology to remove background noise, opening=erosion then dilation
    open_dst, contours, hierarchy = cv2.findContours(open_dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)              #Find contour, only the external contours is used, only endpoints are used

    id = 0
    threasharea = h * w / 50;                                                                                           #Define threshold area
    chesses = []
    for contour in contours:
        if cv2.contourArea(contour) > threasharea:                                                                      #Condition for drawing contour   
            cv2.drawContours(imgsrc, contours, id, (0, 0, 255), 5)                                                      #Draw red line around the contour, line thickness=5
            chesses.append(contour)
            id = id + 1

    chesstypes = []
    pts_dst = np.array([[0, tempw], [0, 0], [temph, 0], [temph, tempw]], dtype="float32") #Define points on output image
    id = 0
    for chess in chesses:
        rect = cv2.minAreaRect(chess)
        box = cv2.boxPoints(rect) #Find the vertices defining the rectangle
        box = np.int0(box) #Return the verticles to integer
        boxf = box.astype(np.float32) #Convert type of array

        H = cv2.getPerspectiveTransform(boxf, pts_dst) #Find transformation matrix
        warp = cv2.warpPerspective(open_dst, H, (temph, tempw), cv2.INTER_NEAREST) #Perspective transform with respect to the matrix

        warp, contoursdraw, hierarchy = cv2.findContours(warp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_out = contoursdraw[findmaxcontour(contoursdraw)]

        reto = cv2.matchShapes(contouro, contour_out, cv2.CONTOURS_MATCH_I1, 0.0)   #Check similarity with O
        retx = cv2.matchShapes(contourx, contour_out, cv2.CONTOURS_MATCH_I1, 0.0)   #Check similarity with X
        if reto < retx:                                                             #Compare the similarity of X & O
            chesstypes.append('O')                                                  #If similarity with O is lower than X, then output O
        else:
            chesstypes.append('X')
        # print("Similarity with O:", 1-reto) #Print similarity with O, higher is similar
        # print("Similarity with X:", 1-retx) #Print similarity with X, higher is similar
        id = id + 1
    return chesstypes, chesses
imgo = cv2.imread('O.jpg', 0)               #import O
imgx = cv2.imread('X.jpg', 0)               #import X
temph, tempw = imgo.shape #Get the height and width
ret, imgo = cv2.threshold(imgo,178,255,cv2.THRESH_BINARY)                                           #Thresholding using 178 into B&W
ret, imgx = cv2.threshold(imgx,178,255,cv2.THRESH_BINARY)                                           #Thresholding using 178 into B&W
imgo, contourso, hierarchyo = cv2.findContours(imgo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    #Find contour of template, only the external contour is used, only endpoints are used
imgx, contoursx, hierarchyx = cv2.findContours(imgx, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    #Find contour of template, only the external contour is used, only endpoints are used
contouro = contourso[findmaxcontour(contourso)]
contourx = contoursx[findmaxcontour(contoursx)]
showtempo = np.zeros(imgo.shape, np.uint8)
def GetBroadDic(path):
    broad_dic={0:"",1:"",2:"",3:"",4:"",5:"",6:"",7:"",8:""} #当前棋盘信息初始化
    imagename = "./TestBorad/"+str(path)+".jpg"
    if FirstConfig(imagename):
        try:
            img = cv2.imread(imagename)
            x0, x1, y0, y1 = _GetRect()
            # img = img[x0:y1, x1:y1]
            img = img[y0:y1, x0:x1]

            cv2.imwrite("./result/%s" % (str(path)+".jpg"), img)
            chesstypes, chesses = find_chesses(img)
            points, cords, posIndex = get_pos(img, chesses)
            for t in range(len(posIndex)):
                broad_dic[posIndex[t]] = chesstypes[t]
            return broad_dic
        except:
            print("Error,Get Broad_Dic error")
            return False
def _GetRect():
    cf = configparser.ConfigParser()
    cf.read("./config.ini")
    x0 = int(cf.get("Setting", "x0"))
    x1 = int(cf.get("Setting", "x1"))
    y0 = int(cf.get("Setting", "y0"))
    y1 = int(cf.get("Setting", "y1"))
    return x0,x1,y0,y1
def GetBroadDicAllPath(num):
    from GetCamera import SaveCameraPic
    Flag,path=SaveCameraPic(num)
    broad_dic={0:"",1:"",2:"",3:"",4:"",5:"",6:"",7:"",8:""} #当前棋盘信息初始化
    imagename = "./"+str(path)
    if FirstConfig(path):
        try:
            img = cv2.imread(imagename)
            x0, x1, y0, y1=_GetRect()
            img=img[y0:y1, x0:x1]
            cv2.imwrite("./result/%s"%path, img)
            chesstypes, chesses = find_chesses(img)
            points, cords,posIndex = get_pos(img, chesses)
            for t in range(len(posIndex)):
                broad_dic[posIndex[t]]=chesstypes[t]
            return broad_dic
        except:
            print("Error,Get Broad_Dic error")
            return False


if __name__ == '__main__':
    print(GetBroadDic('02'))
