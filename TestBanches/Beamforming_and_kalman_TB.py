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
dspCore.DBG(0, "W")

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
KALMAN = BbKalmanFilter("KalmanFilter", dspCore)
Scope = Analyzer("Analyzer", dspCore)
dspCore.Connect("LinearPhasedArray", "BeamScan", "Music", "KalmanFilter")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Configuration and initialization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

angles = np.linspace(-90, 90, 181)
LPA.Config(bypass=False, carrier_freq=fc, ant_dist=d, ant_num=num_antennas, theta=true_angle_deg, noise_power = 4)
BS.Config(bypass=False, carrier_freq=fc, ant_dist=d, mode="doa", angles_range=angles)
MUSIC.Config(bypass=True, carrier_freq=fc, ant_dist=d, angles_range=angles)
KALMAN.Config(bypass = False, fs = fs, 
              measurement_variance = 8, 
              process_variance = 0.01, 
              init_pos = 10,  
              init_vel = 0, 
              init_pos_var = 180, 
              init_vel_var = 0)
Scope.Config("amplitude", fs)

# ~~~~~~~~~~
# Activation
# ~~~~~~~~~~

t = np.arange(num_snapshots) / fs
base_signal = np.exp(1j * 2 * np.pi * 1e5 * t)

LPA.mInput = base_signal
for i in range(20):
    LPA.CallProcess()
    doa_estimation = MUSIC.mOutput
    kalmans_estimation = KALMAN.mOutput
    print("True angle: " + str(true_angle_deg) + ", Kalmns estimated angle: " + str(kalmans_estimation) + ", DOA Estimation: " + str(doa_estimation))