'''
与arduino建立通讯
'''
import time
import serial
import serial.tools.list_ports
import numpy as np
class SerialArduino():
    def __init__(self,port,Baudrate=9600):
        self.port=port
        self.Baudrate=Baudrate
    def GetAllPort(self):
        port_list = []
        for port in list(serial.tools.list_ports.comports()):
            port_list.append(port[0])
        return port_list
    def IsPortExit(self,port):
        port_list = self.GetAllPort()
        if port in port_list:
            return True
        else:
            return False
    def ConnectArduino(self):
        Flag=False
        if self.IsPortExit(self.port):
            try:
                ser = serial.Serial(self.port,self.Baudrate, timeout=1)
                Flag = True
            except:
                Flag=False
        else:
            Flag=False
        if Flag:
            return ser
        else:
            print("未能成功链接Arduino端口，请检查1端口是否存在，2端口是否被占用")
            return Flag
    def SendByteToArduino(self,str1):
        con = self.ConnectArduino()
        SendFlag=False
        RecvFlag=False
        if con:
            s="<%s>\n"%str1
            con.write(s.encode('utf-8'))
            SendFlag = True
            time.sleep(0.5)
            str = con.read_all()
            str1 = str.decode("utf-8")
            if "ok" in str1:
                RecvFlag=True
                print("发送成功")
            print(str1)
        if not RecvFlag:
            print("发送成功，但未接收到反馈信息，请检查Arduino板Mode")
        return SendFlag
if __name__ == '__main__':
    ser=SerialArduino(port='/dev/cu.wchusbserial1410')
    ser.SendByteToArduino(1)

    # ser= ConnectArduino('/dev/cu.wchusbserial1410', 9600)
    # ser = ConnectArduino('/dev/cu.wchusbserial1410', 9600)
    # if ser:
    #     ser.write(b"<aa>\n")
    #     time.sleep(1)
    #     str=ser.read_all()
    #     str1=str.decode("utf-8")
    #     print(str)
    #     print(str1)
    #     ser.write(b"<aa>\n")
    #     time.sleep(1)
    #     str = ser.read_all()
    #     str1 = str.decode("utf-8")
    #     print(str)
    #     print(str1)


    # except SerialException as e:
    #
    # while 1:
    #     ser.write(b"<aa>\n")
    #     time.sleep(1)
    #     str=ser.read_all()
    #     str1=str.decode("utf-8")
    #     print(str)
    #     print(str1)

