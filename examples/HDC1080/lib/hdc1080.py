import time
from adafruit_bus_device.i2c_device import I2CDevice

# HDC1080 Default I2C Address
HDC1080_I2C_ADDR = 0x40

# HDC1080 Registers
HDC1080_TEMP_REG = 0x00
HDC1080_HUMIDITY_REG = 0x01
HDC1080_CONFIG_REG = 0x02

class HDC1080:
    def __init__(self, i2c, address=HDC1080_I2C_ADDR):
        self.i2c_device = I2CDevice(i2c, address)
        self._buffer = bytearray(2)
        #self.reset() // Reset is not causing error

    def reset(self):
        with self.i2c_device as i2c:
            i2c.write(bytes([0x0, 0x0]))  # Writing to the configuration register to reset

    @property
    def temperature(self):
        with self.i2c_device as i2c:
            i2c.write(bytes([HDC1080_TEMP_REG]))
            time.sleep(0.0625)  # Temperature conversion time
            i2c.readinto(self._buffer)
            raw_temp = (self._buffer[0] << 8) | self._buffer[1]
            return (raw_temp / 65536.0) * 165.0 - 40.0

    @property
    def humidity(self):
        with self.i2c_device as i2c:
            i2c.write(bytes([HDC1080_HUMIDITY_REG]))
            time.sleep(0.0625)  # Humidity conversion time
            i2c.readinto(self._buffer)
            raw_humidity = (self._buffer[0] << 8) | self._buffer[1]
            return (raw_humidity / 65536.0) * 100.0

    @property
    def serial_number(self):
        with self.i2c_device as i2c:
            i2c.write(b'\xfc\x0d')  # Reading serial number register
            time.sleep(0.1)  # Wait for serial number to be ready
            i2c.readinto(self._buffer)
            return (self._buffer[0] << 24) | (self._buffer[1] << 16) | (self._buffer[2] << 8) | self._buffer[3]

    @property
    def firmware_version(self):
        with self.i2c_device as i2c:
            i2c.write(b'\x2d\x00')  # Reading firmware version register
            time.sleep(0.1)  # Wait for firmware version to be ready
            i2c.readinto(self._buffer)
            return (self._buffer[0] << 8) | self._buffer[1]

    def configure(self, heater=False, mode='sequential', battery_status=False):
        config_value = 0x1000 if heater else 0x0000
        if mode == 'sequential':
            config_value |= 0x0000
        elif mode == 'acquisition':
            config_value |= 0x0100
        else:
            raise ValueError("Invalid mode. Must be 'sequential' or 'acquisition'")
        config_value |= 0x0001 if battery_status else 0x0000

        with self.i2c_device as i2c:
            i2c.write(bytes([HDC1080_CONFIG_REG, (config_value >> 8) & 0xFF, config_value & 0xFF]))
