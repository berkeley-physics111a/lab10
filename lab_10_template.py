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
import time
import numpy as np
import matplotlib.pyplot as plt
from WF_SDK import device
from WF_SDK import scope
from WF_SDK import wavegen

class ADSHardware():
    """Class of functions for interfacing with the ADS.
    """

    def __init__(self):
        self.handle = None

    def startup(self):
        """Connects to the ADS. Defines 'handle', the address to the ADS.
        Must be run at the beginning of every program using the ADS.
        """
        self.handle = device.open()

    def open_scope(self, buffer_size=1000, sample_freq=1e6):
        """Opens connection to the scope.

        Args:
            buffer_size (int, optional): How many data points are temporarily stored
            before being returned. The buffer is a temporary slot for storing a small amount of
            data before it is transferred to its final destination. Defaults to 1000.
            sample_freq (int, optional): How frequently the oscilloscope will sample
            from the input. Defaults to 1e6. You can decrease this if you have too
            many data points/the function is taking awhile to run for the time scale you need.
            (16e3 can be a reasonable selection.)
        """
        scope.open(self.handle, buffer_size=buffer_size, sampling_frequency=sample_freq)

    def trigger_scope(self, channel=1, level=0.1):
        """Sets trigger level for the scope. Kind of a buggy function; not used.

        Args:
            channel (int, optional): Selects which channel of scope to read out. 
            Defaults to 1.
            level (float, optional): Sets trigger level for scope. Defaults to 0.1.
        """
        scope.trigger(self.handle, enable=True, source=scope.trigger_source.analog, channel=channel,
                      edge_rising=True, level=level)

    def read_scope(self, channel=1):
        """Collects data from the scope.

        Args:
            channel (int, optional): Which channel to read from. Defaults to 1.

        Returns:
            buffer (array): An array of output data points. The buffer is a temporary slot 
            for storing a small amount of data before it is transferred to its final destination.
        """
        buffer = scope.record(self.handle, channel=channel)
        return buffer

    def close_scope(self):
        """Closes connection to the scope.
        """
        scope.close(self.handle)

    def use_wavegen(self, channel=1, function=wavegen.function.sine, offset_v=0, freq_hz=1e3, amp_v=1):
        """Runs the wavegen producing function with given parameters.

        Args:
            channel (int, optional): Which channel output is at. Defaults to 1.
            function (function object, optional): What type of function to output. 
            Defaults to wavegen.function.sine.
            offset (int, optional): Voltage offset (V). Defaults to 0.
            freq (int, optional): Frequency (Hz). Defaults to 1e3.
            amp (int, optional): Amplitude (V). Defaults to 1.
        """
        wavegen.generate(self.handle, channel=channel, function=function, offset=offset_v,
                         frequency=freq_hz, amplitude=amp_v)

    def close_wavegen(self):
        """Closes wavegen.
        """
        wavegen.close(self.handle)

    def disconnect(self):
        """Closes ADS connection. Must be run at the end of every program.
        """
        device.close(self.handle)

def oscilloscope_run(ads_object: ADSHardware, n_points: int, channel: int, sampling_freq=1e6, buffer_size=1000):
    """Collects data from the oscilloscope.

    Args:
        ads_object (ADSHardware object): the ADS being used
        n_points (int): number of data points to collect; 1000-2000 is a good starting point
        channel (int): which channel to collect data from
        sampling_freq (int, optional): How frequently the oscilloscope will sample
        from the input. Defaults to 1e6. You can decrease this if you have too
        many data points/the function is taking awhile to run for the time scale you need.
        (16e3 can be a reasonable selection.)
        buffer_size (int): Defaults to 1000. Number of points oscilloscope gets at a time.

    Returns:
        data (dict): has two keys, "x" and "y" which have time (ms) and voltage (V) data
        This function works by pulling a buffer n_points times. The time between points in
        the buffer is determined by the sampling frequency, and the time between buffers is
        determined by how long it takes the code to run - this is recorded in loop_offset_time,
        which records how 'offset' each buffer is from 0 time. The contents of the buffer are
        averaged to reduce noise.
    """
    data = {}
    ads_object.open_scope(sample_freq=sampling_freq, buffer_size=buffer_size)
    data["y"] = np.zeros(n_points)
    data["x"] = np.zeros(n_points)
    loop_offset_time = 0
    loop_start_time = time.time()
    for i in range(n_points):
        buffer_mean, loop_offset_time = np.mean(ads_object.read_scope(channel=channel)), time.time() - loop_start_time
        data["y"][i] = buffer_mean
        MS_CONVERSION = 1e3
        #MODIFY THE LINE BELOW THIS ONE IN L10.2(d)
        data["x"][i] = i
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
