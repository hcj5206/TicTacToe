# import cv2
# imgsrc = cv2.imread('22.jpg')
# (B, G, R) = cv2.split(imgsrc)                                                                                       #Split colour into BGR channels respectively
# h, w, c = imgsrc.shape                                                                                              #Find height(row), width(column) & BGR
# gray = R
# # (3280, 2464)
# cropped = gray[0:h-500,400:w-400]
# cv2.imwrite("f2.jpg",R )
# cv2.imwrite("f3.jpg",cropped )
# ret2, threshimg = cv2.threshold(cropped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# cv2.imwrite("f.jpg",threshimg)
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 09:32:02 2016

@author: http://blog.csdn.net/lql0716
"""
import cv2
import numpy as np

current_pos = None
tl = None
br = None

#鼠标事件
def get_rect(im, title='get_rect'):   #   (a,b) = get_rect(im, title='get_rect')
    mouse_params = {'tl': None, 'br': None, 'current_pos': None,
        'released_once': False}

    cv2.namedWindow(title)
    cv2.moveWindow(title, 20, 20)

    def onMouse(event, x, y, flags, param):

        param['current_pos'] = (x, y)

        if param['tl'] is not None and not (flags & cv2.EVENT_FLAG_LBUTTON):
            param['released_once'] = True

        if flags & cv2.EVENT_FLAG_LBUTTON:
            if param['tl'] is None:
                param['tl'] = param['current_pos']
            elif param['released_once']:
                param['br'] = param['current_pos']

    cv2.setMouseCallback(title, onMouse, mouse_params)
    cv2.imshow(title, im)

    while mouse_params['br'] is None:
        im_draw = np.copy(im)

        if mouse_params['tl'] is not None:
            cv2.rectangle(im_draw, mouse_params['tl'],
                mouse_params['current_pos'], (255, 0, 0))

        cv2.imshow(title, im_draw)
        _ = cv2.waitKey(10)

    cv2.destroyWindow(title)

    tl = (min(mouse_params['tl'][0], mouse_params['br'][0]),
        min(mouse_params['tl'][1], mouse_params['br'][1]))
    br = (max(mouse_params['tl'][0], mouse_params['br'][0]),
        max(mouse_params['tl'][1], mouse_params['br'][1]))

    return list(tl), list(br)  #tl=(y1,x1), br=(y2,x2)

#读取摄像头/视频，然后用鼠标事件画框
def readVideo(pathName, skipFrame):  #pathName为视频文件路径，skipFrame为视频的第skipFrame帧
    cap = cv2.VideoCapture(0)    #读取摄像头
    if not cap.isOpened():  #如果为发现摄像头，则按照路径pathName读取视频文件
        cap = cv2.VideoCapture(pathName)    #读取视频文件，如pathName='D:/test/test.mp4'
    c = 1

    while(cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if(c>=skipFrame):
            mask = np.zeros(gray.shape, dtype=np.uint8)  #掩码操作，该矩阵与图片大小类型一致，为初始化全0像素值，之后对其操作区域赋值为1即可
            if(c==skipFrame):
                (a,b) = get_rect(frame, title='get_rect')  #鼠标画矩形框
                img01, img02 = frame, frame
                gray01, gray02 = gray, gray
            else:
                img1, img2 = prev_frame, frame
                gray1, gray2 = prev_frame, frame
            cv2.imshow('frame', frame)
        c = c + 1
        prev_gray = gray
        prev_frame = frame
        if cv2.waitKey(1) & 0xFF == ord('q'):    #点击视频窗口，按q键退出
            break
    cap.release()
    cv2.destroyAllWindows()
def FirstConfig():
    import configparser
    cf = configparser.ConfigParser()
    cf.read("./config.ini")
    IsRestart = cf.get("Setting", "IsRestart")
    if IsRestart==1:
        imgsrc = cv2.imread('22.jpg')
        h, w = imgsrc.shape[0:2]
        (B, G, R) = cv2.split(imgsrc)
        img2 = cv2.resize(imgsrc, (int(w / 5), int(h / 5)))
        pos1, pos2 = get_rect(img2)
        gray = R

if __name__ == '__main__':
    imgsrc = cv2.imread('./TestBorad/02.jpg')
    h,w=imgsrc.shape[0:2]
    img2=cv2.resize(imgsrc,(int(w/5),int(h/5)))
    pos1,pos2=get_rect(img2)
    print(pos1,pos2)
    x1=pos1[0] * 5
    y1=pos1[1] * 5
    x2=pos2[0] * 5
    y2=pos2[1] * 5

    cropped = imgsrc[y1:y2,x1:x2]
    # cv2.imwrite("f2.jpg",R )
    cv2.imwrite("f3.jpg",cropped )
    # ret2, threshimg = cv2.threshold(cropped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imwrite("f.jpg",threshimg)
