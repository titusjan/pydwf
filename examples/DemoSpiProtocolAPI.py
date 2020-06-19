#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary
from demo_utilities import open_demo_device, OpenDemoDeviceError

def set_positive_supply_voltage(analogIO, voltage: float):
    analogIO.channelNodeSet(0, 0, 1)
    analogIO.channelNodeSet(0, 1, 3.3)
    analogIO.enableSet(1)

def demo_spi_protocol_api(spi):
    """Demonstrate the SPI protocol functionality.

    The Digital SPI protocol API has 18 methods.
    """

    SPI_CSn  = 0  # SPI chip-select   (DIO channel 0)
    SPI_SCLK = 1  # SPI clock         (DIO channel 1)
    SPI_MOSI = 2  # SPI MOSI          (DIO channel 2)
    SPI_MISO = 3  # SPI MISO          (DIO channel 3)

    SPI_TRANSFERTYPE_MOSI_MISO = 1
    SPI_BITS_PER_WORD = 8

    SPI_CSn_START = 0
    SPI_CSn_STOP  = 1

    SPI_MODE = 3

    SPI_BITORDER = 1 # MSB first

    spi.reset()

    spi.frequencySet(5000000.0)
    spi.clockSet(SPI_SCLK)       # Select clock pin
    spi.dataSet(0, SPI_MOSI)    # Select MOSI pin
    spi.dataSet(1, SPI_MISO)    # Select MISO pin

    spi.modeSet(SPI_MODE)       # CPOL=1, CPHA=1

    spi.orderSet(SPI_BITORDER)  # Send MSB first

    spi.select(SPI_CSn, 1)   # Set chip-select to 1
    time.sleep(0.100)
    spi.select(SPI_CSn, 0)   # Set chip-select to 1
    time.sleep(0.100)
    spi.select(SPI_CSn, 1)   # Set chip-select to 1
    time.sleep(0.100)

    print()

    if True:
        spi.select(SPI_CSn, 0)   # Set chip-select to 0
        response = spi.writeRead(SPI_TRANSFERTYPE_MOSI_MISO, SPI_BITS_PER_WORD, [0x00 + 0x2d, 8])
        spi.select(SPI_CSn, 1)   # Set chip-select to 1

    while True:

        spi.select(SPI_CSn, 0)   # Set chip-select to 0
        response = spi.writeRead16(SPI_TRANSFERTYPE_MOSI_MISO, SPI_BITS_PER_WORD, [0xc0 + 50, 0, 0, 0, 0, 0, 0])
        spi.select(SPI_CSn, 1)   # Set chip-select to 1

        axisdata = response[1:7]

        ax = (axisdata[0] + axisdata[1] * 256 + 32768) % 65536 - 32768
        ay = (axisdata[2] + axisdata[3] * 256 + 32768) % 65536 - 32768
        az = (axisdata[4] + axisdata[5] * 256 + 32768) % 65536 - 32768

        print("{:6} {:6} {:6}".format(ax, ay, az))

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the SPI protocol API.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformLibrary()
        with contextlib.closing(open_demo_device(dwf, args.serial_number)) as device:
            set_positive_supply_voltage(device.analogIO, 3.3)
            demo_spi_protocol_api(device.digitalSpi)
    except OpenDemoDeviceError:
        print("Could not open demo device, exiting.")

if __name__ == "__main__":
    main()
