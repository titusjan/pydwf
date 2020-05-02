#! /usr/bin/env python3

import time
import argparse
import contextlib

from pydwf import DigilentWaveformLibrary
from demo_utilities import open_demo_device, OpenDemoDeviceError

def demo_analog_io_api(analogIO) -> None:
    """Demonstrates the Analog I/O device functionality.

    The Analog I/O API has 17 methods, 15 of which are used in this demo.

    * Device-level methods:

      - reset()
      - configure()                     (*) NOTE: not used in this demo.
      - status()

    * Device-level "enable" methods:

      - enableInfo()
      - enableSet()
      - enableGet()
      - enableStatus()

    * The Analog I/O device supports multiple channels.
      The following channel query methods are provided:

      - channelCount()
      - channelName()
      - channelInfo()

    * Each channel consists of a number of channel nodes.
      The following channel node query and set methods are provided:

      - channelNodeName()
      - channelNodeInfo()
      - channelNodeSetInfo()
      - channelNodeSet()                (*) NOTE: not used in this demo.
      - channelNodeGet()
      - channelNodeStatusInfo()
      - channelNodeStatus()
    """

    analogIO.reset()

    (enableSetSupported, enableStatusSupported) = analogIO.enableInfo()
    enableGet = analogIO.enableGet()
    enableStatus = analogIO.enableStatus()

    print("analogIO.enableSet() supported ......... : {}".format(enableSetSupported))
    print("analogIO.enableStatus() supported ...... : {}".format(enableStatusSupported))
    print("analogIO.enableGet() ................... : {}".format(enableGet))
    print("analogIO.enableStatus() ................ : {}".format(enableStatus))
    print()

    analogIO.status()  # Request status update of all channels.

    channel_count = analogIO.channelCount()
    print("The Analog I/O device has {} channels:".format(channel_count))
    print()

    for channel_index in range(channel_count):
        channel_name = analogIO.channelName(channel_index)
        node_count = analogIO.channelInfo(channel_index)  # Count number of nodes.
        print("Channel #{} ({} of {} channels) named {} has {} nodes:".format(channel_index, channel_index+1, channel_count, channel_name, node_count))
        print()

        for node_index in range(node_count):
            node_name        = analogIO.channelNodeName(channel_index, node_index)
            node_info        = analogIO.channelNodeInfo(channel_index, node_index)
            node_set_info    = analogIO.channelNodeSetInfo(channel_index, node_index)
            node_get         = analogIO.channelNodeGet(channel_index, node_index)
            node_status_info = analogIO.channelNodeStatusInfo(channel_index, node_index)
            node_status      = analogIO.channelNodeStatus(channel_index, node_index)
            print("    node_#{} ({} of {}):".format(node_index, node_index + 1, node_count))
            print("        node_name ............. {}".format(node_name))
            print("        node_info ............. {}".format(node_info))
            print("        node_set_info ......... {}".format(node_set_info))
            print("        node_get .............. {}".format(node_get))
            print("        node_status_info ...... {}".format(node_status_info))
            print("        node_status ........... {}".format(node_status))
            print()

def demo_analog_io_continuous_readout(analogIO) -> None:

    channel_index = 2 # USB Monitor channel.

    channel_name = analogIO.channelName(channel_index)[0]
    if channel_name != "USB Monitor":
        raise RuntimeError("Unexpected channel name.")

    print("Monitoring USB voltage, current, and temperature ...")
    print()

    try:
        while True:
            analogIO.status()  # Request status update
            usb_volts = analogIO.channelNodeStatus(channel_index, 0)
            usb_amps  = analogIO.channelNodeStatus(channel_index, 1)
            temp      = analogIO.channelNodeStatus(channel_index, 2)
            print("{}: {:.6f} [V] {:.3f} [mA] {:.2f} [°C]".format(channel_name, usb_volts, usb_amps * 1000.0, temp))
            time.sleep(0.500)
    except KeyboardInterrupt:
        print()
        print("Monitoring terminated.")
        print()

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the AnalogIO channels.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")
    args = parser.parse_args()

    try:
        dwf = DigilentWaveformLibrary()
        with contextlib.closing(open_demo_device(dwf, args.serial_number)) as device:
            demo_analog_io_api(device.analogIO)
            demo_analog_io_continuous_readout(device.analogIO)
    except OpenDemoDeviceError:
        print("Could not open demo device, exiting.")

if __name__ == "__main__":
    main()
