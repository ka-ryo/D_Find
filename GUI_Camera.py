import eel
import numpy as np
import time
import base64

import cv2 as cv
import sys


cap = None
frame = None

def onCloseWindow(page, sockets):
    global cap
    cv.destroyAllWindows()
    cap.release()
     
    

@eel.expose
def Save_Room_pic():
    global frame
    cv.imwrite('room.jpg',frame)

def main():
    global cap
    global frame
    eel.init("web/html")

    cap = cv.VideoCapture(0)

    #web_app_options = {"chromeFlags": ["--window-size=420,200"]}
    eel.start('camera.html',
            mode='chrome',
            cmdline_args=['--start-fullscreen'],
            block=False,
            port = 0,
            close_callback=onCloseWindow,
            size=(1080, 700))



    while True:
            start_time = time.time()

            eel.sleep(0.01)

            # カメラキャプチャ #####################################################
            ret, frame = cap.read()
            if not ret:
                continue

            # UI側へ転送(画像) #####################################################
            _, imencode_image = cv.imencode('.jpg', frame)
            base64_image = base64.b64encode(imencode_image)
            eel.set_base64image("data:image/jpg;base64," + base64_image.decode("ascii"))

            key = cv.waitKey(1)
            if key == 27:  # ESC
                break

            # UI側へ転送(処理時間) #################################################
            #elapsed_time = round((time.time() - start_time), 3)
            #eel.set_elapsedtime(elapsed_time)


if __name__ == '__main__':
    main()