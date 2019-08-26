import time
import picamera
from TicTacToe import GetBroadDicAllPath

imgname=['pic1.jpg','pic2.jpg','pic3.jpg','pic4.jpg','pic5.jpg','pic6.jpg','pic7.jpg','pic8.jpg','pic9.jpg']

def SaveCameraPic(num):
    with picamera.PiCamera() as camera:
        camera.resolution = (3280, 2464)
        path=imgname[num]
        FlagSave=False
        try:
            camera.capture(path)
            print("保存成功，位置：",path)
            FlagSave=True
        except:
            print("保存失败，位置：", path)
        return FlagSave,path
if __name__ == '__main__':
    for i in range(5):
        print("第%s次采集"%str(i))
        name="image"+str(i)
        Flag,path=SaveCameraPic(i)
        time.sleep(1)
        if Flag:
            print(GetBroadDicAllPath(path))
            time.sleep(1)