#! /usr/bin/env python3

"""
To run this demo program, hook up an ADXL345 to the Analog Discovery as follows:

   Ground <----> Ground
   V+     <----> VCC
   DIO0   -----> CS
   (NC)   ------ INT1
   (NC)   ------ INT2
   DIO3   -----> SDO
   DIO2   -----> SDA
   DIO1  ------> SCL
"""

import time
import argparse

from pydwf import DigilentWaveformLibrary, DwfDigitalOutIdle
from demo_utilities import find_demo_device, DemoDeviceNotFoundError

def set_positive_supply_voltage(analogIO, voltage: float):
    analogIO.channelNodeSet(0, 0, 1)
    analogIO.channelNodeSet(0, 1, voltage)
    analogIO.enableSet(1)

def demo_spi_protocol_api(spi):

    """Demonstrate the SPI protocol functionality by connecting to an ADXL345 accellerometer sensor.

    The Digital SPI protocol API has 19 methods.
    """

    # We use the ADXL345 in four-wire SPI mode (MISO and MOSI are separate lines).

    SPI_CSn  = 0  # SPI chip-select [CS ] (DIO channel 0)
    SPI_SCLK = 1  # SPI clock       [SCL] (DIO channel 1)
    SPI_MOSI = 2  # SPI MOSI        [SDA] (DIO channel 2)
    SPI_MISO = 3  # SPI MISO        [SDO] (DIO channel 3)

    SPI_TRANSFERTYPE_MOSI_MISO = 1
    SPI_BITS_PER_WORD = 8

    SPI_CSn_START = 0
    SPI_CSn_STOP  = 1

    SPI_MODE = 3

    SPI_BITORDER = 1 # MSB first

    spi.reset()

    spi.frequencySet(5000000.0) # Maximum clock frequency according to datasheet.

    spi.clockSet(SPI_SCLK)      # Select clock pin
    spi.dataSet(0, SPI_MOSI)    # Select MOSI pin
    spi.dataSet(1, SPI_MISO)    # Select MISO pin

    spi.idleSet(0, DwfDigitalOutIdle.High) # Set MOSI pin idle mode
    spi.idleSet(1, DwfDigitalOutIdle.High) # Set MISO pin idle mode

    spi.modeSet(SPI_MODE)       # CPOL=1, CPHA=1

    spi.orderSet(SPI_BITORDER)  # Send MSB first

    time.sleep(0.100)

    print()

    # Enable measurements (set 'Measure' bit in POWER_CTL register).
    # First byte, high two bits indicate a 'write' operation of a single byte.
    spi.select(SPI_CSn, 0)   # Set chip-select to 0
    response = spi.writeRead(SPI_TRANSFERTYPE_MOSI_MISO, SPI_BITS_PER_WORD, [0x00 | 0x2d, 8])
    spi.select(SPI_CSn, 1)   # Set chip-select to 1

    # Loop until interrupted.
    while True:

        # Perform readout of registers 0x32 .. 0x37.
        # First byte, high two bits indicate a 'read' operation of multiple bytes.
        spi.select(SPI_CSn, 0)   # Set chip-select to 0
        response = spi.writeRead(SPI_TRANSFERTYPE_MOSI_MISO, SPI_BITS_PER_WORD, [0xc0 | 0x32, 0, 0, 0, 0, 0, 0])
        spi.select(SPI_CSn, 1)   # Set chip-select to 1

        axisdata = response[1:7]

        ax = (axisdata[0] + axisdata[1] * 256 + 32768) % 65536 - 32768
        ay = (axisdata[2] + axisdata[3] * 256 + 32768) % 65536 - 32768
        az = (axisdata[4] + axisdata[5] * 256 + 32768) % 65536 - 32768

        print("\r[SPI] ADXL345: ax {:6} ay {:6} az {:6}".format(ax, ay, az), end="", flush=True)

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the SPI protocol API with an ADXL345 accellerometer.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformLibrary()
        with find_demo_device(dwf, args.serial_number) as device:
            set_positive_supply_voltage(device.analogIO, 3.3)
            demo_spi_protocol_api(device.digitalSpi)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")
    except KeyboardInterrupt:
        print("Keyboard interrupt, ending demo.")

if __name__ == "__main__":
    main()
