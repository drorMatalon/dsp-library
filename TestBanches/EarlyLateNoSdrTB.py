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

fs = 1
int_factor = 40

# ~~~~~~~~~~~~~~~~~~
# system decleration
# ~~~~~~~~~~~~~~~~~~

preamble = BbPreamble("preamble", dspCore)
Interpulation = BbInterpulator("Interpulation", dspCore)
Fir0 = BbFir("pulse_shape", dspCore)
Fir1 = BbFir("matched_filter", dspCore)
EarlyLateGate = BbEarlyLateGate("EarlyLateAlgo", dspCore)
FrameSync = BbFrameSync("FrameSync", dspCore)
Scope = Analyzer("Analyzer", dspCore)

dspCore.Connect("preamble", "Interpulation", "pulse_shape", "matched_filter", "EarlyLateAlgo", "FrameSync", "Analyzer")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# configuration and initializtion
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pulse = np.exp(-(np.arange(int_factor) - (int_factor // 2))**2 / (2 * (int_factor // 7) ** 2))
sync_sequence = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
padded_sync_sequence = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1] + sync_sequence

s = [1, -1, 1, 1, -1, -1, 1, 1, -1, -1]
signal = np.array((s + s + s + s + s + s + s + s))

preamble.Config(False, padded_sync_sequence)
Interpulation.Config(False, int_factor)
Fir0.Config(False, pulse)
Fir1.Config(False, pulse)
EarlyLateGate.Config(False, int_factor, 7, 1)
FrameSync.Config(False, sync_sequence, False)

# ~~~~~~~~~~
# Activation
# ~~~~~~~~~~


preamble.mInput = signal
Scope.Config("amplitude", fs * int_factor)
preamble.CallProcess()
plt.pause(5)

Scope.Config("constellation", fs * int_factor)
Scope.CallProcess()
plt.pause(5)