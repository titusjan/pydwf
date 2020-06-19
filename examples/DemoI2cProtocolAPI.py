#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary, DwfParam
from demo_utilities import open_demo_device, OpenDemoDeviceError

def set_positive_supply_voltage(analogIO, voltage: float):
    analogIO.channelNodeSet(0, 0, 1)
    analogIO.channelNodeSet(0, 1, 3.3)
    analogIO.enableSet(1)

def demo_i2c_protocol_api(i2c):
    """Demonstrate the SPI protocol functionality.

    The Digital I2C protocol API has 18 methods.
    """

    I2C_SCL = 0
    I2C_SDA = 1

    i2c.reset()

    i2c.stretchSet(1)
    i2c.rateSet(400000.0)
    i2c.readNakSet(1)
    i2c.sclSet(I2C_SCL)
    i2c.sdaSet(I2C_SDA)

    time.sleep(0.100)

    # Enable measurements.
    i2c.write(0xa6, [0x2d, 0x08])

    while True:
        response = i2c.writeRead(0xa6, [0x32], 6)
        axisdata = response[1]

        ax = (axisdata[0] + axisdata[1] * 256 + 32768) % 65536 - 32768
        ay = (axisdata[2] + axisdata[3] * 256 + 32768) % 65536 - 32768
        az = (axisdata[4] + axisdata[5] * 256 + 32768) % 65536 - 32768

        print("{:6} {:6} {:6}".format(ax, ay, az))

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the I2C protocol API.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformLibrary()
        with contextlib.closing(open_demo_device(dwf, args.serial_number)) as device:
            set_positive_supply_voltage(device.analogIO, 3.3)
            demo_i2c_protocol_api(device.digitalI2c)
    except OpenDemoDeviceError:
        print("Could not open demo device, exiting.")

if __name__ == "__main__":
    main()
