import time
import os
import board
import digitalio
from adafruit_dps310.basic import DPS310
import wifi
import socketpool as socket
import ssl
import adafruit_requests
import adafruit_connection_manager

# IO Enable
io_enable_pin = digitalio.DigitalInOut(board.IO_POWER)
io_enable_pin.direction = digitalio.Direction.OUTPUT
io_enable_pin.value = False


i2c = board.I2C()
dps310 = DPS310(i2c, 0x76)
radio = wifi.radio
print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(
    os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
)
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}!")

SENSEBOX_ID = os.getenv("SENSEBOX_ID")
SENSOR_ID = os.getenv("SENSOR_ID")
# Define the openSensemap server
OSENSEMAP_HOST = "ingress.opensensemap.org"
OSENSEMAP_PATH = "/boxes/" + SENSEBOX_ID + "/data"
OSENSEMAP_TOKEN = os.getenv("AUTH_TOKEN")


pool = adafruit_connection_manager.get_radio_socketpool(radio)


# Initialize a requests session

#ssl_context = adafruit_connection_manager.get_radio_ssl_context(radio)
requests = adafruit_requests.Session(pool)

while True:
    try:
        print("Temperature = %.2f *C" % dps310.temperature)
        print("Pressure = %.2f hPa" % dps310.pressure)
        print("hello 1")
        # Prepare data to send
        data = {
            SENSOR_ID: "%.2f" % dps310.temperature,
        }

        # Send data to openSenseMap
        print(
            "Sending data to openSenseMap...http://" + OSENSEMAP_HOST + OSENSEMAP_PATH
        )
        url = "http://" + OSENSEMAP_HOST + OSENSEMAP_PATH
        headers = {"Content-Type": "application/json", "Authorization": OSENSEMAP_TOKEN}
        response = requests.post(url, json=data, headers=headers)

        # Print response
        print("Response:", response.json())

        # Close response
        response.close()

    except Exception as e:
        print("Error:", e)

    # Delay between measurements
    time.sleep(20)  # Change this value as needed