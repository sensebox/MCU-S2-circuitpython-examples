import board
import neopixel
import digitalio
from adafruit_pixel_framebuf import PixelFramebuffer
import time
import adafruit_scd30
import math
from digitalio import DigitalInOut, Direction, Pull

# IO Enable
io_enable_pin = digitalio.DigitalInOut(board.IO_POWER)
io_enable_pin.direction = digitalio.Direction.OUTPUT
io_enable_pin.value = False

# SCD30 CO2
i2c = board.I2C()
scd = adafruit_scd30.SCD30(i2c)

# BTN
btn = DigitalInOut(board.BUTTON)
btn.direction = Direction.INPUT
btn.pull = Pull.UP
btn_state = btn.value

# LED Matrix
pixel_pin = board.D2
pixel_width = 12
pixel_height = 8
num_pixels = pixel_width * pixel_height
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.05, pixel_order=neopixel.GRB, auto_write=False
)

pixel_framebuf = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    alternating=True,
)

def mapRange(value, inMin, inMax, outMin, outMax):
    value = outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))
    return math.floor(value)

while True:
    btn_state = btn.value
    if btn_state:
        time.sleep(0.05)
        btn_state = btn.value

    print(btn_state)

    time.sleep(0.1) # sleep for debounce
    
    if scd.data_available:
        if btn_state:
            co2_value = scd.CO2
            width = mapRange(co2_value, 400, 2000, 1, pixel_width)
            color = 0xFF0000
            if(co2_value < 1000):
                color = 0x00FF00
            elif(co2_value < 1500):
                color = 0xFFFF00
            pixel_framebuf.fill(0x000000)
            pixel_framebuf.fill_rect(0, 0, width, pixel_height, color)
            pixel_framebuf.display()
        else:
            text = "CO2: " + str(scd.CO2) + " ppm"
            for i in range(6 * len(text) + pixel_width):
                pixel_framebuf.fill(0x000000)
                pixel_framebuf.text(text, pixel_width - i, 0, 0xFF00FF)
                pixel_framebuf.display()
                time.sleep(0.05)

