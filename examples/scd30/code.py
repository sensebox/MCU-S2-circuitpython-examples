import time
import board
import busio
import digitalio
import adafruit_scd30

# IO Enable - WICHTIG: Muss aktiviert werden für die Sensoren!
io_enable_pin = digitalio.DigitalInOut(board.IO_POWER)
io_enable_pin.direction = digitalio.Direction.OUTPUT
io_enable_pin.value = True

# Warte kurz, damit die Stromversorgung stabil ist
time.sleep(0.5)

# SCD-30 hat temperamental I2C mit clock stretching, datasheet empfiehlt 50KHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

while True:
    # Da das Messintervall lang ist (2+ Sekunden), prüfen wir auf neue Daten
    if scd.data_available:
        print("Data Available!")
        print("CO2:", scd.CO2, "PPM")
        print("Temperature:", scd.temperature, "degrees C")
        print("Humidity:", scd.relative_humidity, "%%rH")
        print("")
        print("Waiting for new data...")
        print("")
    time.sleep(0.5)