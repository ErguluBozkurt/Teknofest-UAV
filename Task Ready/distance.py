# coding: utf8
import cv2
import numpy as np
import matplotlib.pyplot as plt
import task 


def display(img, cmap='gray'):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)  
    ax.imshow(img, cmap='gray')
    plt.pause(1)

Known_distance = 0.762  #kameradaki uzaklık
Known_width = 0.143  #resimdeki uzaklık metre

GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

fonts = cv2.FONT_HERSHEY_COMPLEX
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
	focal_length = (width_in_rf_image * measured_distance) / real_width   # uzaklık bulma
	return focal_length

def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):  # mesafe tahmin fonksiyonu
	distance = (real_face_width * Focal_Length)/face_width_in_frame
	return distance

def face_data(image):
	face_width = 0 
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # gri ton renk      
	faces = face_detector.detectMultiScale(gray_image, 1.3, 5)  # yüz algılama

	
	
	for (x, y, h, w) in faces:	# x, y  kalınlık ve yükseklik
		cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2)  # yüz içi kare kutucuk
		face_width = w  # yüz genişliği ayarlaması
	return face_width

ref_image = cv2.imread("Codes\WIN_20221127_16_53_15_Pro.jpg")  # resim kaydedilen yerin adresi
ref_image_face_width = face_data(ref_image)
Focal_length_found = Focal_Length_Finder(Known_distance, Known_width, ref_image_face_width)  # Known_distance(meters),
                                                                                             # known_width(meters)
print(Focal_length_found)

cv2.imshow("Kamera", ref_image) #kamerada göster
cap = cv2.VideoCapture(0)

yuz_ismi = 1  # yeni çekilecek kişi için değiştirmememiz gerkli
sayi = 1  # kaç fotoraf çekileceğimimizi saydırmak için 
yukseklik = task.iha.location.global_relative_frame.alt

while True:

	_, frame = cap.read()  #kamera okutuldu
	gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #resim rengi için gri yapıldı  
	yuzler = face_detector.detectMultiScale(gri, 1.3, 5)
    
	face_width_in_frame = face_data(frame)
	if face_width_in_frame != 0:
		Distance = Distance_finder(Focal_length_found, Known_width, face_width_in_frame)    # Known_width(meters)
	                                                                                    	# and Known_distance(meters)
		cv2.line(frame, (30, 30), (230, 30), RED, 32)   # metnin arka planına hat çiz
		cv2.line(frame, (30, 30), (230, 30), BLACK, 28)

		
		cv2.putText(frame, f"Mesafe: {round(Distance,2)} Metre ",  (30, 35),fonts, 0.6, WHITE, 1)  # Ekran üstünde uzaklık gösterimi
  
		
		cv2.line(frame, (620, 30), (390, 30), RED, 32)   # metnin arka planına hat çiz
		cv2.line(frame, (620, 30), (390, 30), BLACK, 28)
		cv2.putText(frame, f"Yukseklik: {round(yukseklik,2)} Metre ",  (390, 35),fonts, 0.6, WHITE, 1) # iha yükseklik ekran da gösterdi
  
	cv2.imshow("Kamera", frame)

	if cv2.waitKey(1) == ord("q"):
		break
	
	

cap.release()
cv2.destroyAllWindows()
