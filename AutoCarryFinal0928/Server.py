#!/usr/bin/python
# coding=utf-8
import socket
import time
import sys

import cv2

HOST_IP = ""    # 树莓派作为AP热点的ip地址，默认""
HOST_PORT = 8999           # 端口号
from Movement import Movement


class TcpConnect(object):
    # 定义公开属性
    recv_data = ''
    send_data = ''

    def __init__(self, host_ip, host_port):
        self.flag = False
        self.host_ip = host_ip
        self.host_port = host_port
        self.mv = Movement()
        self.color = 'red'

    # 返回本机IP地址，用于连接
    def get_my_ip(self):
        my_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))  # 获取本机IP地址
        print(my_ip)  # 调试用
        return my_ip

    def create_connect(self):
        self.flag = True

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立socket，参数为ipv4，TCP，另一个参数默认为1.
        server_sock.bind((self.host_ip, self.host_port))
        server_sock.listen(1)
        buffer = 1024
        print('服务器已经就绪......')

        cap = cv2.VideoCapture(0)

        try:
            while True:
                # 循环接受客户端的连接请求
                print('waiting for connection...')
                socket_con, (client_ip, client_port) = server_sock.accept()
                print("Connection accepted from %s." % client_ip)
                self.flag = True
                self.mv.robotModeSet()
                while True:
                    # 循环接收客户端发送的消息
                    client_msg = socket_con.recv(buffer)


                    if client_msg:
                        print(client_msg)
                        client_msg = client_msg.decode()
                        self.mv.control_movement(client_msg)
                    else:
                        # 当接受到的clientMsg为空就跳出循环，出现过卡死状态
                        continue
        except:
            print('连接错误......')
            cv2.destroyAllWindows()
        server_sock.close()


tcp = TcpConnect(HOST_IP, HOST_PORT)
tcp.get_my_ip()
tcp.create_connect()


