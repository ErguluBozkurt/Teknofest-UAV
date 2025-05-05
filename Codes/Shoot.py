import numpy as np

k = 0.32 # Hava sürtünme katsayısı
r = 0.036 # 3 cm yarıçap
g = 9.81 # yer çekim ivmesi
h = 50 # m yükseklik
m = 0.7 # kg top ağırlığı
Vx = 9 # m/s uçağın hızı 
Vc = 5 # m/s arabanın hızı
wind_v = 5 # m/s rüzgarın hızı

def shoot():
    A = round(3.14*(r**2),5)
    t = round(np.sqrt((2*h) / g), 3) # yere düşüş zamanı (hava kuvveti ihmal)
    Vy = round(g*t, 3)

    fs1 = round(k*A*(Vy**2), 3)
    fs1 = round((fs1 - (m*g)),3)
    a1 = round(fs1/m, 3)# yukarı yönlü ivme
    Vy_net = round(Vy - (-a1*t) - wind_v, 3)
    t_net = round(Vy_net/g, 3)

    fs2 = round(k*A*(Vx**2), 3)
    a2 = round(fs2/m, 3) # kuvvetin yapmış olduğu araca ters ivme
    Vx_net = round(Vx - (a2*t), 3)

    x1 = round(Vx_net*t_net, 3) # topun gittiği mesafe
    x2 = round(Vc*t_net, 3) # aracın t zamanda aldığı yol

    X = x1 - x2 # Bu mesafe olduğunda aracı vurur
    print("Distance Between : ", X) # pozitif ileri, negatif geri
    if(X>-2.5 and X<2.5):
        print("Atış Yapılabilir")

shoot()