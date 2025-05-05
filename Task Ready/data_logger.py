# coding: utf8
import serial
import csv   #CSV dosyaları tıpkı Excel'dekine benzer şekilde tablo formatındaki verileri metin dosyalarında depolamamızı sağlayan bir formattır.
import distance
import task



arduino_port = "PORT" #Arduino port girilecek Arduino ide den alabiliriz 
baud = 115200 #arduino haberleşme hızı, 9600 da olabilir
fileName="Codes/csv_kayıt.csv" #csv dosyasının ismi
try:
    ser = serial.Serial(arduino_port, baud, timeout=2)
    print("Arduino portuna bağlandı: " + arduino_port)
except:
    print("Arduino portuna bağlanamadı: " + arduino_port + " !!!!")


sayi = 50   #veri saklama sayısı sınırlandırıldı
line = 0

sensor_verisi1 = []
sensor_verisi2 = []
sensor_verisi3 = []


while line <= sayi:

    try:
        sensor_verisi1.append(distance.Distance)  ############### mesafe verisi #############
    except:
        print("Mesafe bilgisi alınamadı!!!")
    try:
        sensor_verisi2.append(distance.yukseklik)  ############## ihanın yüksekliği ##############
    except:
        print("Irtifa bilgisi alınamadı!!!")
    try:
        sensor_verisi3.append(task.xlat_xlong)  ############## iki nokta arasındaki mesafe #############
    except:
        print("Iki nokta arasındaki mesafe bilgisi alınamadı!!!")
    

    line = line+1 
with open(fileName, 'w', encoding='utf-8', newline='') as file:
    yaz = csv.writer(file)
    yaz.writerow(["cisim uzaklik:\n",sensor_verisi1])
    yaz.writerow(["iha yukseklik:\n",sensor_verisi2])
    yaz.writerow(["iki nokta arasındaki mesafe:\n",sensor_verisi3])
    print("Tamamlandı")



