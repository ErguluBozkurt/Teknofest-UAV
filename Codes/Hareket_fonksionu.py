from dronekit import connect
from pymavlink import mavutil
import time

drone = connect('127.0.0.1:14550', wait_ready=True)

# GLOBALİ REFERANS ALAN HAREKET FONKSİYONU
def hareket(north, east, down):  # Kuzey güney ve aşağı yönde üç parametre istiyor
    
    msg = drone.message_factory.set_position_target_local_ned_encode(0,0, 0,mavutil.mavlink.MAV_FRAME_LOCAL_NED,0b0000111111111000, north, east, down,0, 0, 0, 0, 0, 0, 0, 0)    
    drone.send_mavlink(msg)  #drona bir mesaj yollar gibi
hareket(5, 5, -10)   # 5m kuzeye 5m güneye 10m yukarı çık demektir.

-------------------------------------------------------------------------------------------------------
# DRONE'U REFERANS ALAN HAREKET FONKSİYONU
def hareket(x, y, down):  #kendisinin olduğu yerde öne, sola(-) veya sağa(+), yukarı gitmesini sağlar

    msg = drone.message_factory.set_position_target_local_ned_encode(0, 0, 0,mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,0b0000111111111000, x, y, down,0, 0, 0, 0, 0, 0, 0, 0)    
    drone.send_mavlink(msg)
hareket(5,5,-10) #5m ileri, 5m sağa, 10m yukarı gönderir.
-----------------------------------------------------------------------------------------------------------
# İSTENİLEN HIZA GÖRE BELİRLİ SÜRE HAREKET FONKSİYONU
def hız(velocity_x, velocity_y, velocity_z, time): # x ,y, z yönleri time gideceği süreyi ifade eder(m/s)
   
    msg = drone.message_factory.set_position_target_local_ned_encode(0,0, 0,mavutil.mavlink.MAV_FRAME_LOCAL_NED, 0b0000111111000111, 0, 0, 0, velocity_x, velocity_y, velocity_z, 0, 0, 0, 0, 0)    
    
    for x in range(0,time):  # 0 dan time değerine kadar geçen sürede verilen hızda gider
        drone.send_mavlink(msg)
        time.sleep(1)
hız(5,5,1,10)
--------------------------------------------------------------------------------------------------
# DRONE'UN AÇISINI DEĞİŞTİRME FONKSİYONU
def derece(derece, relative=False): # girilen derece kadar dronun kendi ekseninde dönmesini sağlar.
    if relative:                           # relative true olursa kendisine göre döner, false olursa dünyaya göre döner.
        is_relative=1 
    else:
        is_relative=0 
    
    msg = drone.message_factory.command_long_encode(0, 0, mavutil.mavlink.MAV_CMD_CONDITION_YAW,0, derece ,0, 1, is_relative, 0, 0, 0)    
    drone.send_mavlink(msg)


derece(90, True)