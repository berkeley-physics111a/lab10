"""Physics 111A Lab 10 functions.
Written by Auden Young, 11/2025.

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
    demod_radio (function): demodulates a signal like we did for AM radio
    demod_lockin (function): does phase locked demodulation
    wavegen_functions (dict): easy names to access major types of functions wavegen can output
"""
import traceback
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
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

def oscilloscope_run(ads_object: ADSHardware, duration: int, channel: int, sampling_freq=500):
    """Collects data from the oscilloscope.

    Args:
        ads_object (ADSHardware object): the ADS being used
        duration (int): time length of trace to collect in seconds
        channel (int): which channel to collect data from
        sampling_freq (int, optional): How frequently the oscilloscope will sample
        from the input. Defaults to 1e6. You can decrease this if you have too
        many data points/the function is taking awhile to run for the time scale you need.
        (16e3 can be a reasonable selection.)

    Returns:
        data (dict): has two keys, "x" and "y" which have time (ms) and voltage (V) data
    """
    buffer_size = int(duration * sampling_freq)
    data = {}
    ads_object.open_scope(sample_freq=sampling_freq, buffer_size=buffer_size)

    MS_CONVERSION = 1e3

    buffer = ads_object.read_scope()
    data["y"] = buffer

    # MODIFY THE LINE BELOW THIS ONE IN L10.2(d)
    data["x"] = np.arange(buffer_size)

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
    MS_CONVERSION = 1e3
    #avg_timestep below may be helpful for your call to np.fft.fftfreq...
    avg_timestep = np.mean(np.diff(data["x"])/MS_CONVERSION)

    fft_result["frequencies"] = ...
    fft_result["magnitudes"] = ...

    return fft_result

def butter_lowpass_filter(data, cutoff: float, fs: float, order=5):
    """Creates and applies a lowpass filter.

    Args:
        data (list): Provides y data in V obtained from oscilloscope.
        cutoff (float): 3 dB frequency (Hz) for low pass filter.
        fs (float): Sampling frequency data was taken at.
        order (int, optional): Order of the filter. Defaults to 5.

    Returns:
        list: Low pass filtered data in V.
    """
    # Define lowpass filter coefficients using butter function in scipy.signal package
    b, a = sig.butter(order, cutoff, btype='lowpass', analog=False, fs=fs, output='ba')
    # Applies lowpass filter using scipy.signal.filtfilt function
    y = sig.filtfilt(b, a, data)
    return y

def demodulate_radio(data: dict, nu_3db: float, save=True):
    """Demodulate signal using the strategy we used for the AM radio.
    That is, first subtract the mean of the data, then do a lowpass filter.

    Args:
        data (dict): Provides x data in ms and y data in V obtained from oscilloscope.
        nu (float): 3 dB frequency (Hz) for low pass filter.
        save (bool, optional): Whether or not to save data to file. Defaults to True.

    Returns:
        demod_data (dict): has two keys, "x" and "y" which have time (ms) and voltage (V) data
    """
    demod_data = {}
    demod_data["x"] = data["x"]
    MILLISECOND_CONVERSION = 1e3

    #calculates average sampling frequency for digital filter
    fs = len(data["x"] - 1)*MILLISECOND_CONVERSION / (data["x"][-1] - data["x"][0])

    #FILL IN THESE LINES FOR L10.5(c)
    dc_offset_remove = ... #remove dc offset
    rectified_data = ... #rectify
    demod_data["y"] = ... #low pass

    #plot the different steps
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(demod_data["x"], data["y"])
    axs[0, 0].set_title('Raw Signal (Vout)')
    axs[0, 1].plot(demod_data["x"], dc_offset_remove, 'tab:orange')
    axs[0, 1].set_title('DC Offset Removed')
    axs[1, 0].plot(demod_data["x"], rectified_data, 'tab:green')
    axs[1, 0].set_title('Rectified (Vout1)')
    axs[1, 1].plot(demod_data["x"], demod_data["y"], 'tab:red')
    axs[1, 1].set_title('Low Pass Filtered (Vout2)')

    for ax in axs.flat:
        ax.set(xlabel='Time (ms)', ylabel='Voltage (V)')
        ax.grid(visible=True, which='major', color='black', linestyle='-')
        ax.grid(visible=True, which='minor', color='black', linestyle='--')
    
    for ax in axs.flat:
        ax.label_outer()
    
    plt.show()

    #save the data if desired
    if save:
        fname = os.path.join('./heartbeat_data', 'demod_lockin'+time.strftime("%Y%m%d-%H%M%S")+".txt")
        save_array = np.array([demod_data["x"], demod_data["y"]])
        np.savetxt(fname, save_array)

    return demod_data

def demodulate_lockin(ads_object: ADSHardware, nu_mod: float, nu_3db: float, duration=5, channel=1, save=True):
    """Demodulate signal the way a lock in amplifier would, taking advantage
    of the fact that we can phase match.

    Args:
        ads_object (ADSHardware): the ADS being used.
        nu_mod (float): Modulation frequency (Hz). 100 recommended starting point.
        nu_3db (float): 3 dB frequency for low pass (Hz).
        duration (int, optional): Number of seconds to record for. Defaults to 5.
        channel (int, optional): Channel to read oscilloscope on. Defaults to 1.
        save (bool, optional): Whether or not to save data to file. Defaults to True.

    Returns:
        dict: _description_
    """
    MILLISECOND_CONVERSION = 1e3
    omega = 2*np.pi*nu_mod

    #we have to start the wavegen and oscilloscope read right after each other
    #in order to achieve phase locking
    test = ads.use_wavegen(channel=1, 
                    function=wavegen_functions["sine"], 
                    offset_v=2.75, 
                    freq_hz=nu_mod, 
                    amp_v=1)
    data = oscilloscope_run(ads_object, channel=channel, duration=duration)
    ads_object.close_wavegen()

    #calculates average sampling frequency for digital filter
    fs = len(data["x"] - 1)*MILLISECOND_CONVERSION / (data["x"][-1] - data["x"][0])

    demodulated_data = {}
    demodulated_data["x"] = data["x"]

    #calculate the cos and sin components of the local oscillator
    #i.e. what is being produced by wavegen
    demodulated_data["local_oscillator_cos"] = np.cos(omega*data["x"]/MILLISECOND_CONVERSION)
    demodulated_data["local_oscillator_sin"] = np.sin(omega*data["x"]/MILLISECOND_CONVERSION)

    #FILL IN THE BLANKS BELOW FOR L10.6(a)
    #finds the cos and sin components of the signal read on the scope
    demodulated_data["sin"] = ...
    demodulated_data["cos"] = ...

    #low pass filters the data
    demodulated_data["lowpass_sin"] = ...
    demodulated_data["lowpass_cos"] = ...

    #adds sin and cos components in quadrature to obtain the demodulated signal
    demodulated_data["y"] = np.sqrt(demodulated_data["lowpass_cos"]**2 + demodulated_data["lowpass_sin"]**2)

    #plot the steps to get demodulated signal
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(demodulated_data["x"], data["y"])
    axs[0, 0].set_title('Raw Signal')
    axs[0, 1].plot(demodulated_data["x"], demodulated_data["sin"], 'tab:orange')
    axs[0, 1].plot(demodulated_data["x"], demodulated_data["cos"], 'tab:green')
    axs[0, 1].set_title('Sin & Cos components')
    axs[1, 0].plot(demodulated_data["x"], demodulated_data["local_oscillator_cos"])
    axs[1, 0].plot(demodulated_data["x"], demodulated_data["local_oscillator_sin"])
    axs[1, 0].set_title('Local oscillator')
    axs[1, 1].plot(demodulated_data["x"], demodulated_data["lowpass_cos"])
    axs[1, 1].plot(demodulated_data["x"], demodulated_data["lowpass_sin"])
    axs[1, 1].set_title("Filtered sin & cos components")

    for ax in axs.flat:
        ax.set(xlabel='Time (ms)', ylabel='Voltage (V)')
        ax.grid(visible=True, which='major', color='black', linestyle='-')
        ax.grid(visible=True, which='minor', color='black', linestyle='--')
    
    for ax in axs.flat:
        ax.label_outer()
    
    plt.show()

    #plot the final demodulated signal
    plt.plot(demodulated_data["x"], demodulated_data["y"])
    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (V)")
    plt.show()

    #save the data if desired
    if save:
        fname = os.path.join('./heartbeat_data', 'demod_lockin'+time.strftime("%Y%m%d-%H%M%S")+".txt")
        save_array = np.array([demodulated_data["x"], demodulated_data["y"]])
        np.savetxt(fname, save_array)

    return demodulated_data

wavegen_functions = {"sine":wavegen.function.sine, "square":wavegen.function.square,
                     "triangle":wavegen.function.triangle, "dc":wavegen.function.dc}

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

        ### DC BASEBAND
        # UNCOMMENT THE CODE BELOW FOR 10.5(b) (i.e., remove the ''' at top and bottom)
        '''
        ads.use_wavegen(channel=1,
                        function=wavegen_functions["dc"],
                        offset_v=2.75)
        time.sleep(1) #so everything can 'settle' before data is collected

        dc_baseband_data = oscilloscope_run(ads, duration=5, channel=1)

        plt.plot(dc_baseband_data["x"], dc_baseband_data["y"])
        plt.grid(visible=True, which='major', color='black', linestyle='-')
        plt.grid(visible=True, which='minor', color='black', linestyle='--')
        plt.xlabel('Time (ms)')
        plt.ylabel('Voltage (V)')
        plt.title("DC Baseband Data")
        plt.show()

        fname = os.path.join('./heartbeat_data', 'demod_lockin'+time.strftime("%Y%m%d-%H%M%S")+".txt")
        np.savetxt(fname, np.array([dc_baseband_data["x"], dc_baseband_data["y"]]))

        fft_dc_baseband = fft(dc_baseband_data)

        plt.plot(fft_dc_baseband["frequencies"], fft_dc_baseband["magnitudes"])
        plt.xlabel("Frequencies (Hz)")
        plt.ylabel("Voltage (V)")
        plt.grid(visible=True, which='major', color='black', linestyle='-')
        plt.grid(visible=True, which='minor', color='black', linestyle='--')
        plt.title("FFT of DC Baseband Data")
        plt.show()
        '''

        ### DEMOD RADIO
        # UNCOMMENT THE CODE BELOW FOR L10.5(f) and fill in nu_3db
        '''
        demod_data_radio = demodulate_radio(raw_data, nu_3db=...)

        fft_demod_radio = fft(demod_data_radio)
        plt.plot(fft_demod_radio["frequencies"], fft_demod_radio["magnitudes"])
        plt.xlabel("Frequencies (Hz)")
        plt.ylabel("Voltage (V)")
        plt.grid(visible=True, which='major', color='black', linestyle='-')
        plt.grid(visible=True, which='minor', color='black', linestyle='--')
        plt.title("FFT Demod Radio")
        plt.show()
        '''

        ### DEMOD LOCKIN
        # UNCOMMENT THE LINE BELOW FOR L10.6(b)
        #demod_data_lockin = demodulate_lockin(ads, duration=5, nu_mod=..., nu_3db=...)

        ### APPROACH COMPARISON

        #if you want to use data from a different run, uncomment the following lines
        #dc_baseband_data["x"], dc_baseband_data["y"] = np.loadtxt("./heartbeat_data/FILENAME")
        #demod_data_radio["x"], demod_data_radio["y"] = np.loadtxt("./heartbeat_data/FILENAME")
        #demod_data_lockin["x"], demod_data_lockin["y"] = np.loadtxt("./heartbeat_data/FILENAME")

        # UNCOMMENT THE CODE BELOW FOR L10.6(c)
        '''
        fig, axs = plt.subplots([3, 1])
        axs[0].plot(dc_baseband_data["x"], dc_baseband_data["y"])
        axs[0].set_title("DC Baseband")
        axs[1].plot(demod_data_radio["x"], demod_data_radio["y"])
        axs[1].set_title("Demod Radio")
        axs[2].plot(demod_data_lockin["x"], demod_data_lockin["y"])
        axs[2].set_title("Demod Lockin")

        for ax in axs.flat:
            ax.set(xlabel='Time (ms)', ylabel='Voltage (V)')
            ax.grid(visible=True, which='major', color='black', linestyle='-')
            ax.grid(visible=True, which='minor', color='black', linestyle='--')
        
        for ax in axs.flat:
            ax.label_outer()
        
        plt.show()
        '''

    except Exception:
        #allows you to see errors while ensuring that connections closed
        traceback.print_exc()
        ads.close_scope()
        ads.close_wavegen()
        ads.disconnect()
