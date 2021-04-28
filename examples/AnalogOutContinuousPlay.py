#! /usr/bin/env python3

import argparse
import numpy as np

from pydwf import DigilentWaveformsLibrary, AnalogOutNode, FUNC, DwfState
from demo_utilities import find_demo_device, DemoDeviceNotFoundError


class sampler:
    def __init__(self, fs, frequency):
        self.fs = fs
        self.frequency = frequency
        self.k = 0 # sample index

    def get_samples(self, n: int):
        t = np.arange(self.k, self.k + n) / self.fs
        data = np.sin(t * self.frequency * 2 * np.pi)
        self.k += n

        return data

def demo_analog_output_instrument_api(analogOut):

    channel_count = analogOut.count()

    if channel_count == 0:
        print("The device has no analog output channels that can be used for this demo.")
        return

    analogOut.reset(-1)

    CH1 = 0
    CH2 = 1

    fs = 192e3

    analogOut.nodeEnableSet(CH1, AnalogOutNode.Carrier, True)
    analogOut.nodeFunctionSet(CH1, AnalogOutNode.Carrier, FUNC.Play)
    analogOut.nodeFrequencySet(CH1, AnalogOutNode.Carrier, fs)

    analogOut.nodeEnableSet(CH2, AnalogOutNode.Carrier, True)
    analogOut.nodeFunctionSet(CH2, AnalogOutNode.Carrier, FUNC.Play)
    analogOut.nodeFrequencySet(CH2, AnalogOutNode.Carrier, fs)

    sampler_ch1 = sampler(fs, 1000.0)
    sampler_ch2 = sampler(fs, 1000.1) # 0.1 Hz more, so you will see something non-static on the scope.

    data = sampler_ch1.get_samples(4096)
    analogOut.nodePlayData(CH1, AnalogOutNode.Carrier, data)

    data = sampler_ch2.get_samples(4096)
    analogOut.nodePlayData(CH2, AnalogOutNode.Carrier, data)

    analogOut.masterSet(CH2, CH1)
    analogOut.configure(CH1, True) # start

    while True:

        ch1_status = analogOut.status(CH1)
        ch2_status = analogOut.status(CH2)

        assert (ch1_status == DwfState.Triggered) and (ch2_status == DwfState.Triggered)

        (ch1_data_free, ch1_data_lost, ch1_data_corrupted) = analogOut.nodePlayStatus(CH1, AnalogOutNode.Carrier)
        (ch2_data_free, ch2_data_lost, ch2_data_corrupted) = analogOut.nodePlayStatus(CH2, AnalogOutNode.Carrier)

        if ch1_data_lost != 0 or ch1_data_corrupted != 0 or ch2_data_lost != 0 or ch2_data_corrupted != 0:
            print("ch1 status: {:10} {:10} {:10} ch2 status: {:10} {:10} {:10}".format(
                ch1_data_free, ch1_data_lost, ch1_data_corrupted,
                ch2_data_free, ch2_data_lost, ch2_data_corrupted))

        feed_ch1 = 0
        feed_ch2 = 0

        if ch1_data_free > ch2_data_free:
            if ch1_data_free >= 2048:
                feed_ch1 = ch1_data_free
        else:
            if ch2_data_free >= 2048:
                feed_ch2 = ch2_data_free

        if feed_ch1 > 0:
            print("Transferring {} samples to channel 1.".format(feed_ch1))
            data = sampler_ch1.get_samples(feed_ch1)
            analogOut.nodePlayData(CH1, AnalogOutNode.Carrier, data)

        if feed_ch2 > 0:
            print("Transferring {} samples to channel 2.".format(feed_ch2))
            data = sampler_ch2.get_samples(feed_ch2)
            analogOut.nodePlayData(CH2, AnalogOutNode.Carrier, data)

def main():

    parser = argparse.ArgumentParser(description="Demonstrate AnalogOut continuous playback of sample data.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformsLibrary()
        with find_demo_device(dwf, configuration_fitness_func=lambda configuration_parameters: configuration_parameters["AnalogOutBufferSize"]) as device:
            demo_analog_output_instrument_api(device.analogOut)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")

if __name__ == "__main__":
    main()
