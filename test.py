import time
import picamera
from TicTacToe import GetBroadDicAllPath

camera = picamera.PiCamera()
camera.resolution = (3280, 2464)
name=['test1.jpg','test2.jpg','test3.jpg','test4.jpg','test5.jpg','test6.jpg']
if __name__ == '__main__':
    for i in range(6):
        camera.capture(name[i])
        input("按回车拍下一张")
        print("path=",name[i])
        print(GetBroadDicAllPath(name[i]))


