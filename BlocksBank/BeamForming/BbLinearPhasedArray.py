import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

class BbLinearPhasedArray(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "IgLinearPhasedArray"
        self.mFc = None
        self.mD = None
        self.mAntNum = None
        self.mTheta = None
        self.mNoisePower = None
        self.mPhaseMissmatch = None

    def Process(self):
        waveLength = 3e8 / self.mFc
        steeringVector = np.exp(1j * 2 * np.pi * np.sin(self.mTheta) * np.arange(self.mAntNum)[:, None] * self.mD / waveLength)
        if self.mPhaseMissmatch is not None:
            phase_offset = np.exp(1j * self.mPhaseMissmatch)
            steeringVector *= phase_offset[:, np.newaxis]
        received = steeringVector * self.mInput
        if self.mNoisePower > 0:
            noise = (np.random.randn(*received.shape) + 1j * np.random.randn(*received.shape)) * np.sqrt(self.mNoisePower / 2)
            received += noise
        self.mOutput = received

    def Config(self, bypass, carrier_freq, ant_dist, ant_num, theta, noise_power=0, phase_missmatch = None):
        self.mByPass = bypass
        self.mFc = carrier_freq
        self.mD = ant_dist
        self.mAntNum = ant_num
        self.mTheta = np.radians(theta)
        self.mNoisePower = noise_power
        if phase_missmatch is not None:
            phase_missmatch = np.asarray(phase_missmatch)
            if phase_missmatch.shape != (ant_num,):
                ExitError(self.mName + " - phase_missmatch must be a 1D array of length equal to ant_num")
        self.mPhaseMissmatch = phase_missmatch
        self.mConfigDone = True

    def Help(self):
        print("BbLinearPhasedArray block Process:")
        print(" -> Models a linear phased array with optional additive noise")
        print("Config(bypass, carrier_freq, ant_dist, ant_num, theta, noise_power=0, phase_missmatch = None):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> carrier_freq: signal's carrier frequency [Hz]")
        print(" -> ant_dist: antenna spacing [m]")
        print(" -> ant_num: number of antennas")
        print(" -> theta: angle of arrival in degrees")
        print(" -> noise_power: Noise power added to each antenna (uncorelated AWGN)")
        print(" -> phase_missmatch: Add a built in phase and gain diferences, add a numpy array at the size of the ant number")
