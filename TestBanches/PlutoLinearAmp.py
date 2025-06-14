import numpy as np
from BlocksBank.BeamForming import *
from BlocksBank.DigitalComm import *
from BlocksBank.BaseBlocks import *
from BlocksBank.OtherBlocks import *
from BlocksBank.CommonFun import *
import matplotlib.pyplot as plt
import adi
import scipy

# ~~~~~~~~~~~~~~~~~~~~~~~~~
# before system decleration
# ~~~~~~~~~~~~~~~~~~~~~~~~~

dspCore = DspCore()
dspCore.DBG(1, "W")

sdr = adi.Pluto("ip:192.168.2.1")

samples_num = 1024 * 4
fs = 1000000
fc = fs / 40
dec_factor = 2
avarage_width = 50

def EdgeDetect(self):
    abs_sig = np.abs(self.mInput)
    taps = scipy.signal.firwin(numtaps = 100, cutoff = fc * 1.5, width = 0.4 * fc, fs = fs, window="hamming")
    filt_abs_sig = np.convolve(abs_sig, taps, mode = "same")
    taps = np.ones(avarage_width) / avarage_width
    filt_cleaned_abs_sig = np.convolve(filt_abs_sig, taps, mode = "same")    
    self.mOutput = filt_cleaned_abs_sig

def DcRemoval(self):
    mean = np.mean(self.mInput)
    self.mOutput = self.mInput - mean
    #self.mOutput = self.mInput

# ~~~~~~~~~~~~~~~~~~
# system decleration
# ~~~~~~~~~~~~~~~~~~

sdrTx = PlutoSdrTx("SdrTx", dspCore, sdr)

sdrRx = PlutoSdrRx("SdrRx", dspCore, sdr)
decimator = BbDecimator("decimator", dspCore)
tmp_block_0 = BbTemplateBlock("temp_block_0", dspCore, EdgeDetect)
tmp_block_1 = BbTemplateBlock("temp_block_1", dspCore, DcRemoval)

analyzer = Analyzer("Scope_0", dspCore)

dspCore.Connect("SdrRx", "decimator", "temp_block_1", "temp_block_0", "Scope_0")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# configuration and initializtion
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sdrTx.Config(False, fs = 1000000, rf_gain = -35, buffer_size = samples_num)

sdrRx.Config(False, fs = 1000000, rf_gain = 20, buffer_size = samples_num)
decimator.Config(False, dec_factor)
analyzer.Config("amplitude", fs / dec_factor)

# ~~~~~~~~~~
# Activation
# ~~~~~~~~~~

N = samples_num
Ts = 1 / fs
t = np.linspace(0, N-1, N) * Ts
i = 1000 * t / (N * Ts) * np.sin(2 * np.pi * t * fc)
q = 0
iq = i + 1j * q

sdrTx.TransmitSignal(iq)
sdrRx.CallProcess()
plt.pause(5)

analyzer.Config("spectrum", fs / dec_factor)
analyzer.CallProcess()
plt.pause(5)

del sdr