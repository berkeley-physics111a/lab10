import ctypes
import faulthandler
import logging

from WF_SDK import device
from WF_SDK import scope
from WF_SDK import wavegen

# initialize a log handle
# Docs: https://docs.python.org/3/library/logging.html
logger = logging.getLogger(__name__)

# faulthandler.enable() installs fault handlers that dump traceback on
# SIGSEGV, SIGFPE, SIGABRT, SIGBUS, and SIGILL signals
# by default, the traceback is written to sys.stderr (unbuffered)
# Docs: https://docs.python.org/3/library/faulthandler.html
# Related to: https://github.com/berkeley-physics111a/lab10/issues/2
faulthandler.enable()


class ADSHardware():
    """Class of functions for interfacing with the ADS.
    """

    def __init__(self):
        self.handle = None

    def __del__(self):
        """ 
        Called when an instance of ADSHardware is about to be destroyed, used to cleanup handles
        Docs: https://docs.python.org/3/reference/datamodel.html#object.__del__
        """
        if self.handle is not None:
            self.close_wavegen()
            self.close_scope()
            self.disconnect()

    def startup(self):
        """Connects to the ADS. Defines 'handle', the address to the ADS.
        Must be run at the beginning of every program using the ADS.
        """
        logger.warning(f"[ATTEMPT] Opening ADS device")
        self.handle = device.open()
        logger.warning(f"[SUCCESS] Opened device {self.handle.name} handle={self.handle.handle} addr={ctypes.addressof(self.handle.handle)}")

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
        addr = ctypes.addressof(self.handle.handle)
        logger.warning(f"[ATTEMPT] Closing device {self.handle.name} handle={self.handle.handle} addr={addr}")
        device.close(self.handle)
        logger.warning(f"[SUCCESS] Closed device {self.handle.name} handle={self.handle.handle} addr={addr}")
