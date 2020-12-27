# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 08:39:49 2020

@author: wangz
"""
from aip import AipFace
import base64
import time
import os
import cv2
import urllib3
import numpy as np 
import urllib.request

urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#将目标图片保存再文件中
class Face_destination():
    def _init_(self):
        self.path=""
    def img_save(self):
        dirname="./dataset/match/"
        face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')  
        if (not os.path.isdir(dirname)):        
            os.makedirs(dirname)     
        cap = cv2.VideoCapture(0)    
        count = 0    
        while True:       
            ret, frame = cap.read() 
            #frame= cv2.flip(frame,-1,dst=None) #翻转镜像
            cv2.imshow('target', frame)
            x, y = frame.shape[0:2]         
            small_frame = cv2.resize(frame, (int(y/2), int(x/2)))         
            result = small_frame.copy()         
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)         
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)         
            for (x, y, w, h) in faces:             
                result = cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 2)            
                f = cv2.resize(gray[y:y+h, x:x+w], (200, 200))               
                if count<20:                 
                    cv2.imwrite(dirname + '%s.png' % str(count), f)       #pgm          
                    print(count)                
                    count += 1                        
            cv2.imshow('face', result)
            cv2.waitKey(10)
            if(count==20):
                break
            
        cap.release()    
        cv2.destroyAllWindows()  
                    
    
#上传目标图片
class api_updata():
    def __init__(self):
        self.APP_ID = '22624110'
        self.API_KEY = 'cswQBIxIV4lGekOxQdLiI9QV'
        self.SECRET_KEY ='8LuO1xtjbgeT6YjkPlTB5nxK3C7P8xSp'
        
        #图像编码方式
        self.IMAGE_TYPE='BASE64'
        #用户组
        self.userId = "1"
        self.groupId = "1"

    def updata(self,face_img_path):
        
        f = open(face_img_path,'rb')
        base_data = base64.b64encode(f.read())
        img = str(base_data,'utf-8')
        options = {}
        options["start"] = 0
        options["length"] = 50
        
        client = AipFace(self.APP_ID, self.API_KEY, self.SECRET_KEY)#创建一个客户端用以访问百度云
        list1 = client.updateUser(img, self.IMAGE_TYPE, self.groupId, self.userId)
        
        """ 调用获取用户人脸列表 """
        #client.getGroupUsers(groupId, options)
        print(list1)
        #return list1
        
#事实显示识别图片
        
class Face_recognize:
    def __init__(self):
        #百度人脸识别API账号信息
        self.APP_ID = '22624110'
        self.API_KEY = 'cswQBIxIV4lGekOxQdLiI9QV'
        self.SECRET_KEY ='8LuO1xtjbgeT6YjkPlTB5nxK3C7P8xSp'
        self.client = AipFace(self.APP_ID, self.API_KEY, self.SECRET_KEY)#创建一个客户端用以访问百度云
        #图像编码方式
        self.IMAGE_TYPE='BASE64'
        #用户组
        self.GROUP = '1'        
        self.array_of_img = [] # 存储图片数据
    
    #读取文件夹中的数据
    def read_directory(self,directory_name):
        for filename in os.listdir(r"./"+directory_name):
            #img is used to store the image data
            result = open(directory_name + "/" + filename,'rb')
            self.array_of_img.append(result)  
            
    #返回分辨的图片
    def photo(self):
        #print(self.array_of_img)
        return self.array_of_img
   
    #对图片的格式进行转换 
    def transimage(self,img):
        img = base64.b64encode(img.read())
        return img
    
    #进行人脸检测
    def go_api(self,image):
        result = self.client.search(str(image, 'utf-8'), self.IMAGE_TYPE, self.GROUP);#在百度云人脸库中寻找有没有匹配的人脸
        if result['error_msg'] == 'SUCCESS':#如果成功了
            name = result['result']['user_list'][0]['user_id']#获取名字
            score = result['result']['user_list'][0]['score']#获取相似度
            #print(score)
            #print('#######')
            if score > 80:#如果相似度大于80
                if name == '1':#第一组第一人图片替换,替换成功
                    #print("欢迎%s !" % name)
                    #time.sleep(3)
                    print('//yes')
                    return score
            else:
                #print("对不起，我不认识你！")
                name = 'Unknow'
                print('##no')
                return score
        '''   
        if result['error_msg'] == 'pic not has face':
            print('检测不到人脸')
            #time.sleep(2)
            return 0
        else:
            return 0  
        '''
    def read_images(self,path, sz=None): 
            c = 0     
            X, y = [], []     
            names = []     
            for dirname, dirnames, filenames in os.walk(path):         
                for subdirname in dirnames:             
                    subject_path = os.path.join(dirname, subdirname)            
                    for filename in os.listdir(subject_path):                 
                        try:                     
                            if (filename == ".directory"):                        
                                continue                     
                            filepath = os.path.join(subject_path, filename)                     
                            im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)   
                            if (im is None):                         
                                print("image" + filepath + "is None")                    
                            if (sz is not None):                         
                                im = cv2.resize(im, sz)                     
                            X.append(np.asarray(im, dtype=np.uint8))                    
                            y.append(c)                
                        except:                     
                            print("unexpected error")                     
                            raise   
                    c = c+1             
                    names.append(subdirname) 
                    
            return [names, X, y , c]
        
    def count_num(self,p_label,maxtrix):
        
        maxtrix[p_label]=maxtrix[p_label]+1
        
        return maxtrix
    
    def face_find(self,frame):
        area=0
        X,Y,W,H=-1,-1,0,0#左上角坐标和宽、高
        face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')                
        x, y = frame.shape[0:2]
        #print(middle) # the middle of the Cap equal 160
        small_frame = cv2.resize(frame, (int(y/2), int(x/2)))         
        result = small_frame.copy()         
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)         
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        for (x, y, w, h) in faces:             
            result = cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 2)   
            if(w*h>area):
                area=w*h
                X,Y,W,H=(x,y,w,h)
        # cv2.imshow("recognize_face", result)

        cv2.waitKey(20)
        #max_index, max_number = max(enumerate(maxtrix), key=operator.itemgetter(1))
        #print(names[max_index])
        return int(X+W/2),int(Y+H/2)
                     
            
    def face_rec(self,frame):           
        dirname="./dataset/1/"
        count=0
        face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')          
        x, y = frame.shape[0:2]
        middle=int(y/4)
        #print(middle) # the middle of the Cap equal 160
        small_frame = cv2.resize(frame, (int(y/2), int(x/2)))         
        result = small_frame.copy()         
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)         
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)         
        for (x, y, w, h) in faces:             
            result = cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 2)   
            #roi = gray[x:x+w, y:y+h]
            roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            #if(abs(middle-int((2*x+w)/2))<=5): # Assuming a certain range in the middle of the image
                #print(int((2*x+w)/2)) #the middle of the face picture
            try:
                #roi = cv2.resize(roi, (300,300), interpolation=cv2.INTER_LINEAR)
                cv2.imshow("face", roi)
                cv2.imwrite(dirname + '%s.png' % str(count), roi)
                self.read_directory("./dataset/1")
                for img in self.array_of_img:
                    img = self.transimage(img)#转换照片格式
                    res = self.go_api(img)#将转换了格式的图片上传到百度云
                    time.sleep(0.5)


                print(res)
                if res>90:
                    cv2.putText(result, 'target', (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
                    return 1,int(x+w/2),int(y+h/2)
                else:
                    cv2.putText(result, 'unknow', (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
                    return 0,-1,-1
                ############
                #cv2.putText(result, names[p_label], (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
                #cv2.putText(result, 'target', (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
            except:
                continue
         
        cv2.imshow("recognize_face", result)               
        return 0,-1,-1
#主函数
if __name__ == '__main__':
    #获得目标图像
    '''
    c=Face_destination()
    c.img_save()
    '''
    
    #上传目标图像
    '''
    face_img_path="./dataset/match/9.png"
    b=api_updata()
    b.updata(face_img_path)
    '''
         
    #识别人物图像
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        #print(frame.shape)
        #frame= cv2.flip(frame,-1,dst=None) #镜像镜像
        Key = chr(cv2.waitKey(15) & 255)
        if Key == 'q':
            cv2.destroyAllWindows()
            break
        
        a=Face_recognize()
        ret,x,y=a.face_rec(frame)
        if (ret==1):
            print("yes","x:", x, "y:", y)
        else:
            print("no","x:", x, "y:", y)
            
        #返回人物图像中心点坐标
       # x, y= a.face_find(frame)
        #print("x:", x, "y:", y)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
