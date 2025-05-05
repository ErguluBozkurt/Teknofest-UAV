import os

def set_fan_speed(speed):
    # speed değeri 0-255 arasında olmalıdır
    os.system("sudo bash -c 'echo {} > /sys/devices/pwm-fan/target_pwm'".format(speed))

# Fan hızının %50'sine ayarlama
set_fan_speed(127)
