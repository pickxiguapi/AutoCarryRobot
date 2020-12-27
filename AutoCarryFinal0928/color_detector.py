# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 19:16:32 2020

@author: wangz
"""
# -*- coding:utf-8 -*-

import cv2
import numpy as np


# 返回识别的最大面积的中心点
class ColorBounding:
    def __init__(self):

        self.ball_color = 'red'
        self.color_dist = {'red': {'Lower': np.array([3, 43, 46]), 'Upper': np.array([10, 255, 255])},
                           'yellow': {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])},
                           'green': {'Lower': np.array([35, 43, 46]), 'Upper': np.array([77, 255, 255])},
                           'black': {'Lower': np.array([0, 0, 0]), 'Upper': np.array([180, 255, 50])},
                           }
        '''
        HSV模型中颜色的参数分别是：色调（H），饱和度（S），明度（V）
        下面两个值是要识别的颜色范围
        '''
        self.kernel_2 = np.ones((2, 2), np.uint8)  # 2x2的卷积核
        self.kernel_3 = np.ones((3, 3), np.uint8)  # 3x3的卷积核
        self.kernel_4 = np.ones((3, 5), np.uint8)  # 4x4的卷积核

        self.red_area = 0

    def bounding(self, Img, color):

        self.ball_color = color
        if Img is not None:  # 判断图片是否读入
            # gs_frame = cv2.GaussianBlur(binary, (5, 5), 0)              # 高斯模糊
            hsv = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式
            erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀,膨胀

            inRange_hsv = cv2.inRange(erode_hsv, self.color_dist[self.ball_color]['Lower'],
                                      self.color_dist[self.ball_color]['Upper'])
            # 转化为hsv格式,提取颜色区域,在颜色范围内的区域变成白色，其他区域变成黑色
            # 下面四行是用卷积进行滤波
            erosion = cv2.erode(inRange_hsv, self.kernel_4, iterations=3)
            erosion = cv2.erode(erosion, self.kernel_4, iterations=1)
            dilation = cv2.dilate(erosion, self.kernel_4, iterations=1)
            dilation = cv2.dilate(dilation, self.kernel_4, iterations=1)
            # target是把原图中的非目标颜色区域去掉剩下的图像
            target = cv2.bitwise_and(Img, Img, mask=dilation)
            # contours,hierarchy = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # 提取轮廓边界

            # 将滤波后的图像变成二值图像放在binary中
            ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
            # 在binary中发现轮廓，轮廓按照面积从小到大排列
            binary, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            p = 0
            x, y, w, h = 0, 0, 0, 0
            X, Y, W, H = 0, 0, 0, 0  # 左上角坐标和宽、高
            area_max = 0
            # 初始化红色面积
            self.red_area = 0
            for i in contours:  # 遍历所有的轮廓
                area = cv2.contourArea(i)

                # 红色面积总和
                # self.red_area += area

                if (area > area_max):
                    area_max = area
                    x, y, w, h = cv2.boundingRect(i)  # 保存最大面积的坐标
                self.red_area = area_max
                '''
                x,y,w,h = cv2.boundingRect(i)#将轮廓分解为识别对象的左上角坐标和宽、高
                X,Y,W,H= cv2.boundingRect(i)#保存最大面积的坐标
                #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
                cv2.rectangle(Img,(x,y),(x+w,y+h),(0,255,),3)
                #给识别对象写上标号
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(Img,str(p),(x-10,y+10), font, 1,(0,0,255),2)#加减10是调整字符位置
                '''
                p += 1

            cv2.rectangle(Img, (x, y), (x + w, y + h), (0, 255,), 3)
            # 给识别对象写上标号
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(Img, str(p), (x - 10, y + 10), font, 1, (0, 0, 255), 2)  # 加减10是调整字符位置
            # print('目标数量是', p, '个')  # 终端输出目标数量
            # cv2.imshow('target', target)
            cv2.imshow('Img', Img)
            # cv2.imwrite('Img.png', Img)#将画上矩形的图形保存到当前目录
            if x != 0 and self.red_area>100:
                return int(x + w / 2), int(y + h / 2)
            else:
                return -1, -1


if __name__ == '__main__':
    b = ColorBounding()
    cap = cv2.VideoCapture(0)
    color = 'black'
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 0, dst=None)  # 垂直镜像
        Key = chr(cv2.waitKey(15) & 255)
        if Key == 'q':
            cv2.destroyAllWindows()
            break
        # frame = cv2.medianBlur(frame,7)
        x, y = b.bounding(frame, color)
        print("x:", x, "y:", y)
