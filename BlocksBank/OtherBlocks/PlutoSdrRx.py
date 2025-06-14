import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock
import adi

class PlutoSdrRx(BaseBlock):

    def __init__(self, name, dspCore, sdr):
        super().__init__(name, dspCore)
        self.mType = "IgPlutoSdrRx"
        self.mSdr = sdr
        self.mByPass = False
        self.mConfigDone = False

    def Config(self, bypass, fs = 1000000, buffer_size = 1024, rf_bw = 4000000, rf_gain = "slow_attack", lo_freq = 915e6):
        self.mByPass = bypass
        self.mSdr.rx_buffer_size = buffer_size
        self.mSdr.sample_rate = int(fs)
        self.mSdr.rx_lo = int(lo_freq)
        self.mSdr.rx_rf_bandwidth = int(rf_bw)
        if isinstance(rf_gain, str):
            if rf_gain != "slow_attack" and rf_gain != "fast_attack":
            self.mSdr.gain_control_mode = rf_gain
        else:
            self.mSdr.gain_control_mode = "manual"
            self.mSdr.rx_hardwaregain = float(rf_gain)
        self.mSdr.rx_destroy_buffer()
        self.mConfigDone = True

    def Process(self):
        samples = self.mSdr.rx()
        self.mOutput = np.array(samples).astype(np.complex64)

    def Help(self):
        print("PlutoSdrRx block Process:")
        print(" -> Pluto SDR RX block using pyadi-iio")
        print("Config(bypass, fs = 1000000, buffer_size = 1024, rf_bw = 4000000, rf_gain = \"slow_attack\", lo_freq = 2000000000):")
        print(" -> bypass: if True, input is passed to output without reading from SDR")
        print(" -> fs: sampling rate in Hz")
        print(" -> buffer_size: number of samples per Process call")
        print(" -> rf_bw: RF filter bandwidth in Hz")
        print(" -> rf_gain: 'slow_attack', 'fast_attack', or numeric gain value (manual mode)")
        print(" -> lo_freq: LO frequency in Hz")