import board
import busio
import time
from hdc1080 import HDC1080
import digitalio

# IO Enable
io_enable_pin = digitalio.DigitalInOut(board.IO_POWER)
io_enable_pin.direction = digitalio.Direction.OUTPUT
io_enable_pin.value = False

# Initialize I2C bus
i2c = board.I2C()

# Initialize HDC1080 sensor
sensor = HDC1080(i2c)


try:
    while True:
        temperature = sensor.temperature
        humidity = sensor.humidity

        print("Temperature: {:.2f} °C".format(temperature))
        print("Humidity: {:.2f} %".format(humidity))

        time.sleep(2)  # Wait for 2 seconds before next reading

except KeyboardInterrupt:
    print("Program stopped by user")
