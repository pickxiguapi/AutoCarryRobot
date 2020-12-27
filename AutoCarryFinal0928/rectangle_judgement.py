# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 14:58:10 2020

@author: zgzaacm
"""
import time
import cv2
import numpy as np

class ShapeAnalysis:
    def __init__(self):
        self.shapes = 0

    def analysis(self, frame, opt):
        h, w, ch = frame.shape
        result = np.zeros((h, w, ch), dtype=np.uint8)
        # 二值化图像
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if opt ==1:  # red
            lower_hsv = np.array([160, 100, 100])
            upper_hsv = np.array([180, 255, 255])
            mask1 = cv2.inRange(hsv, lower_hsv, upper_hsv)
            lower_hsv = np.array([0, 100, 100])
            upper_hsv = np.array([10, 255, 255])
            mask2 = cv2.inRange(hsv, lower_hsv, upper_hsv)
            binary = mask1 | mask2
        elif opt==2:  # yellow
            lower_hsv = np.array([26, 100, 100])
            upper_hsv = np.array([34, 255, 255])
            binary = cv2.inRange(hsv, lower_hsv, upper_hsv)
        elif opt==3:  # green
            lower_hsv = np.array([35, 100, 100])
            upper_hsv = np.array([77, 255, 255])
            binary = cv2.inRange(hsv, lower_hsv, upper_hsv)

        binary_1, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in range(len(contours)):
            # 提取与绘制轮廓
            cv2.drawContours(result, contours, cnt, (0, 255, 0), 2)

            # 轮廓逼近
            epsilon = 15
            approx = cv2.approxPolyDP(contours[cnt], epsilon, True)

            # 分析几何形状
            corners = len(approx)
            shape_type = ""
            if corners == 3:
                self.shapes = 0
            if corners == 4:
                self.shapes = 1
            if corners >= 10:
                self.shapes = 0
            if 4 < corners < 10:
                self.shapes = 0
        cv2.imshow("Analysis Result", binary)
        return self.shapes



if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    ld = ShapeAnalysis()
    i = 1
    while (i < 51):  # 读取50张图片
        time.sleep(1)
        
        j=0
        while j < 10:
            ret, frame =cap.read()
            j+=1
        
        ret, frame = cap.read()
        frame = cv2.flip(frame, -1)
        print(ld.analysis(frame,3))
        cv2.imshow('frame', frame)
        cv2.waitKey(100)
        # 最小外接矩形的中心（x，y），（宽度，高度），旋转角度）
        i = i + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
