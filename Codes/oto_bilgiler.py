from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

drone = connect("127.0.0.1:14550", wait_ready=True) #bağlanana kadar deneme yapar

print(f"Drone armed modu {drone.armed}")   #drone un arm edilip edilmediğini bildir
print(f"enlem, boylam ve irtifa bilgisi bulunduğu yükseklik için {drone.location.global_relative_frame} ")
print(f"sadece irtifa {drone.location.global_relative_frame.alt}")
#iha.location.global_relative_frame.lat    enlem boylam
#iha.location.global_relative_frame.lon

def takeoff(irtifa):
    while drone.is_armable is not True:
        print("İHA arm edilebilir durumda değil.")
        time.sleep(1)


    print("İHA arm edilebilir.")  #arm edilip edilmediğini kontrol ediyor

    drone.mode = VehicleMode("GUIDED")

    drone.armed = True

    while drone.armed is not True:
        print("İHA arm ediliyor...")
        time.sleep(2)

    print("İHA arm edildi.")

    drone.simple_takeoff(irtifa)
    
    while drone.location.global_relative_frame.alt < irtifa * 0.9:   #Hedefe yükselene kadar bekliyor
        print("İha hedefe yükseliyor.")
        time.sleep(1)
        
#with open("Codes\mesafe.rtf", "r", encoding="utf-8") as file:
#    Distance = file.read()
#if(Distance>0): komutların altında hedefi tespit ettiğinde fonksiyonu çağırarak işlemi başlatır.
"""
def atis():
    
	yukseklik = iha.location.global_relative_frame.alt
	yatay_uzaklık = math.sqrt((Distance**2)-(yukseklik**2))
	hız = iha.vehicle.airspeed
	zaman1 = math.sqrt((2*yukseklik)/9.81)
	zaman2 = (yatay_uzaklık/hız)
	if(zaman1==zaman2):
		print("Atış yapıldı")
"""

"""
if(input("hangi konumu değişmek istermisiniz(y/n)=")=="y"):
		n = int(input("kaçıncı konuma gitsin =")) 
		next_waypoint = komut.n

"""


def task():
    global command
    command = drone.commands
        
    command.clear()  #drone a verilmiş bir görev var ise siler.
    time.sleep(2)
        
        #TAKAOFF
    command.add(Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATİVE_ALT,mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,0,0,0,0,0,0,10 ))  
        #1. parametre her zaman aynıdır. 2. parametre dronda ek cihaz varsa onun kontrolü için belirmesi gerekir.
        #  3. parametre hangi komutun kaçıncı sırada çalışması gerektiğini belirmek için kullanılır 0 verirsek ilk gelen komutta göre kendi sıraya dizer.
        #5. parametre görev parametresi drone a yapmak istediğimiz kodu yaziyoruz.
        # görev parametresinin alt parametrelerine siteden bakabiliriz. her komutta ilk iki sıfır olur diğerleri değişir.
        
        #WAYPOINT
    command.add(Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATİVE_ALT,mavutil.mavlink.MAV_CMD_NAV_WAYPOİNT, 0,0,0,0,0,35.54634643,75.43564262,10 ))
        # ilk iki sıfırdan sonra 4.parametre droneun enlem ifadesi, 5.parametre boylam, 6.parametre ise iltifa olarak girilir.
        #enlem ve boylamı mission planner üzerindeki haritadan alabiliriz.  
        
        #RETUR
    command.add(Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATİVE_ALT,mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0,0,0,0,0,0,0,0 ))
    #eve dönüşü sağlar
      #DOĞRULAMA
    command.add(Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATİVE_ALT,mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0,0,0,0,0,0,0,0 ))
    #diğer komutla eve gelen drone un görevi tamamlayıp tamamlamadığını öğrenmek için kullanadık. her hangi bir etkisi yok
    command.upload()   #komutları araca göndermek için kullanılır.
    
takeoff(10) #drone armed moduna geçmez ise bu komut ile yapabilirz.
task()
command.next = 0    #drone görevi birdikden sonra tekrar en başdan başlamasını istemek için kullanabiliriz

drone.mode = VehicleMode("AUTO") # drone a hazır komut yollarken (şimdi yaptığımız gibi) auto modunda çalıştırmamız gerekiyor.


while True:
    next_waypoint = command.next    #komut sırasını bize verir.
    print(f"sıradaki komut{next_waypoint}")
    time.sleep(2)
       
    if next_waypoint is 4:     #4. komutun gerçekleşip gerçekleşmediğini gösteriyor.
        print("görev tamamlandı")
        break
    
        
konum = LocationGlobalRelative(35.54634643,150.43564262,20)  #drone gitmesini istediğimiz konumu giriyoruz
drone.simple_goto(konum)  #gitmesi için emri verdik