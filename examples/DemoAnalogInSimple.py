#! /usr/bin/env python3

import argparse
import time

from pydwf import DigilentWaveformsLibrary
from demo_utilities import find_demo_device, DemoDeviceNotFoundError


def demo_analog_input_instrument_api_simple(analogIn):
    """Demonstrate the simplest possible use of the analog input channels.

    This demonstration simply calls the status() function of the AnalogIn instrument, with the 'readdData' argument specified as value False.
    Even though the 'readData' argument is false, the status update requested from the instrument does return up-to-date voltage levels of each
    of the channels.

    This straightforward way of querying the current AnalogIn voltages may be sufficient for simple applications that have no strict requirement
    on sample timing and triggering.
    """

    channel_count = analogIn.channelCount()
    if channel_count == 0:
        print("The device has no analog input channels that can be used for this demo.")
        return

    analogIn.reset()

    while True:
        analogIn.status(False)
        print("analog input", ", ".join("channel {}: {:25.20f} [V]".format(channel_index, analogIn.statusSample(channel_index)) for channel_index in range(channel_count)))
        time.sleep(0.010)

def main():

    parser = argparse.ArgumentParser(description="Demonstrate simplest possible AnalogIn instrument usage.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformsLibrary()
        with find_demo_device(dwf, args.serial_number) as device:
            demo_analog_input_instrument_api_simple(device.analogIn)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")
    except KeyboardInterrupt:
        print("Keyboard interrupt, ending demo.")

if __name__ == "__main__":
    main()
