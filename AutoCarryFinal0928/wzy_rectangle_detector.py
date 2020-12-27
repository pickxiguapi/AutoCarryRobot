# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 15:35:26 2020

@author: wangz
"""

import cv2
import numpy as np
import time
class ShapeAnalysis:
    def __init__(self):
        self.shapes = { 'rectangle': 0, 'polygons': 0}
        self.ball_color = 'red'
        self.color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([10, 255, 255])},
              'yellow': {'Lower': np.array([20, 80, 46]), 'Upper': np.array([40, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              }
        self.kernel_4 = np.ones((3,3),np.uint8)#10x10的卷积核
    
    
    def analysis(self, frame,color):
        self.ball_color = color
        h, w, ch = frame.shape
        result = np.zeros((h, w, ch), dtype=np.uint8)
        # 二值化图像
        print("start to detect lines...\n")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
        inRange_hsv = cv2.inRange(hsv, self.color_dist[self.ball_color]['Lower'], self.color_dist[self.ball_color]['Upper'])
        #下面四行是用卷积进行滤波
        #erosion = cv.erode(inRange_hsv,self.kernel_4,iterations = 3)
        #erosion = cv.erode(erosion,self.kernel_4,iterations = 1)
        #dilation = cv.dilate(erosion,self.kernel_4,iterations = 1)
        #dilation = cv.dilate(dilation,self.kernel_4,iterations = 1) 
        target = cv2.bitwise_and(frame, frame, mask=inRange_hsv )#保留红色
        gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        #cv.imshow('binary',binary)
        cv2.imshow("input image", frame)
    
        binary, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in range(len(contours)):
            # 提取与绘制轮廓
            cv2.drawContours(target, contours, cnt, (0, 255, 0), 2)
            # 轮廓逼近
            epsilon =15#0.01 * cv.arcLength(contours[cnt], True)#########3
            approx = cv2.approxPolyDP(contours[cnt], epsilon, True)
            # 分析几何形状
            corners = len(approx)
            shape_type = ""
            if corners == 4:
                count = self.shapes['rectangle']
                count = count + 1
                self.shapes['rectangle'] = count
                shape_type = "矩形"
                # 求解中心位置
                try:
                    mm = cv2.moments(contours[cnt])
                    cx = int(mm['m10'] / mm['m00'])
                    cy = int(mm['m01'] / mm['m00'])
                    cv2.circle(result, (cx, cy), 3, (0, 0, 255), -1)
                    print("x:", cx, "y:", cy)
                    
                    
                except ZeroDivisionError as e:
                    pass
                return 1
                
            if 4 < corners < 10:
                count = self.shapes['polygons']
                count = count + 1
                self.shapes['polygons'] = count
                shape_type = "多边形"
                return 0

            #area = cv.contourArea(contours[cnt])
            # print("形状: %s "% (shape_type))
            
        cv2.imshow('binary',self.draw_text_info(binary))
        cv2.imshow("Analysis Result", self.draw_text_info(target))
        #return self.shapes

    def draw_text_info(self, image):
        c2 = self.shapes['rectangle']
        c3 = self.shapes['polygons']
        cv2.putText(image, "rectangle: " + str(c2), (10, 40), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 0), 1)
        cv2.putText(image, "polygons: " + str(c3), (10, 60), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 0), 1)
        return image

if __name__ == "__main__":
    color='yellow'
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.waitKey(10)
        #print(frame.shape)
        frame= cv2.flip(frame,-1,dst=None) #镜像镜像
        Key = chr(cv2.waitKey(15) & 255)
        if Key == 'q':
            cv2.destroyAllWindows()
            break
        
        ld = ShapeAnalysis()
        ld.analysis(frame,color)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
