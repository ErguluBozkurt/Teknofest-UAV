# coding: utf-8
import cv2
import numpy as np
from ultralytics import YOLO

class DistanceCalculator:
    def __init__(self, iha):
        # İHA nesnesini sakla
        self.iha = iha
        
        # Nesnenin bilinen özellikleri
        self.KNOWN_DISTANCE = 0.762  # metre
        self.KNOWN_WIDTH = 0.143     # metre (nesnenin gerçek genişliği)
        
        # Fiziksel parametreler (İHA'dan alınacak)
        self.h = 50  # m yükseklik (default değer)
        self.g = 9.81  # yer çekimi
        self.k = 0.32  # hava sürtünme katsayısı
        self.r = 0.036  # m cinsinden yarıçap (3.6 cm)
        self.m = 0.7  # kg (default değer)
        
        # Renk tanımları
        self.GREEN = (0, 255, 0)
        self.RED = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONTS = cv2.FONT_HERSHEY_COMPLEX
        
        # Model yükleme
        self.model = YOLO("best.pt")
        self.FOCAL_LENGTH = self.calibrate_camera()

    def update_iha_parameters(self):
        """İHA'dan güncel parametreleri al"""
        try:
            # İHA'nın mevcut irtifasını al
            self.h = self.iha.location.global_relative_frame.alt
            
            # İHA'nın mevcut hızını al (m/s)
            self.Vx = self.iha.airspeed if self.iha.airspeed is not None else 9  # m/s default
            
            # Rüzgar hızı için (gerçek uygulamada daha karmaşık hesaplama gerekebilir)
            self.WIND_V = 5  # m/s (default)
            
            # Hedef hızı (sabit varsayıyoruz)
            self.Vc = 5  # m/s
            
        except Exception as e:
            print(f"İHA parametreleri alınırken hata: {e}")
            # Hata durumunda default değerleri kullanmaya devam et

    def calibrate_camera(self):
        # Kalibrasyon için referans görüntü
        ref_image_path = "ref.jpg"
        ref_image = cv2.imread(ref_image_path)
        ref_width = self.get_object_width(ref_image, class_name="target")
        
        if ref_width == 0:
            raise Exception("Hata: Referans görüntüde hedef nesne bulunamadı!")
        
        focal_length = self.focal_length_finder(self.KNOWN_DISTANCE, self.KNOWN_WIDTH, ref_width)
        print(f"Bulunan Fokal Uzunluk: {focal_length}")
        return focal_length

    def focal_length_finder(self, measured_distance, real_width, width_in_rf_image):
        return (width_in_rf_image * measured_distance) / real_width

    def distance_finder(self, object_width_in_frame):
        if object_width_in_frame == 0:
            return 0
        return (self.KNOWN_WIDTH * self.FOCAL_LENGTH) / object_width_in_frame

    def get_object_width(self, image, class_name="target"):
        results = self.model(image)[0]
        for box in results.boxes:
            cls = int(box.cls[0])
            label = self.model.names[cls]
            if label == class_name:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(image, (x1, y1), (x2, y2), self.GREEN, 2)
                return x2 - x1  # nesnenin piksel cinsinden genişliği
        return 0

    def shoot_decision(self, distance):
        # Önce İHA parametrelerini güncelle
        self.update_iha_parameters()
        
        # Fiziksel hesaplamalar
        A = round(np.pi * (self.r ** 2), 5)
        t = round(np.sqrt((2 * self.h) / self.g), 3)
        Vy = round(self.g * t, 3)

        fs1 = round(self.k * A * (Vy ** 2), 3)
        fs1 = round((fs1 - (self.m * self.g)), 3)
        a1 = round(fs1 / self.m, 3)
        Vy_net = round(Vy - (-a1 * t) - self.WIND_V, 3)
        t_net = round(Vy_net / self.g, 3)

        fs2 = round(self.k * A * (self.Vx ** 2), 3)
        a2 = round(fs2 / self.m, 3)
        Vx_net = round(self.Vx - (a2 * t), 3)

        x1 = round(Vx_net * t_net, 3)
        x2 = round(self.Vc * t_net, 3)
        X = x1 - x2

        diff = round(X - distance, 2)
        print(f"Atış Mesafesi ile Hedef Arası Fark: {diff} m")
        print(f"İHA Parametreleri - İrtifa: {self.h}m, Hız: {self.Vx}m/s, Rüzgar: {self.WIND_V}m/s")
        
        if -2.5 < diff < 2.5:
            return True, "🎯 Atış yapılabilir!"
        else:
            return False, "🚫 Atış yapılmaz, hedef menzilde değil."

    def process_frame(self, frame):
        width_in_frame = self.get_object_width(frame, class_name="target")
        distance = 0
        decision = ""
        can_shoot = False
        
        if width_in_frame != 0:
            distance = self.distance_finder(width_in_frame)
            distance = round(distance, 2)
            
            # Mesafe bilgisini ekrana yaz
            cv2.line(frame, (30, 30), (300, 30), self.RED, 32)
            cv2.line(frame, (30, 30), (300, 30), self.BLACK, 28)
            cv2.putText(frame, f"Mesafe: {distance} m", (30, 35), self.FONTS, 0.6, self.WHITE, 1)
            
            # Atış kararını al ve ekrana yaz
            can_shoot, decision = self.shoot_decision(distance)
            cv2.putText(frame, decision, (30, 70), self.FONTS, 0.6, self.WHITE, 1)

        return frame, distance, can_shoot, decision

def init_distance(iha):
    """İHA nesnesi ile DistanceCalculator'ı başlat"""
    global distance_calculator
    distance_calculator = DistanceCalculator(iha)

def distance():
    """Generator fonksiyonu olarak mesafe bilgisini üretir"""
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame, current_distance, can_shoot, decision = distance_calculator.process_frame(frame)
            
            cv2.imshow("Nesne Tespiti ve Mesafe Hesaplama", processed_frame)
            
            if cv2.waitKey(1) == ord("q"):
                break
                
            yield current_distance, can_shoot, decision
            
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test için
    class MockIHA:
        def __init__(self):
            self.location = type('', (), {})()
            self.location.global_relative_frame = type('', (), {'alt': 50})()
            self.airspeed = 9
            
    mock_iha = MockIHA()
    init_distance(mock_iha)
    
    for dist, shootable, msg in distance():
        print(f"Mesafe: {dist}m - {msg}")
