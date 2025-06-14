import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock
import adi

class Ad9361Rx(BaseBlock):

    def __init__(self, name, dspCore, ad9361):
        super().__init__(name, dspCore)
        self.mType = "IgAd9361"
        self.mAd9361 = ad9361
        self.mByPass = False
        self.mConfigDone = False

    def Config(self, bypass, fs = 1000000, buffer_size = 1024, rf_bw = 4000000, rf_gain = "slow_attack", lo_freq = 915e6):
        self.mByPass = bypass
        self.mAd9361.rx_enabled_channels = ['voltage0', 'voltage1']
        self.mAd9361.rx_buffer_size = buffer_size
        self.mAd9361.sample_rate = int(fs)
        self.mAd9361.rx_lo = int(lo_freq)
        self.mAd9361.rx_rf_bandwidth = int(rf_bw)
        if isinstance(rf_gain, str):
            if rf_gain != "slow_attack" and rf_gain != "fast_attack":
                ExitError(self.mName + " - Wrong gain configuration -> choose slow_attack, fast_attack or integer (for manual configuration)")
            self.mAd9361.gain_control_mode_chan0 = rf_gain
            self.mAd9361.gain_control_mode_chan1 = rf_gain
        else:
            self.mAd9361.gain_control_mode_chan0 = "manual"
            self.mAd9361.gain_control_mode_chan1 = "manual"
            self.mAd9361.rx_hardwaregain_chan0 = float(rf_gain)
            self.mAd9361.rx_hardwaregain_chan1 = float(rf_gain)
        self.mAd9361.rx_destroy_buffer()
        self.mConfigDone = True

    def Process(self):
        samples = self.mAd9361.rx()
        self.mOutput = np.array(samples).astype(np.complex64)

    def Help(self):
        print("Ad9361Rx block Process:")
        print(" -> Pluto SDR RX block using pyadi-iio with ad9361 rf front end FW")
        print("Config(bypass, fs = 1000000, buffer_size = 1024, rf_bw = 4000000, rf_gain = \"slow_attack\", lo_freq = 2000000000):")
        print(" -> bypass: if True, input is passed to output without reading from SDR")
        print(" -> fs: sampling rate in Hz")
        print(" -> buffer_size: number of samples per Process call")
        print(" -> rf_bw: RF filter bandwidth in Hz")
        print(" -> rf_gain: 'slow_attack', 'fast_attack', or numeric gain value (manual mode)")
        print(" -> lo_freq: LO frequency in Hz")