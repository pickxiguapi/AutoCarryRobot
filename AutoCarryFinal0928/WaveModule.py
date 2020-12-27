from robotpi_Cmd import UPComBotCommand
from robotpi_serOp import serOp
import time


class Wave(object):
    def __init__(self):
        self.ser = serOp()

    def getWaveData(self):
        data = list()
        distance = 0
        while True:
            recv_data = self.ser.serial_listen()
            # print('recv_data: ', recv_data)
            # 200:start 201:end
            for i in recv_data[-7:]:
                data.append(i)
            # print('data: ', data)
            if len(data) >= 7:
                for j in range(len(data)):
                    if data[j] == 200:
                        distance = data[j+1] * 100 + data[j+2]
                        data.clear()
                        print(distance)
                        return distance
                        
        

if __name__ == '__main__':
    w = Wave()
    mv = Movement()
    mv.move_forward()
    w.getWaveData()
        # time.sleep(1)



