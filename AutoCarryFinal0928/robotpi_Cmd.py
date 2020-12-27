
class UPComBotCommand(object):
    def Command(self, angle=0, speed=0, turn=0, time=500):
        
        data = [0]*8
        data[0] = angle&0xFF
        data[1] = (angle>>8)&0xFF
        data[2] = speed&0xFF
        data[3] = (speed>>8)&0xFF
        data[4] = turn&0xFF
        data[5] = (turn>>8)&0xFF
        data[6] = time&0xFF
        data[7] = (time>>8)&0xFF
        buffer, length = self.GenerateCmd(0x08, 0x02, 0x08, data)
            
        return buffer

    def GenerateCmd(self, device, cmd, len, data):
        buffer = [0]*(len+6)
        buffer[0] = 0xF5
        buffer[1] = 0x5F
        buffer[2] = device & 0xFF
        check = buffer[2]
        buffer[3] = cmd & 0xFF
        check = check+buffer[3]
        buffer[4] = len & 0xFF
        check = check+buffer[4]
        for i in range(len):
            buffer[5+i] = data[i]
            check = check+buffer[5+i]
        buffer[len+5] = (~check) & 0xFF
        return buffer, len+6

    def wave_hands(self):
        data = [0] * 1
        data[0] = 2 & 0xFF

        buffer, length = self.GenerateCmd(0x07, 0x55, 0x01, data)
        return buffer

    def hit(self):
        data = [0] * 1
        data[0] = 4 & 0xFF

        buffer, length = self.GenerateCmd(0x07, 0x55, 0x01, data)
        print(type(buffer))
        return buffer

    def call_action_by_name(self, name):
        length = len(name.encode())
        # data = name.encode()
        data = [0] * 5
        data[0] = 4 & 0xFF
        data[1] = 3000 & 0xFF
        data[2] = (3000 << 8) & 0xFF
        data[3] = 500 & 0xFF
        data[4] = (500 << 8) & 0xFF
        buffer, length = self.GenerateCmd(0x07, 0x5c, 0x05, data)
        return buffer

    def check_operation(self, data):
        l = len(data)
        check = data[2]
        check = check+data[3]
        check = check+data[4]
        for i in range(data[4]-1):
        
            check = check+data[5+i]
        print("data calculated:", data[l-1])
        if data[l-1] == (~check) & 0xFF:
            print("OK")
            return True
        else:
            return False
    
    
if __name__ == '__main__':
    up = UPComBotCommand()
    up.wave_hands()
    up.call_action_by_name('hold')
