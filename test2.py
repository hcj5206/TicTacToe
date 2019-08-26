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

