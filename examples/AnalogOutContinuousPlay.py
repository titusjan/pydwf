#! /usr/bin/env python3

""" This demo shows continuous, synchronized sample playback on two channels."""

import argparse
import numpy as np

from pydwf import DigilentWaveformsLibrary, AnalogOutNode, FUNC, DwfState, TRIGSRC
from demo_utilities import find_demo_device, DemoDeviceNotFoundError


class circle_sampler:

    def __init__(self, channel: str, sample_frequency: float, refresh_frequency: float):
        self.channel = channel
        self.sample_frequency = sample_frequency
        self.refresh_frequency = refresh_frequency
        self.k = 0 # sample index

    def get_samples(self, n: int):
        t = np.arange(self.k, self.k + n) / self.sample_frequency
        self.k += n

        if self.channel == 'x':
            return np.cos(t * self.refresh_frequency * 2 * np.pi)
        elif self.channel == 'y':
            return np.sin(t * self.refresh_frequency * 2 * np.pi)


class rotating_polygon_sampler:

    def __init__(self, channel: str, sample_frequency: float, refresh_frequency: float, n_points: float, n_step: int, revolutions_per_sec: float):
        self.sample_frequency = sample_frequency
        self.refresh_frequency = refresh_frequency
        self.revolutions_per_sec = revolutions_per_sec
        self.channel = channel
        self.n_points = n_points
        self.n_step   = n_step
        self.k = 0 # sample index

    def get_samples(self, n: int):
        t = np.arange(self.k, self.k + n) / self.sample_frequency
        self.k += n

        tt = t * self.refresh_frequency

        residual = np.mod(tt * self.n_points, 1.0)

        b = np.round(tt * self.n_points - residual)

        h0 = (2.0 * np.pi * self.n_step / self.n_points) * b
        h1 = (2.0 * np.pi * self.n_step / self.n_points) * (b + 1)

        x0 = np.cos(h0)
        y0 = np.sin(h0)

        x1 = np.cos(h1)
        y1 = np.sin(h1)

        x = x0 + (x1 - x0) * residual
        y = y0 + (y1 - y0) * residual

        # rotate (x, y) by "revolutions_per_sec * t"

        h = 2 * np.pi * self.revolutions_per_sec * t

        if self.channel == 'x':
            return np.cos(h) * x - np.sin(h) * y
        elif self.channel == 'y':
            return np.sin(h) * x + np.cos(h) * y


def demo_analog_output_instrument_api(analogOut, shape, sample_frequency, refresh_frequency, n_points, n_step, revolutions_per_sec):

    channel_count = analogOut.count()

    if channel_count == 0:
        print("The device has no analog output channels that can be used for this demo.")
        return

    analogOut.reset(-1)

    CH1 = 0
    CH2 = 1

    # The samplers for a given shape return the requested number of samples on demand, for the given channel.
    if shape == 'circle':
        sampler_ch1 = circle_sampler('x', sample_frequency, refresh_frequency)
        sampler_ch2 = circle_sampler('y', sample_frequency, refresh_frequency)
    elif shape == 'poly':
        sampler_ch1 = rotating_polygon_sampler('x', sample_frequency, refresh_frequency, n_points, n_step, revolutions_per_sec)
        sampler_ch2 = rotating_polygon_sampler('y', sample_frequency, refresh_frequency, n_points, n_step, revolutions_per_sec)

    analogOut.nodeEnableSet(CH1, AnalogOutNode.Carrier, True)
    analogOut.nodeFunctionSet(CH1, AnalogOutNode.Carrier, FUNC.Play)
    analogOut.nodeFrequencySet(CH1, AnalogOutNode.Carrier, sample_frequency)

    analogOut.nodeEnableSet(CH2, AnalogOutNode.Carrier, True)
    analogOut.nodeFunctionSet(CH2, AnalogOutNode.Carrier, FUNC.Play)
    analogOut.nodeFrequencySet(CH2, AnalogOutNode.Carrier, sample_frequency)

    # Configure CH2 to follow CH1.
    analogOut.masterSet(CH2, CH1)

    analogOut.configure(CH1, True) # Start channels 1 and 2.

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

    parser = argparse.ArgumentParser(description="Demonstrate AnalogOut continuous, synchronous playback of sample data on two channels.")
    parser.add_argument('serial_number', nargs='?', help="serial number of the Digilent device")

    parser.add_argument('--shape', choices = ('circle', 'poly')     , default = 'circle' , help="shape to be output on CH1 (x coordinate) and CH2 (y coordinate)")
    parser.add_argument('--sample_frequency'   , "-fs"  , type=float, default =   48.0e3 , help="output sample frequency")
    parser.add_argument('--refresh_frequency'  , "-fr"  , type=float, default =   100.0  , help="number of shape redraws per second")
    parser.add_argument('--n_points'           , "-np"  , type=int  , default =       5  , help="number of poly points (poly mode only)")
    parser.add_argument('--n_step'             , "-ns"  , type=int  , default =       1  , help="steps to the next poly point (poly mode only)")
    parser.add_argument('--revolutions_per_sec', "-rps" , type=float, default =     0.1  , help="shape revolutions per second (poly mode only)")

    args = parser.parse_args()

    try:
        dwf = DigilentWaveformsLibrary()
        # Select the device configuration with the largest value for AnalogOutBufferSize.
        with find_demo_device(dwf, configuration_fitness_func=lambda configuration_parameters: configuration_parameters["AnalogOutBufferSize"]) as device:
            demo_analog_output_instrument_api(device.analogOut, args.shape, args.sample_frequency, args.refresh_frequency, args.n_points, args.n_step, args.revolutions_per_sec)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")


if __name__ == "__main__":
    main()
