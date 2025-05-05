import numpy as np

k = 0.32 # Hava sürtünme katsayısı
r = 0.036 # 3 cm yarıçap
g = 9.81 # yer çekim ivmesi
h = 50 # m yükseklik
m = 0.7 # kg top ağırlığı
Vx = 9 # m/s uçağın hızı 
Vc = 5 # m/s arabanın hızı
wind_v = 5 # m/s rüzgarın hızı

A = round(3.14*(r**2),5)
print("A : ", A)
t = round(np.sqrt((2*h) / g), 3) # yere düşüş zamanı (hava kuvveti ihmal)
print("T : ", t)
Vy = round(g*t, 3)
print("Vy : ", Vy)

fs1 = round(k*A*(Vy**2), 3)
print("FS1 : ", fs1)
fs1 = round((fs1 - (m*g)),3)
print("FS1 : ", fs1)
a1 = round(fs1/m, 3)# yukarı yönlü ivme
print("a1 : ", a1)
Vy_net = round(Vy - (-a1*t) - wind_v, 3)
print("Vy net : ", Vy_net)
t_net = round(Vy_net/g, 3)
print("T net : ", t_net)

fs2 = round(k*A*(Vx**2), 3)
print("FS2 : ", fs2)
a2 = round(fs2/m, 3) # kuvvetin yapmış olduğu araca ters ivme
print("a2 : ", a2)
Vx_net = round(Vx - (a2*t), 3)
print("Vx net : ", Vx_net)

x1 = round(Vx_net*t_net, 3) # topun gittiği mesafe
print("x1 : ", x1)
x2 = round(Vc*t_net, 3) # aracın t zamanda aldığı yol
print("x2 : ", x2)

X = x1 - x2 # Bu mesafe olduğunda aracı vurur
print(X)
if(X>-2.5 and X<2.5):
    print("Atış Yapılabilir")
