import cv2
import time
import numpy as np
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, hCam)
cap.set(4, wCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.8)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
print(volume.GetVolumRange())
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 9, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 9, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2,y2), (255,0,255), 2)
        cv2.circle(img, (cx, cy), 9, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        print(length)
        if length < 40:
            cv2.circle(img, (cx, cy), 9, (0, 255, 255), cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    cv2.imshow("img", img)
    cv2.waitKey(1)