# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 08:39:49 2020

@author: wangz
"""

import os
import cv2
import numpy as np


class Face_detector:

    def face_find(self, frame):
        area = 0
        X, Y, W, H = -1, -1, 0, 0  # 左上角坐标和宽、高
        face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
        x, y = frame.shape[0:2]
        # print(middle) # the middle of the Cap equal 160
        small_frame = cv2.resize(frame, (int(y / 2), int(x / 2)))
        result = small_frame.copy()
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            result = cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 2)
            if (w * h > area):
                area = w * h
                X, Y, W, H = (x, y, w, h)
        # cv2.imshow("recognize_face", result)

        # max_index, max_number = max(enumerate(maxtrix), key=operator.itemgetter(1))
        # print(names[max_index])
        cv2.waitKey(20)
        return int(X + W / 2), int(Y + H / 2)


# 主函数
if __name__ == '__main__':

    a = Face_detector()

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        # print(frame.shape)
        frame= cv2.flip(frame,-1,dst=None) #镜像镜像
        Key = chr(cv2.waitKey(15) & 255)
        if Key == 'q':
            cv2.destroyAllWindows()
            break
        x, y = a.face_find(frame)
        print("x:", x, "y:", y)
