import cv2
import numpy as np
import torch
from ultralytics import YOLO

# Nesnenin bilinen özellikleri
KNOWN_DISTANCE = 0.762  # metre
KNOWN_WIDTH = 0.143     # metre (nesnenin gerçek genişliği)

# Fiziksel parametreler
h = 50  # m yükseklik
g = 9.81  # yer çekimi
k = 0.32  # hava sürtünme katsayısı
r = 0.036  # m cinsinden yarıçap (3.6 cm)
m = 0.7  # kg
Vx = 9  # m/s uçak hızı
Vc = 5  # m/s hedef hızı
WIND_V = 5  # m/s rüzgar

# Renk tanımları
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONTS = cv2.FONT_HERSHEY_COMPLEX

# Model yükleme
model = YOLO("best.pt")

# Fokal uzunluk hesaplayıcı
def focal_length_finder(measured_distance, real_width, width_in_rf_image):
    return (width_in_rf_image * measured_distance) / real_width

# Mesafe hesaplayıcı
def distance_finder(focal_length, real_object_width, object_width_in_frame):
    if object_width_in_frame == 0:
        return 0
    return (real_object_width * focal_length) / object_width_in_frame

# Görüntüde nesnenin genişliğini tespit et
def get_object_width(image, class_name="target"):
    results = model(image)[0]
    for box in results.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]
        if label == class_name:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), GREEN, 2)
            return x2 - x1  # nesnenin piksel cinsinden genişliği
    return 0

# Atış kararı fonksiyonu
def shoot(distance):
    A = round(np.pi * (r ** 2), 5)
    t = round(np.sqrt((2 * h) / g), 3)
    Vy = round(g * t, 3)

    fs1 = round(k * A * (Vy ** 2), 3)
    fs1 = round((fs1 - (m * g)), 3)
    a1 = round(fs1 / m, 3)
    Vy_net = round(Vy - (-a1 * t) - WIND_V, 3)
    t_net = round(Vy_net / g, 3)

    fs2 = round(k * A * (Vx ** 2), 3)
    a2 = round(fs2 / m, 3)
    Vx_net = round(Vx - (a2 * t), 3)

    x1 = round(Vx_net * t_net, 3)
    x2 = round(Vc * t_net, 3)
    X = x1 - x2

    diff = round(X - distance, 2)
    print(f"Atış Mesafesi ile Hedef Arası Fark: {diff} m")
    
    if -2.5 < diff < 2.5:
        return "🎯 Atış yapılabilir!"
    else:
        return "🚫 Atış yapılmaz, hedef menzilde değil."

# Kalibrasyon için referans görüntü
ref_image_path = "ref.jpg"
ref_image = cv2.imread(ref_image_path)
ref_width = get_object_width(ref_image, class_name="target")

if ref_width == 0:
    print("Hata: Referans görüntüde hedef nesne bulunamadı!")
    exit()

FOCAL_LENGTH = focal_length_finder(KNOWN_DISTANCE, KNOWN_WIDTH, ref_width)
print(f"Bulunan Fokal Uzunluk: {FOCAL_LENGTH}")

# Kamera aç
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    width_in_frame = get_object_width(frame, class_name="target")
    
    if width_in_frame != 0:
        distance = distance_finder(FOCAL_LENGTH, KNOWN_WIDTH, width_in_frame)
        distance = round(distance, 2)
        
        # Mesafe bilgisini ekrana yaz
        cv2.line(frame, (30, 30), (300, 30), RED, 32)
        cv2.line(frame, (30, 30), (300, 30), BLACK, 28)
        cv2.putText(frame, f"Mesafe: {distance} m", (30, 35), FONTS, 0.6, WHITE, 1)
        
        # Atış kararını al ve ekrana yaz
        decision = shoot(distance)
        cv2.putText(frame, decision, (30, 70), FONTS, 0.6, WHITE, 1)

    cv2.imshow("Kamera", frame)
    
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
