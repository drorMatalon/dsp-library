import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock
import adi

class PlutoSdrTx(BaseBlock):

    def __init__(self, name, dspCore, sdr):
        super().__init__(name, dspCore)
        self.mType = "OgPlutoSdrTx"
        self.mSdr = sdr
        self.mByPass = False
        self.mConfigDone = False

    def Config(self, bypass, fs = 1000000, buffer_size = 1024, rf_bw = 4000000, rf_gain = -40, lo_freq = 915e6):
        self.mByPass = bypass
        self.mSdr.tx_buffer_size = buffer_size
        self.mSdr.sample_rate = int(fs)
        self.mSdr.tx_lo = int(lo_freq)
        self.mSdr.tx_rf_bandwidth = int(rf_bw)
        self.mSdr.tx_hardwaregain_chan0 = float(rf_gain)
        self.mSdr.tx_destroy_buffer()
        self.mConfigDone = True

    def TransmitSignal(self, signal):
        self.mInput = signal
        self.CallProcess()

    def Process(self):
        self.mSdr.tx_destroy_buffer()
        self.mSdr.tx_cyclic_buffer = True
        self.mSdr.tx(np.array(self.mInput).astype(np.complex64))

    def Help(self):
        print("PlutoSdrTx block Process:")
        print(" -> Pluto SDR TX block using pyadi-iio")
        print("TransmitSignal(signal):")
        print(" -> transmite the input signal in loops")
        print("Config(bypass, fs = 1000000, buffer_size = 1024, rf_bw = 4000000, rf_gain = -40, lo_freq = 2000000000):")
        print(" -> bypass: if True, input is passed to output without reading from SDR")
        print(" -> fs: sampling rate in Hz")
        print(" -> buffer_size: number of samples per Process call")
        print(" -> rf_bw: RF filter bandwidth in Hz")
        print(" -> rf_gain: numeric gain value")
        print(" -> lo_freq: LO frequency in Hz")