# Sabit Kanat Hava Aracı Görev Planlama, Otonom Hareket ve Uçuş

Bu proje, bir İHA'nın (`ArduPilot` tabanlı) belirlenen görev noktalarına otomatik olarak uçmasını, belirli bir irtifada kalkış yapmasını, hız ayarını ve inişi gerçekleştirmesini sağlar. Ayrıca görev sırasında kamera kullanılarak kara hedefine olan mesafe hesaplanarak belirli irtifa ve hızda, doğru atış zamanı matematiksel yöntemler ile belirlenmesi ve tüm sistemin veri kaydı yapılır.

## 🚀 Özellikler

- Otomatik kalkış ve iniş
- MAVLink üzerinden görev komutlarının yüklenmesi
- Belirlenen koordinatlara otomatik uçuş (waypoint'ler)
- Gerçek zamanlı kara hedefi için mesafe ve atış zamanı hesaplama (distance)
- Uçuş verilerinin kaydı (data_logger)

## 🛠 Gereksinimler

Aşağıdaki Python modüllerinin kurulu olması gerekir:

- dronekit
- pymavlink
- distance (Yazılı modül)
- data_logger (Yazılı modül)

Kurulum için:

```bash
pip install -r requirements.txt
