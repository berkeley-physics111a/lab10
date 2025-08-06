"""Physics 111A Lab 10 functions.
Written by Auden Young, 7/2025.

Important objects:
    ADSHardware (class): a collection of methods for interfacing with the ADS
        variables:
            handle: address to connect to the ADS
        functions:
            startup: connects to ADS
            open_scope: opens connection to oscilloscope
            trigger_scope: sets trigger level for scope (buggy)
            read_scope: collects data from oscilloscope
            close_scope: closes connection to oscilloscope
            use_wavegen: outputs function at wavegen
            close_wavegen: closes connection to wavegen
            disconnect: closes connection to ADS
    oscilloscope_run (function): opens connection to and collects data from scope
    fft (function): returns a fast fourier transform of input data
    demodulate (function): not implemented
    snr (function): not implemented
    wavegen_functions (dict): easy names to access major types of functions wavegen can output
"""
import traceback
import numpy as np
import matplotlib.pyplot as plt
from WF_SDK import device
from WF_SDK import scope
from WF_SDK import wavegen
from ads import ADSHardware

def oscilloscope_run(ads_object: ADSHardware, n_points: int, channel: int, sampling_freq=1e6):
    """Collects data from the oscilloscope.

    Args:
        ads_object (ADSHardware object): the ADS being used
        n_points (int): number of data points to collect; 1000-2000 is a good starting point
        channel (int): which channel to collect data from
        sampling_freq (int, optional): How frequently the oscilloscope will sample
        from the input. Defaults to 1e6. You can decrease this if you have too
        many data points/the function is taking awhile to run for the time scale you need.
        (16e3 can be a reasonable selection.)

    Returns:
        data (dict): has two keys, "x" and "y" which have time (ms) and voltage (V) data
    """
    #test 16 khz, 1 mhz as well for sampling_freq
    data = {}
    ads_object.open_scope(sample_freq=sampling_freq)
    buffer = ads_object.read_scope(channel=channel)
    data["y"] = np.mean(buffer)
    data["x"] = np.array([0])
    for i in range(n_points):
        buffer = np.mean(ads_object.read_scope(channel=channel))
        data["y"] = np.append(data["y"], buffer)
        #MODIFY THE LINE BELOW THIS ONE IN L10.2(c)
        data["x"] = np.append(data["x"], np.array([i]))
    ads_object.close_scope()
    return data

def fft(data: dict):
    """Takes an FFT of input data.

    Args:
        data (dict): Provides x data in ms and y data in V obtained from oscilloscope.
    Returns:
        fft_result (dict): a dictionary with two keys, "frequencies" and "magnitudes",
                            containing the frequencies and magnitudes from the FFT.
    """
    fft_result = {}
    #FILL IN THIS FUNCTION FOR L10.3(b) and L10.3(c)

    fft_result["frequencies"] = ...
    fft_result["magnitudes"] = ...

    return fft_result

def demodulate(data: dict, envelope: dict):
    """Not implemented.

    Args:
        data (_type_): _description_
        envelope (_type_): _description_

    Returns:
        _type_: _description_
    """
    demodulated_data = ...
    return demodulated_data

def snr_calc(data):
    """Not implemented.

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    snr = ...
    return snr

wavegen_functions = {"sine":wavegen.function.sine, "square":wavegen.function.square,
                     "triangle":wavegen.function.triangle}

if __name__ == "__main__":
    ads = ADSHardware()
    ads.startup()

    try:
        ads.use_wavegen(channel=1, function=wavegen_functions["sine"], offset_v=0, freq_hz=1e3, amp_v=1)
        ### FILL IN THIS LINE FOR L10.2(a)
        raw_data = ...
        ads.close_wavegen()

        ### UNCOMMENT THIS CODE FOR L10.3(a)
        #fft_data = fft(raw_data)

        ### UNCOMMENT THIS CODE FOR L10.2(b)
        #plt.plot(raw_data["x"], raw_data["y"])
        #plt.xlabel('Time (ms)')
        #plt.ylabel('Voltage (V)')
        #plt.show()

        ### PLOT YOUR DATA HERE FOR L10.3(d)
    except Exception:
        #allows you to see errors while ensuring that connections closed
        traceback.print_exc()
        ads.close_scope()
        ads.close_wavegen()
        ads.disconnect()
