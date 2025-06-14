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

fs = 1000000
dec_factor = 1

def Gain(self):
    self.mOutput = 1 * self.mInput

# ~~~~~~~~~~~~~~~~~~
# system decleration
# ~~~~~~~~~~~~~~~~~~

sdrTx = PlutoSdrTx("SdrTx", dspCore, sdr)

sdrRx = PlutoSdrRx("SdrRx", dspCore, sdr)
decimator = BbDecimator("decimator", dspCore)
block_0 = BbTemplateBlock("Gain_0", dspCore, Gain)
block_1 = BbTemplateBlock("Gain_1", dspCore, Gain)

analyzer = Analyzer("Scope_0", dspCore)

dspCore.Connect("SdrRx", "decimator", "Gain_0", "Gain_1", "Scope_0")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# configuration and initializtion
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sdrTx.Config(False, fs = 1000000, rf_gain = -40)

sdrRx.Config(False, fs = 1000000, rf_gain = 20)
decimator.Config(False, dec_factor)
analyzer.Config("amplitude", fs / dec_factor)

# ~~~~~~~~~~
# Activation
# ~~~~~~~~~~

N = 1024
fc = int(2 * 10000)
ts = 1 / float(fs)
t = np.arange(0, N * ts, ts)
i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq = i + 1j * q

sdrTx.TransmitSignal(iq)
sdrRx.CallProcess()
plt.pause(4)

analyzer.Config("spectrum", fs / dec_factor)
analyzer.CallProcess()
plt.pause(4)

analyzer.Config("constellation", fs / dec_factor)
sdrRx.CallProcess()
plt.pause(4)

del sdr