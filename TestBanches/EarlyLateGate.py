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
dspCore.DBG(2, "W")

sdr = adi.Pluto("ip:192.168.2.1")

fs = 1000000
int_factor = 100

# ~~~~~~~~~~~~~~~~~~
# system decleration
# ~~~~~~~~~~~~~~~~~~

preamble = BbPreamble("preamble", dspCore)
Interpulation = BbInterpulator("Interpulation", dspCore)
Fir0 = BbFir("pulse_shape", dspCore)
sdrTx = PlutoSdrTx("sdrTx", dspCore, sdr)

sdrRx = PlutoSdrRx("sdrRx", dspCore, sdr)
Fir1 = BbFir("matched_filter", dspCore)
EarlyLateGate = BbEarlyLateGate("EarlyLateAlgo", dspCore)
FrameSync = BbFrameSync("FrameSync", dspCore)
Scope = Analyzer("Analyzer", dspCore)

dspCore.Connect("preamble", "Interpulation", "pulse_shape", "sdrTx")
dspCore.Connect("sdrRx", "matched_filter", "EarlyLateAlgo", "FrameSync", "Analyzer")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# configuration and initializtion
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pulse = np.exp(-(np.arange(int_factor) - (int_factor // 2))**2 / (2 * (int_factor // 7) ** 2))
sync_sequence = np.array([1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1])

BPSK = [-1, 1, -1, 1, 1, -1, -1, 1]
QAM4 = [1 + 1j, -(1 + 1j), 1 + 1j, -(1 + 1j), 1 - 1j, -(1 - 1j), 1 - 1j, -(1 - 1j)]

s = BPSK
s = 2 ** 14 * np.array((s + s + s + s + s + s + s + s + s))

preamble.Config(False, 2 ** 14 * sync_sequence)
Interpulation.Config(False, int_factor)
Fir0.Config(False, pulse)
sdrTx.Config(False, fs = 1000000, rf_gain = -30, buffer_size = 2 ** 13)

sdrRx.Config(False, fs = 1000000, rf_gain = 30, buffer_size = 2 ** 13)
Fir1.Config(False, pulse)
EarlyLateGate.Config(False, int_factor, 11, 3)
FrameSync.Config(False, sync_sequence, True)

# ~~~~~~~~~~
# Activation
# ~~~~~~~~~~


preamble.mInput = s
Scope.Config("amplitude", fs * int_factor)
preamble.CallProcess()
sdrRx.CallProcess()
plt.pause(5)

Scope.Config("constellation", fs * int_factor)
Scope.CallProcess()
plt.pause(5)