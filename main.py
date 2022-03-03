from time import sleep

import cv2
import cvpackage
from cvpackage import HandDetectionModule
import serial

# reading webcam
cam = cv2.VideoCapture(0)
# hand detector object
detector = HandDetectionModule.MbHandDetector(
    iMaxHands=1,
    iMinDetectionCon=0.5
)
# creating arduino detector to send data to arduino
arduinoDetector = serial.Serial("COM4", baudrate=9600, timeout=2)
data = ""
send = False
on = False
off = True

while cam.isOpened():
    success, images = cam.read()
    if success:
        lmList = detector.findCoordinates(inputImage=images)
        images = detector.detectHands(inputImage=images, draw=True)

        # drawing button on screen
        cv2.rectangle(images, (10, 10), (100, 80), color=(255, 0, 0), thickness=cv2.FILLED)
        cv2.putText(images, "OFF", (25, 50), fontFace=cv2.FONT_ITALIC, fontScale=1, thickness=2, color=(0, 0, 0))

        if lmList:
            if 10 < lmList[8][0] < 100 and 10 < lmList[8][1] < 80:

                if off:
                    if send:
                        send = False
                    data = "on"
                    if not send:
                        send = True
                        arduinoDetector.write(data.encode("utf-8"))
                    sleep(0.6)
                    on = True
                    off = False
                elif on:
                    if send:
                        send = False
                    data = "off"
                    if not send:
                        send = True
                        arduinoDetector.write(data.encode("utf-8"))
                    sleep(0.6)
                    off = True
                    on = False


    cv2.imshow("Output", images)
    if cv2.waitKey(1) & 0XFF == ord("c"):
        break

cam.release()
# cv2.destroyWindow("Output")
