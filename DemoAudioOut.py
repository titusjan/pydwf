#! /usr/bin/env python3

import time
import numpy as np
import matplotlib.pyplot as plt

from pydwf import DigilentWaveformLibrary, DwfParam, AnalogOutNode, DwfAnalogOutMode, FUNC

dwf = DigilentWaveformLibrary()

device = dwf.device.open(-1)
try:

    # This is the default value.
    device.paramSet(DwfParam.AudioOut, 1)

    ao = device.analogOut

    # Reset both channels
    ao.reset(-1)

    num_channels = ao.count()

    # (NUM_SAMPLES * freq) should be a multiple of fs.


    freq = 750.0
    fs = 48000.0

    NUM_SAMPLES = 512
    wavedata = np.sin(np.arange(NUM_SAMPLES) / fs * freq * 2 * np.pi)

    plt.plot(wavedata)
    plt.show()

    for channel_index in range(num_channels):

        ao.masterSet        (channel_index, channel_index)
        ao.runSet           (channel_index, 2.0)
        ao.waitSet          (channel_index, 0.500)
        ao.repeatSet        (channel_index, 5)
        ao.repeatTriggerSet (channel_index, False)
        ao.modeSet          (channel_index, DwfAnalogOutMode.Voltage)

        ao.nodeFunctionSet (channel_index, AnalogOutNode.Carrier, FUNC.Custom)
        ao.nodeFrequencySet(channel_index, AnalogOutNode.Carrier, fs)
        ao.nodeAmplitudeSet(channel_index, AnalogOutNode.Carrier, 0.500)
        ao.nodeOffsetSet   (channel_index, AnalogOutNode.Carrier, 0.0)
        ao.nodeSymmetrySet (channel_index, AnalogOutNode.Carrier, 50.0)
        ao.nodePhaseSet    (channel_index, AnalogOutNode.Carrier, 0.0)

        ao.nodeDataSet(channel_index, AnalogOutNode.Carrier, wavedata)

        # Enable Carrier node.
        ao.nodeEnableSet(channel_index, AnalogOutNode.Carrier, True)

        # Disable FM and AM nodes.
        ao.nodeEnableSet(channel_index, AnalogOutNode.FM, False)
        ao.nodeEnableSet(channel_index, AnalogOutNode.AM, False)

    ao.configure(-1, True)

    while True:

        print("\033[2J\033[2H", end="")

        for channel_index in range(num_channels):

            status = ao.status(channel_index)

            master_get         = ao.masterGet(channel_index)  # State machine to which we listen.

            trigger_source_get = ao.triggerSourceGet (channel_index)
            trigger_slope_get  = ao.triggerSlopeGet  (channel_index)
            run_info           = ao.runInfo          (channel_index)
            run_get            = ao.runGet           (channel_index)
            run_status         = ao.runStatus        (channel_index)
            wait_info          = ao.waitInfo         (channel_index)
            wait_get           = ao.waitGet          (channel_index)
            repeat_info        = ao.repeatInfo       (channel_index)
            repeat_get         = ao.repeatGet        (channel_index)
            repeat_status      = ao.repeatStatus     (channel_index)
            repeat_trigger_get = ao.repeatGet        (channel_index)
            limitation_info    = ao.limitationInfo   (channel_index)
            limitation_get     = ao.limitationGet    (channel_index)
            mode_get           = ao.modeGet          (channel_index)
            idle_info          = ao.idleInfo         (channel_index)
            idle_get           = ao.idleGet          (channel_index)
            node_info          = ao.nodeInfo         (channel_index)

            print("channel {}".format(channel_index))
            print("    status .................. : {}".format(status))
            print("    master get............... : {}".format(master_get))
            print("    trigger source get ...... : {}".format(trigger_source_get))
            print("    trigger slope get ....... : {}".format(trigger_slope_get))
            print("    run info ................ : {}".format(run_info))
            print("    run get ................. : {}".format(run_get))
            print("    run status .............. : {}".format(run_status))
            print("    wait info ............... : {}".format(wait_info))
            print("    wait get ................ : {}".format(wait_get))
            print("    repeat info ............. : {}".format(repeat_info))
            print("    repeat get .............. : {}".format(repeat_get))
            print("    repeat status ........... : {}".format(repeat_status))
            print("    repeat trigger get ...... : {}".format(repeat_trigger_get))
            print("    limitation info ......... : {}".format(limitation_info))
            print("    limitation get .......... : {}".format(limitation_get))
            print("    mode get ................ : {}".format(mode_get))
            print("    idle info ............... : {}".format(idle_info))
            print("    idle get ................ : {}".format(idle_get))
            print("    node info ............... : {}".format(node_info))
            print()

            continue

            for node in node_info:

                node_enable_get     = ao.nodeEnableGet     (channel_index, node)
                node_function_info  = ao.nodeFunctionInfo  (channel_index, node)
                node_function_get   = ao.nodeFunctionGet   (channel_index, node)
                node_frequency_info = ao.nodeFrequencyInfo (channel_index, node)
                node_frequency_get  = ao.nodeFrequencyGet  (channel_index, node)
                node_amplitude_info = ao.nodeAmplitudeInfo (channel_index, node)
                node_amplitude_get  = ao.nodeAmplitudeGet  (channel_index, node)
                node_offset_info    = ao.nodeOffsetInfo    (channel_index, node)
                node_offset_get     = ao.nodeOffsetGet     (channel_index, node)
                node_symmetry_info  = ao.nodeSymmetryInfo  (channel_index, node)
                node_symmetry_get   = ao.nodeSymmetryGet   (channel_index, node)
                node_phase_info     = ao.nodePhaseInfo     (channel_index, node)
                node_phase_get      = ao.nodePhaseGet      (channel_index, node)
                node_data_info      = ao.nodeDataInfo      (channel_index, node)

                print("    node {}".format(node))
                print("        enable get .......... : {}".format(node_enable_get))
                print("        function_info ....... : {}".format(node_function_info))
                print("        function_get ........ : {}".format(node_function_get))
                print("        frequency_info ...... : {}".format(node_frequency_info))
                print("        frequency_get ....... : {}".format(node_frequency_get))
                print("        amplitude_info ...... : {}".format(node_amplitude_info))
                print("        amplitude_get ....... : {}".format(node_amplitude_get))
                print("        offset_info ......... : {}".format(node_offset_info))
                print("        offset_get .......... : {}".format(node_offset_get))
                print("        symmetry_info ....... : {}".format(node_symmetry_info))
                print("        symmetry_get ........ : {}".format(node_symmetry_get))
                print("        phase_info .......... : {}".format(node_phase_info))
                print("        phase_get ........... : {}".format(node_phase_get))
                print("        data_info ........... : {}".format(node_data_info))

        time.sleep(0.200)

finally:
    device.close()
