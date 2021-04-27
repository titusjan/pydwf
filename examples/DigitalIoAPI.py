#! /usr/bin/env python3

import time
import argparse
import random

from pydwf import DigilentWaveformsLibrary
from demo_utilities import find_demo_device, DemoDeviceNotFoundError

def demo_digital_io_api(digitalIO) -> None:
    """Demonstrate the Digital I/O functionality.

    The Digital I/O API has 19 methods:

    Three generic methods:

    - reset()
    - configure()
    - status()

    Eight methods that work on 32 pins:

    - outputEnableInfo() -> int
    - outputEnableSet(output_enable: int)
    - outputEnableGet() -> int
    - outputInfo() -> int
    - outputSet(output: int)
    - outputGet() -> int
    - inputInfo() -> int
    - inputStatus() -> int

     Eight methods that work on 64 pins:

    - outputEnableInfo64() -> int
    - outputEnableSet64(output_enable: int)
    - outputEnableGet64() -> int
    - outputInfo64() -> int
    - outputSet64(output: int)
    - outputGet64() -> int
    - inputInfo64() -> int
    - inputStatus64() -> int
    """

    digitalIO.reset()

    print("Pins that support output-enable (i.e., tristate) functionality:")
    print()
    print("  outputEnableInfo (32 bit) ...... : {}0b{:032b}".format(32 * " ", digitalIO.outputEnableInfo()))
    print("  outputEnableInfo (64 bit) ...... : {}0b{:064b}".format( 0 * " ", digitalIO.outputEnableInfo64()))
    print()

    print("Pins for which output-enable is active (i.e. are not tristated):")
    print()
    print("  outputEnableGet (32 bit) ....... : {}0b{:032b}".format(32 * " ", digitalIO.outputEnableGet()))
    print("  outputEnableGet (64 bit) ....... : {}0b{:064b}".format( 0 * " ", digitalIO.outputEnableGet64()))
    print()

    print("Pins that are capable of driving output:")
    print()
    print("  outputInfo (32 bit) ............ : {}0b{:032b}".format(32 * " ", digitalIO.outputInfo()))
    print("  outputInfo (64 bit) ............ : {}0b{:064b}".format( 0 * " ", digitalIO.outputInfo64()))
    print()

    print("Pins for which output is set to high:")
    print()
    print("  outputGet (32 bit) ............. : {}0b{:032b}".format(32 * " ", digitalIO.outputGet()))
    print("  outputGet (64 bit) ............. : {}0b{:064b}".format( 0 * " ", digitalIO.outputGet64()))
    print()

    print("Pins that can be used as input:")
    print()
    print("  inputInfo (32 bit) ............. : {}0b{:032b}".format(32 * " ", digitalIO.inputInfo()))
    print("  inputInfo (64 bit) ............. : {}0b{:064b}".format( 0 * " ", digitalIO.inputInfo64()))
    print()

    print("Pin input status:")
    print()
    print("  inputStatus (32 bit) ........... : {}0b{:032b}".format(32 * " ", digitalIO.inputStatus()))
    print("  inputStatus (64 bit) ........... : {}0b{:064b}".format( 0 * " ", digitalIO.inputStatus64()))
    print()

    save_output_bits = digitalIO.outputEnableGet64()
    all_bits = digitalIO.outputInfo64()

    # Enable all outputs
    digitalIO.outputEnableSet64(all_bits)
    try:
        for i in range(100):
            random_bits = random.randrange(0, 2 ** 64) & all_bits
            digitalIO.outputSet64(random_bits)
            print("  outputGet (64 bit) ............. : {}0b{:064b}".format( 0 * " ", digitalIO.outputGet64()))
            readback = digitalIO.inputStatus()
            print("  inputStatus (64 bit) ........... : {}0b{:064b}".format( 0 * " ", digitalIO.inputStatus64()))
            print()
            time.sleep(0.500)
    finally:
        digitalIO.outputEnableSet64(save_output_bits)

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the DigitalIO functionality.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformsLibrary()
        with find_demo_device(dwf, args.serial_number) as device:
            demo_digital_io_api(device.digitalIO)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")
    except KeyboardInterrupt:
        print("Keyboard interrupt, ending demo.")

if __name__ == "__main__":
    main()
