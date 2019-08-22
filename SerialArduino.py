'''
与arduino建立通讯
'''
import time
import serial
import serial.tools.list_ports
import numpy as np
import configparser
class SerialArduino():
    def __init__(self,Baudrate=9600):
        cf = configparser.ConfigParser()
        cf.read("./config.ini")
        Port = cf.get("Setting", "Port")
        self.port=Port
        self.Baudrate=Baudrate
    def GetAllPort(self):
        port_list = []
        for port in list(serial.tools.list_ports.comports()):
            port_list.append(port[0])
        return port_list
    def IsPortExit(self):
        port_list = self.GetAllPort()
        if self.port in port_list:
            return True
        else:
            return False
    def ConnectArduino(self):
        Flag=False
        if self.IsPortExit():
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
    ser = SerialArduino()
    ser.SendByteToArduino(1)

