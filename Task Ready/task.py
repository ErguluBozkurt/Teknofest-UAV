# coding: utf8    turkce karakterlerin hata vermesini engellemek için
from dronekit import Command, connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil
import math
import distance
import data_logger

# Distance insan yüzü mesafesi ölçüyor bunu nesne mesafesi ie değiştirmemiz gerekiyor

try:
    iha = connect("/dev/serial/by-id/usb-ArduPilot_CUAV-X7_320035000751303137343737-if00", wait_ready=True, timeout = 100)
except:
    print("iha ya baglanma hatasi !!!!")
        
def takeoff(irtifa):
    while iha.is_armable is not True:
        print("İHA arm edilebilir durumda değil.")
        time.sleep(1)


    print("İHA arm edilebilir.")

    iha.mode = VehicleMode("GUIDED")

    iha.armed = True

    while iha.armed is not True:
        print("İHA arm ediliyor...")
        time.sleep(1)

    print("İHA arm edildi.")

    iha.simple_takeoff(irtifa)
    
    while iha.location.global_relative_frame.alt < irtifa * 0.9:
        print("İha hedefe yükseliyor.")
        time.sleep(1)


    
def gorev_ekle():
    global komut
    komut = iha.commands

    komut.clear()
    time.sleep(1)
    

    # TAKEOFF
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 20))
    
    #SPEED
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, 0, 0, 0, 10, 0, 0, 0, 0, 0))	
    
    # WAYPOINT
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,   -35.36032017 , 149.15972986 , 20))
    print(" irtifa = {}".format(iha.location.global_relative_frame.alt))
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,   -35.36383472,149.15950956, 20))
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, -35.36378139, 149.16027576 , 20))
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,  -35.36031410, 149.16056898 , 20))
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, -35.36040835, 149.16136141 , 20))
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,  -35.36372646, 149.16119708 , 20))
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,   -35.36369277, 149.16199566  , 20))
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,  -35.36032421, 149.16224350  , 20))
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,  -35.36034666, 149.16408851   , 20))      
    # iniş komutu 
    
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0,  -35.36270067, 149.16514103   , 0))      
    
    
    # DOĞRULAMA
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    komut.upload()
    print("Komutlar yükleniyor...")


takeoff(10)

gorev_ekle()

komut.next = 0

iha.mode = VehicleMode("AUTO")



################## iki nokta arasındaki mesafe fonksiyonu #####################################
def get_distance_metres(aLocation1, aLocation2):
    global xlat_xlong
    
    xlat = aLocation2.lat - aLocation1.lat
    xlong = aLocation2.lon - aLocation1.lon
    xlat_xlong = math.sqrt((xlat*xlat) + (xlong*xlong)) * 1.113195e5
    print("Gelecek nokataya son: {} Metre".format(round(xlat_xlong, 2)))
###############################################################################################

########### veriler kaydediliyor ##########
distance()
data_logger()  
###########################################

while True:
    next_waypoint = komut.next	
    
    print("Sıradaki komut : {}".format(next_waypoint))
    time.sleep(1)
    
    
    # iki nokta arasındaki mesafenin hesaplanmasında kulllanın değişkenlerin similasyondan çekilmesi
    missionitem=iha.commands[next_waypoint-1] 
    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z
    targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(iha.location.global_frame, targetWaypointLocation)

    if next_waypoint is 13:
        print("Görev bitti.")
        break


print("Döngüden çıkıldı.")
