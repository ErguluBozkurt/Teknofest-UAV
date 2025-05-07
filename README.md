# Drone Görev Planlama ve Uçuş Otomasyonu

Bu proje, bir İHA'nın (`ArduPilot` tabanlı) belirlenen görev noktalarına otomatik olarak uçmasını, belirli bir irtifada kalkış yapmasını, hız ayarını ve inişi gerçekleştirmesini sağlar. Ayrıca görev sırasında mesafe hesaplaması ve veri kaydı yapılır.

## 🚀 Özellikler

- Otomatik kalkış ve iniş
- MAVLink üzerinden görev komutlarının yüklenmesi
- Belirlenen koordinatlara otomatik uçuş (waypoint'ler)
- Gerçek zamanlı mesafe hesaplama
- Uçuş verilerinin kaydı (distance ve data_logger modülleriyle)

## 🛠 Gereksinimler

Aşağıdaki Python modüllerinin kurulu olması gerekir:

- dronekit
- pymavlink
- distance
- data_logger

Kurulum için:

```bash
pip install -r requirements.txt
