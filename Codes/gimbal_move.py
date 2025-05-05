"""
Aralık bıraktığım alanlar servo kontrolü için, geri kalan kısım normal cisim tanıma ve takip algoritması. 
servoları kanal 7 ve kanal 8 bağlı olduklarını düşünerek hazırladım. Kanal 7 ile sağ-sol haereketini, 
kanal 8 ile yukarı aşağı hareketini sağlamış oldum. servoların nesene sağa veya yukarı ne kadar hareket
ettiyse o kadar hareket etmesi gerekiyor. Yani left-rigt ve up-down değerlerine bakılması gerekebilir. 
kanal 7 
0-90 servo sola
90-180 servo sağa
----------------
kanal 8
0-90 servo yukarı
90-180 servo aşağı
"""

import cv2
import math
from pymavlink import mavutil
from ultralytics import YOLO
import numpy as np

# CUAV X7'e bağlan
iha = mavutil.mavlink_connection("/dev/serial/by-id/usb-ArduPilot_CUAV-X7_320035000751303137343737-if00", baud=57600)
# iha = connect("/dev/serial/by-id/usb-ArduPilot_CUAV-X7_320035000751303137343737-if00", wait_ready=True, timeout = 100)



##############################################################
# Servo hareketi için fonksiyon
def move_gimbal(left_right, up_down):
    # Kanal 7 için servo index
    iha.mav.command_long_send(
        iha.target_system, iha.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        7,  # Kanal 7 
        left_right * 100,  # servo position (0-1000)
        0, 0, 0, 0, 0, 0, 0  # Not used parameters
    )

    # Kanal 8 için servo index'i 
    iha.mav.command_long_send(
        iha.target_system, iha.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        8,  # Kanal 8  
        up_down * 100,  # servo position (0-1000)
        0, 0, 0, 0, 0, 0, 0  # Not used parameters
    )

##############################################################


video_path = "car_video.mp4"
model_path = "best.pt"

cap = cv2.VideoCapture(video_path)
model = YOLO(model_path)

_, frame = cap.read()
width = int(cap.get(3))  # kamera pikselleri
height = int(cap.get(4))
print(width, height)




##############################################################

left_right = 90  # sola-sağa yönde başlangıç açısı
up_down = 90  # yukarı-aşağı yönde başlangıç açısı

##############################################################



while True:
    success, frame = cap.read()
    
    if(success):
        frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
        results = model.track(frame,  persist = True, verbose=False)[0] # model içindeki takip modunu çalıştır.persist takibe aldığı nesne 
                                                                        # kaybolup yeniden gözüktüğünde takibe devam etmesi için,
                                                                        # verbose modelin tespitini terminalde göstermesin diye False yapılır
                                                                        # 0 ıncı index deki veriler bizim için anlamlı
        
        bboxes = np.array(results.boxes.data.tolist(), dtype="int") # xyxy değerlerini yani kutunun sol üst köşe ve sağ alt köşesini dönderiyor
        
        for box in bboxes:
            
            x, y, x1, y1, _, _, _ = box
            w = x1-x
            h = y1-y 
            cx, cy = x + w // 2, y + h // 2
            cv2.circle(frame, (cx, cy), 5, (255, 0, 255), -1)

            cx2, cy2 = 1280 // 2, 720 // 2
            cv2.circle(frame, (cx2, cy2), 5, (255, 0, 255), -1)

            cv2.line(frame, (cx2, cy2), (cx, cy), (255, 0, 0), 1)

            s = round(math.sqrt(math.pow(cx2 - cx, 2) + math.pow(cy2 - cy, 2)), 2)
            cv2.putText(frame, f"Mesafe : {s}", (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))

            if cx <= 640 and cy <= 360:
                text = "Left-Up"
            elif cx <= 640 and cy > 360:
                text = "Left-Down"
            elif cx > 640 and cy <= 360:
                text = "Right-Up"
            elif cx > 640 and cy > 360:
                text = "Right-Down"
            else:
                text = "Tespit Edilemedi"

            cv2.putText(frame, f"Bilgi : {text}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))

            

            ##############################################################

            # Servo hareketini hesapla
            left_right += int((cx - cx2) / 10)
            up_down += int((cy - cy2) / 10)
            left_right = abs(left_right)
            up_down = abs(up_down)
            print("1.", up_down, left_right)

            # Servo sınırlarını kontrol et
            left_right = max(0, min(180, left_right))
            up_down = max(0, min(180, up_down))
            print("2.", up_down, left_right)

            # Servo hareketini gerçekleştir
            move_gimbal(left_right, up_down)

            ##############################################################



        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print("Okuma Hatası")
        break

cap.release()
cv2.destroyAllWindows()

