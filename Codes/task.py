from dronekit import Command, connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil
import math

iha = connect("127.0.0.1:14550", wait_ready=True)

points_task = [
[-35.35993278, 149.16515480, 20],
[-35.36079741, 149.16255249, 20],
[-35.36325777, 149.16342011, 20]
]

points_take_off = [
[-35.36088208,149.16511475, 10],
[-35.35995730,149.16515754, 15],
[-35.36281104,149.16398443, 20]
]



def task_add(points): #enlem, boylam, yukseklik
    komut = iha.commands
    komut.clear()
    time.sleep(1)
    

    lat = points[0]
    lon = points[1]
    alt = points[2]
   
    # WAYPOINT
    # 0,0,komut sirasi,alt ve konum referansi,0,0,0,yaricap,yorunge kontrolu,0,lat,lon,alt
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 80, 0, 0, lat, lon, alt)) 
            
    komut.upload()
    print("Görev Komutları yukleniyor...")


def take_off(points):
    komut = iha.commands
    komut.clear()
    time.sleep(1)
    

    lat = points[0]
    lon = points[1]
    alt = points[2]

    # TAKEOFF
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 1))
    # WAYPOINT
    komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 10, 0, 0, lat, lon, alt)) 

    komut.upload()
    print("Kalkış Komutları yukleniyor...")


########### iniş kodu ###########    
def landed():
    pass


#iki nokta arasindaki mesafe
def get_distance_metres(Location1, Location2):

    xlat = Location2[0] - Location1.lat
    xlong = Location2[1] - Location1.lon
    aradaki_mesafe = round(math.sqrt((xlat*xlat) + (xlong*xlong)) * 1.113195e5, 2)
    print(f"Gelecek nokataya son:{aradaki_mesafe} Metre")
    time.sleep(0.2)
    return(aradaki_mesafe)


i = 0
j = 0

while True:
    channel_value = input("Exit : 1100 \nLanded : 1300 \nTake Off : 1600 \nTask Update : 1900 \nChannel SwC : ")
    if(channel_value == "1900"):
        task_add(points_task[i])
    
    elif(channel_value == "1600"):
        take_off(points_take_off[j])
        if(j == 2):
            print("Take Off Success")
        j += 1
        
    elif(channel_value == "1300"):
        landed()

    elif(channel_value == "1100"):
        print("Task Finished. The Mode Guided")
        iha.mode = VehicleMode("GUIDED")
        break

    else:
        print("Channel Error !!!. Task Finished")
        break

    iha.mode = VehicleMode("AUTO") 
    
    aradaki_mesafe = get_distance_metres(iha.location.global_frame , points_task[i])
    if(aradaki_mesafe <= 100):
        print("Konuma gidiliyor...")
        time.sleep(1)
        i += 1
        if(i == 2):
            i = 0
            print("Task Loop Again")