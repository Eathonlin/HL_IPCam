
# coding: utf-8

# In[ ]:


import cv2
import time
import threading
import face_recognition
import numpy as np

# 接收攝影機串流影像，採用多執行緒的方式，降低緩衝區堆疊圖幀的問題。
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False

    # 攝影機連接。
        self.capture = cv2.VideoCapture(URL)

    def start(self):
    # 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('ipcam 連線成功!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
    # 記得要設計停止無限迴圈的開關。
        self.isstop = True
        print('ipcam 連線關閉!')
   
    def getframe(self):
    # 當有需要影像時，再回傳最新的影像。
        return self.Frame
        
    def queryframe(self):
        
        Imagelist = list(np.load('ImageList.npy'))
        Namelist = list(np.load('NameList.npy'))
        
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()
            
            face_locations = face_recognition.face_locations(self.Frame)
            face_encodings = face_recognition.face_encodings(self.Frame, face_locations)
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                #for i,v in enumerate(All_face_encoding):
                for i,v in enumerate(Imagelist):
                    match = face_recognition.compare_faces([v], face_encoding,tolerance=0.5)
                    #print(match)
                    name = "Unknown"
                    if match[0]:
                        #name = All_image_name[i]
                        name = Namelist[i]
                        break
                cv2.rectangle(self.Frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(self.Frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.Frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.imshow('ShowIPCam', self.Frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                ipcam.stop()
                break 
            
        
        self.capture.release()
        


        
URL = "rtsp://ID:password@192.168.10.199:88/videoMain"



# 連接攝影機
ipcam = ipcamCapture(URL)
#video_capture = cv2.VideoCapture(URL)


# 啟動子執行緒
ipcam.start()

# 暫停0.5秒，確保影像已經填充
time.sleep(0.5)


 #使用無窮迴圈擷取影像，直到按下Esc鍵結束
while True:
     #使用 getframe 取得最新的影像
    I = ipcam.getframe()

    #cv2.imshow("capture",I)
    #if cv2.waitKey(1000) == 27:
    #if cv2.waitKey(1) & 0xFF == ord('q'):   
        #ipcam.stop()
        #break     
video_capture.release()
cv2.destroyAllWindows()

