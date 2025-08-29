import time
import busio
import microcontroller
import adafruit_icm20x

scl = microcontroller.pin.GPIO42
sda = microcontroller.pin.GPIO45

i2c = busio.I2C(scl, sda)

icm = adafruit_icm20x.ICM20649(i2c, address=0x68)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % icm.acceleration)
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % icm.gyro)
    print("")
    time.sleep(0.5)