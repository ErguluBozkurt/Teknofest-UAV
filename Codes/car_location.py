"""
İhanın kamerasından yerde bulunan aracın konumunu tespit ediyor.
"""
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import math

# İHA'nın anlık GPS konumunu ve diğer verileri alın
iha_gps_location = (39.9334, 32.8597)  # Örnek koordinatlar
iha_altitude = 100  # metre cinsinden yükseklik
gimbal_servo_angles = [-35,-23 ]  # derece cinsinden servo açıları
iha_to_car_distance = 200  # metre cinsinden İHA ile araba arasındaki mesafe

# Gimbal servo açılarını radyana çevirin
gimbal_servo_angles_rad = [math.radians(angle) for angle in gimbal_servo_angles]

# Araç konumunu hesaplayın
car_relative_position = geodesic(kilometers=iha_to_car_distance/1000).destination(iha_gps_location, gimbal_servo_angles_rad[0], gimbal_servo_angles_rad[1])

# Araç konumunu GPS koordinatlarına dönüştürün
geolocator = Nominatim(user_agent="iha_geolocator")
car_location = geolocator.reverse((car_relative_position.latitude, car_relative_position.longitude))

print(f"Araç konumu: {car_location.address}")
print(f"GPS Koordinatları: (Enlem: {car_relative_position.latitude}, Boylam: {car_relative_position.longitude})")
