# senseBox MCU-S2 CircuitPython Example Code
# Simple code to blink the internal RGB-LED
import time
import board
import neopixel

# Configure the setup
PIXEL_PIN = board.NEOPIXEL  # pin that the NeoPixel is connected to | GPIO 1
ORDER = neopixel.GRB  # pixel color order
COLOR = (0, 255, 0)  # color to blink
CLEAR = (0, 0, 0)  # color to disable the LED
DELAY = 0.25  # blink rate in seconds

# Create the NeoPixel object
pixel = neopixel.NeoPixel(PIXEL_PIN, 1, brightness=0.1, pixel_order=ORDER)

# Loop forever and blink the color
while True:
    print("Hello senseBox")
    pixel[0] = COLOR
    time.sleep(DELAY)
    pixel[0] = CLEAR
    time.sleep(DELAY)
