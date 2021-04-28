#! /usr/bin/env python3

import time
import math

from pydwf import DigilentWaveformsLibrary, AnalogOutNode, FUNC, DwfAnalogOutIdle
from demo_utilities import find_demo_device, DemoDeviceNotFoundError

def demo_fast_analog_out(analogOut):

    # Reset all channels.
    analogOut.reset(-1)  

    CH1 = 0
    CH2 = 1

    # Configure both output channels for square wave output, with idle behavior set to
    # drive the initial signal value.
    #
    # Note that we never actually start this waveform generation! We just set
    # the signal amplitude in Volt, which changes the output of the "idle" level
    # of the signal. This is the simplest way to directly drive the output of
    # the analog output channels that is also at least somewhat performant;
    # setting a single channel's output level in this way takes 0.5 .. 1 ms.

    for channel_index in (CH1, CH2):

        analogOut.nodeFunctionSet (channel_index, AnalogOutNode.Carrier, FUNC.Square)
        analogOut.idleSet         (channel_index, DwfAnalogOutIdle.Initial)
        analogOut.nodeEnableSet   (channel_index, AnalogOutNode.Carrier, True)

    frequency = 1.0 # Hz

    t_stopwatch = 0.0
    counter = 0

    t0 = time.monotonic()

    while True:

        t = time.monotonic() - t0

        vx = 2.5 * math.cos(2 * math.pi * t * frequency)
        vy = 2.5 * math.sin(2 * math.pi * t * frequency)

        # To change the output signal on each of the two channels, we just change the channel's
        # amplitude setting.

        analogOut.nodeAmplitudeSet(CH1, AnalogOutNode.Carrier, vx)
        analogOut.nodeAmplitudeSet(CH2, AnalogOutNode.Carrier, vy)

        counter += 1
        if counter == 1000:
            duration = (t - t_stopwatch)
            print("{:8.3f} loops/sec. Press Control-C to quit.".format(counter / duration))
            counter = 0
            t_stopwatch = t

def main():

    dwf = DigilentWaveformsLibrary()

    try:
        with find_demo_device(dwf) as device:
            demo_fast_analog_out(device.analogOut)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")
    except KeyboardInterrupt:
        print("Keyboard interrupt, ending demo.")


if __name__ == "__main__":
    main()
