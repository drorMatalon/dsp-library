import numpy as np
from BlocksBank.BeamForming import *
from BlocksBank.DigitalComm import *
from BlocksBank.BaseBlocks import *
from BlocksBank.OtherBlocks import *
from BlocksBank.CommonFun import *
import matplotlib.pyplot as plt
import adi
import scipy
from time import sleep

# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Before system declaration
# ~~~~~~~~~~~~~~~~~~~~~~~~~

dspCore = DspCore()
dspCore.DBG(1, "W")

fs = 1e6
fc = 3e9
wavelength = 3e8 / fc
d = 0.5 * wavelength
noise_power = 2

true_angle_deg = 0
num_antennas = 2
num_snapshots = 100

# ~~~~~~~~~~~~~~~~~~
# System declaration
# ~~~~~~~~~~~~~~~~~~

LPA = BbLinearPhasedArray("LinearPhasedArray", dspCore)
CALIBRATION = BbLpaCalibration("Calibration", dspCore)
BS = BbBeamScan("BeamScan", dspCore)
MUSIC = BbMusic("Music", dspCore)
KALMAN = BbKalmanFilter("Kalman", dspCore)
SCOPE = Analyzer("Analyzer", dspCore)

dspCore.Connect("LinearPhasedArray", "Calibration", "BeamScan", "Music", "Kalman")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Configuration and initialization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

angles = np.linspace(-90, 90, 181)
LPA.Config(bypass=False, carrier_freq=fc, ant_dist=d, ant_num=num_antennas, theta=true_angle_deg, noise_power = noise_power, phase_missmatch = [np.pi, np.pi / 2])
CALIBRATION.Config(bypass = False, ant_num = num_antennas, mode = "train")
BS.Config(bypass=False, carrier_freq=fc, ant_dist=d, mode="doa", angles_range=angles)
MUSIC.Config(bypass=True, carrier_freq=fc, ant_dist=d, angles_range=angles)
KALMAN.Config(bypass = True, fs = fs, measurement_variance = 2, process_variance = 0.01, init_pos = 0, init_vel = 0, init_pos_var = 180, init_vel_var = 180)

SCOPE.Config("amplitude", fs)

# ~~~~~~~~~~
# Activation
# ~~~~~~~~~~

t = np.arange(num_snapshots) / fs
base_signal = np.exp(1j * 2 * np.pi * 1e5 * t)

LPA.mInput = base_signal
LPA.CallProcess()

true_angle_deg = 20
CALIBRATION.Config(bypass = False, ant_num = num_antennas, mode = "use")
LPA.Config(bypass = False, carrier_freq=fc, ant_dist=d, ant_num=num_antennas, theta=true_angle_deg, noise_power = noise_power, phase_missmatch = [np.pi, np.pi / 2])
KALMAN.Config(bypass = False, fs = fs, measurement_variance = 2, process_variance = 0.01, init_pos = 0, init_vel = 0, init_pos_var = 180, init_vel_var = 180)

for i in range(10):
    sleep(1)
    LPA.mInput = base_signal
    LPA.CallProcess()
    estimated_doa_deg = MUSIC.mOutput
    estimated_kalman_deg = KALMAN.mOutput
    print("True angle: ", true_angle_deg, ", Estimated DOA angle: ", estimated_doa_deg, ", Estimated Kalman angle: ", estimated_kalman_deg, flush = True)
