#! /usr/bin/env python3

"""Demo of the AnalogIn "recording" mode functionality.

Summary
-------

This demo generates signals on two AnalogOut instrument channels and captures them on two AnalogIn instrument
channels, displaying the result as a graph using matplotlib.

For this demo to work as intended, connect analog-out channel #1 to analog-in channel #1 and analog-out
channel #2 to analog-in channel #2.

Description
-----------

When using the AnalogIn instrument with the "Record" acquisition mode, we prepare the analog input channel and
(if desired) trigger settings, then start the acquisition using a call to analogIn.configure().

Next, we enter a loop where we continuously fetch data from the instrument by calling analogIn.status(True).
This is repeated until analogIn.status() returns DwfState.Done. Note that this last status() call also transfers
acquisition data that needs to be processed.

After the status() call, we get information on the acquisition status by calling statusRecord(). This call
returns three numbers: counts of available, lost, and corrupted samples.

For perfect acquisition, the lost and currupt counts should be zero. If the acquisition requires more bandwith than
can be accomodated on the USB-2 link to the device (i.e., the sample frequency is too high), or if we fetch data too
slowly from our user program, we may see non-zero counts.

If this happens, the documentation provides no guidance on handling this other than to suggest that the acquisition
sample rate should be lowered, and/or the process should fetch data more quickly. The examples provided by digilent
suggest that the way to handle nonzero "lost" samples is to skip over them; this is what we do in the program below
(filling the lost samples with NaNs).

Assuming the lost and corrupt counts are zero, the 'available' count gives the number of valid samples available in
the local (PC-side) buffer. These samples can be obtained using calls to statusData(), statusData2(), or
statusData16(). The pydwf library implements these functions by having them allocate a sufficiently-sized local
numpy array, reading the sample data into it, and returning that array.

At the end of the acquisition, i.e., after the status() function returns DwfState.Done, these sub-arrays are
concatenated to deliver the full sample record of the acquisition.

At that point, we discard all but the last (record_length * sample_frequency) samples that constitute the requested
recording length. The preceding samples were received from the device, but the first few samples may be garbled,
and the total number of samples received will generally exceed the number of samples requested, sometimes by a
considerable margin.

The discarding process is also needed to make sure that the trigger position is in a predictable and reproducable
place. After discarding the first samples of the acquisition to get the requested length, the first remaining
sample is at the time, measured in seconds, returned by the analogIn.triggerPositionStatus() call, relative to
the trigger moment.
"""

import argparse
import time
import numpy as np
import matplotlib.pyplot as plt

from pydwf import DigilentWaveformsLibrary, AnalogOutNode, FUNC, ACQMODE, TRIGSRC, TRIGTYPE, DwfTriggerSlope, DwfState, FILTER
from demo_utilities import find_demo_device, DemoDeviceNotFoundError

def configure_analog_output(analogOut, analog_out_frequency, analog_out_amplitude, analog_out_offset):
    """Configure a cosine signal on channel 1, and a sine signal on channel 2."""

    CH1 = 0 # This channel will carry a 'cosine' (i.e., precede channel 2 by 90 degrees).
    CH2 = 1 # This channel will carry a 'sine'.

    node = AnalogOutNode.Carrier

    analogOut.reset(-1)  # Reset both channels.

    analogOut.nodeEnableSet   (CH1, node, True)
    analogOut.nodeFunctionSet (CH1, node, FUNC.Sine)
    analogOut.nodeFrequencySet(CH1, node, analog_out_frequency)
    analogOut.nodeAmplitudeSet(CH1, node, analog_out_amplitude)
    analogOut.nodeOffsetSet   (CH1, node, analog_out_offset)
    analogOut.nodePhaseSet    (CH1, node, 90.0)

    analogOut.nodeEnableSet   (CH2, node, True)
    analogOut.nodeFunctionSet (CH2, node, FUNC.Sine)
    analogOut.nodeFrequencySet(CH2, node, analog_out_frequency)
    analogOut.nodeAmplitudeSet(CH2, node, analog_out_amplitude)
    analogOut.nodeOffsetSet   (CH2, node, analog_out_offset)
    analogOut.nodePhaseSet    (CH2, node, 0.0)

    # Synchronize second channel to first channel. This ensures that they will start simultaneously.
    analogOut.masterSet(CH2, CH1)

    # Start output on first (and second) channel.
    analogOut.configure(CH1, True)


def run_demo(analogIn, sample_frequency, record_length, trigger_flag, signal_frequency):
    """Set up analog output, configure the analog input, and perform repeated acquisitions and present them graphically."""

    if trigger_flag:
        trigger_position = -0.5 * record_length # Position of first sample relative to the trigger. Setting it to -0.5 * record_length puts the trigger halfway the capture window.
        trigger_level    = 0.0                  # Trigger level in Volts.

    # Configure analog input instrument acquisition.

    CH1 = 0
    CH2 = 1

    channels = (CH1, CH2)

    for channel_index in channels:
        analogIn.channelEnableSet(channel_index, True)
        analogIn.channelFilterSet(channel_index, FILTER.Decimate)
        analogIn.channelRangeSet (channel_index, 5.0)

    analogIn.acquisitionModeSet(ACQMODE.Record)
    analogIn.frequencySet      (sample_frequency)
    analogIn.recordLengthSet   (record_length)

    if trigger_flag:
        # Set up trigger for the analog input instrument.
        # We will trigger on the rising transitions of CH2 (the "cosine" channel) through 0V.
        analogIn.triggerSourceSet(TRIGSRC.DetectorAnalogIn)
        analogIn.triggerChannelSet(CH2)
        analogIn.triggerTypeSet(TRIGTYPE.Edge)
        analogIn.triggerConditionSet(DwfTriggerSlope.Rise)
        analogIn.triggerPositionSet(trigger_position)
        analogIn.triggerLevelSet(trigger_level)
        analogIn.triggerHysteresisSet(0.010) # Configure a small amount of hysteresis to make sure we only see rising edges.

    # Calculate number of samples for each acquisition.
    num_samples = round(sample_frequency * record_length)

    # Outer loop: perform repeated acquisitions.
    acquisition_nr = 0

    while True: 

        acquisition_nr += 1 # Increment acquisition number.

        print("[{}] Recording {} samples ...".format(acquisition_nr, num_samples))

        # Inner loop: single acquisition, receive data from AnalogIn instrument and display it.

        samples = []

        total_samples_lost = total_samples_corrupted = 0

        analogIn.configure(False, True)  # Start acquisition sequence.

        while True:

            status = analogIn.status(True)
            (current_samples_available, current_samples_lost, current_samples_corrupted) = analogIn.statusRecord()

            total_samples_lost += current_samples_lost
            total_samples_corrupted += current_samples_corrupted

            if current_samples_lost != 0:
                # Append NaN samples as placeholders for lost samples.
                # This follows the Digilent example. We haven't verified yet that this is the proper way to handle lost samples.
                lost_samples = np.full((current_samples_lost, 2), np.nan)
                samples.append(lost_samples)

            if current_samples_available != 0:
                # Append samples read from both channels.
                # Note that we read the samples seperately for each channel;
                # We then put them into the same 2D array with shape (current_samples_available, 2).
                current_samples = np.vstack([analogIn.statusData(channel_index, current_samples_available) for channel_index in channels]).transpose()
                samples.append(current_samples)

            if status == DwfState.Done:
                # We received the last of the record samples.
                # Note the time, in seconds, of the first valid sample, and break from the acquisition loop.
                if trigger_flag:
                    time_of_first_sample = analogIn.triggerPositionStatus()
                else:
                    time_of_first_sample = 0.0
                break

        if total_samples_lost != 0:
            print("[{}] - WARNING - {} samples were lost! Reduce sample frequency.".format(acquisition_nr, total_samples_lost))

        if total_samples_corrupted != 0:
            print("[{}] - WARNING - {} samples could be corrupted! Reduce sample frequency.".format(acquisition_nr, total_samples_corrupted))

        # Concatenate all acquired samples. The result is an (n, 2) array of sample values.
        samples = np.concatenate(samples)

        if len(samples) > num_samples:
            discard_count = len(samples) - num_samples
            print("[{}] - NOTE - discarding oldest {} of {} samples ({:.1f}%); keeping {} samples.".format(
                acquisition_nr,
                discard_count, len(samples), 100.0 * discard_count /  len(samples), num_samples))

            samples = samples[discard_count:]

        # Calculate sample time of each of the samples.
        t = time_of_first_sample + np.arange(len(samples)) / sample_frequency

        plt.clf()
        plt.grid()

        plt.title("AnalogIn acquisition #{}\n{} samples ({} seconds at {} Hz)\nsignal frequency: {} Hz".format(
            acquisition_nr, num_samples, record_length, sample_frequency, signal_frequency))

        if trigger_flag:
            plt.xlabel("time relative to trigger [s]\ntriggering on rising zero transition of channel 2")
        else:
            plt.xlabel("acquisition time [s]")

        plt.ylabel("signal [V]")

        if trigger_flag:
            plt.xlim(-0.55 * record_length, 0.55 * record_length)
        else:
            plt.xlim(-0.05 * record_length, 1.05 * record_length)

        plt.ylim(-3.0, 3.0)

        if trigger_flag:
            plt.axvline(0.0, c='r')
            plt.axhline(trigger_level, c='r')

        plt.plot(t, samples[:, CH1], color='orange', label="channel 1 (cos)")
        plt.plot(t, samples[:, CH2], color='blue'  , label="channel 2 (sin)")

        plt.legend(loc="upper right")

        plt.pause(1e-3)


def main():

    parser = argparse.ArgumentParser(description="Demonstrate analog input recording with triggering.")

    parser.add_argument("--sample-frequency", "-fs" , type=float, default=100000.0, help="Sample frequency, in samples per second.")
    parser.add_argument("--record-length"   , "-r"  , type=float, default=0.100, help="Record length, in seconds.")
    parser.add_argument("--disable-trigger" , "-x"  , action="store_false", help="Disable triggering.", dest="trigger")

    args = parser.parse_args()

    dwf = DigilentWaveformsLibrary()

    try:
        # We select the first configuration with the highest available "AnalogInBufferSize" configuration parameter.
        with find_demo_device(dwf, configuration_fitness_func=lambda configuration_parameters: configuration_parameters["AnalogInBufferSize"]) as device:

            analogOut = device.analogOut
            analogIn  = device.analogIn

            analog_out_frequency = 5 / args.record_length # We want to see 5 full cycles in the acquisition window.
            analog_out_amplitude = 2.5                    # Signal amplitude in Volt. The AnalogOut instrument can do 5 Vpp, so 2.5 V amplitude is maximum.
            analog_out_offset    = 0.0                    # Signal offset in Volt.

            print("Configuring analog output signals ({} Hz) ...".format(analog_out_frequency))

            configure_analog_output(analogOut, analog_out_frequency, analog_out_amplitude, analog_out_offset)

            time.sleep(2.0)  # Wait for a bit to ensure the stability of the analog output signals.

            run_demo(analogIn, args.sample_frequency, args.record_length, args.trigger, analog_out_frequency)
    except DemoDeviceNotFoundError:
        print("Could not find demo device, exiting.")

if __name__ == "__main__":
    main()
