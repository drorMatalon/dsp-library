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
# Before system declaration
# ~~~~~~~~~~~~~~~~~~~~~~~~~

dspCore = DspCore()
dspCore.DBG(2, "W")

fs = 1e6
fc = 3e9
wavelength = 3e8 / fc
d = 0.5 * wavelength

true_angle_deg = -10
num_antennas = 2
num_snapshots = 100

# ~~~~~~~~~~~~~~~~~~
# System declaration
# ~~~~~~~~~~~~~~~~~~

LPA = BbLinearPhasedArray("LinearPhasedArray", dspCore)
BS = BbBeamScan("BeamScan", dspCore)
MUSIC = BbMusic("Music", dspCore)
Scope = Analyzer("Analyzer", dspCore)

dspCore.Connect("LinearPhasedArray", "BeamScan", "Music")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Configuration and initialization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

angles = np.linspace(-90, 90, 181)
LPA.Config(bypass=False, carrier_freq=fc, ant_dist=d, ant_num=num_antennas, theta=true_angle_deg, noise_power = 0)
BS.Config(bypass=False, carrier_freq=fc, ant_dist=d, mode="doa", angles_range=angles)
MUSIC.Config(bypass=True, carrier_freq=fc, ant_dist=d, angles_range=angles)
Scope.Config("amplitude", fs)

# ~~~~~~~~~~
# Activation
# ~~~~~~~~~~

t = np.arange(num_snapshots) / fs
base_signal = np.exp(1j * 2 * np.pi * 1e5 * t)

LPA.mInput = base_signal
LPA.CallProcess()

estimated_theta_deg = MUSIC.mOutput
print(f"True angle: {true_angle_deg:.1f}, Estimated angle: {estimated_theta_deg:.2f}")
