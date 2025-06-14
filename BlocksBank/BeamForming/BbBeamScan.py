import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

"""
Math background:
-> y ~ ax + n; recieved signal
-> estimated theta = argmax(theta) {|y - ax|^2} assuming gausian noise using max likelihood estimation
-> estimated theta = (a^H R a) / |a|^2 while R = y y^H
"""

class BbBeamScan(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "BbBeamScan"
        self.mMode = None
        self.mFc = None
        self.mD = None
        self.mTheta = None
        self.mAnglesRange = None

    def Process(self):
        antNum = self.mInput.shape[0]
        waveLength = 3e8 / self.mFc
        if self.mMode == "beamforming":
            steeringVector = np.exp(1j * 2 * np.pi * np.sin(self.mTheta) * np.arange(antNum) * self.mD / waveLength)
            self.mOutput = np.dot(steeringVector.conj().T, self.mInput)
        elif self.mMode == "doa":
            R = self.mInput @ self.mInput.conj().T
            maxPower = -np.inf
            estimatedTheta = None
            powersForPlot = []
            for theta in self.mAnglesRange:
                steeringVec = np.exp(1j * 2 * np.pi * np.sin(theta) * np.arange(antNum) * self.mD / waveLength)
                steeringVec = steeringVec[:, np.newaxis]
                power = np.real((steeringVec.conj().T @ R @ steeringVec)[0, 0])
                powersForPlot.append(power)
                if power > maxPower:
                    maxPower = power
                    estimatedTheta = theta
            self.mOutput = np.rad2deg(estimatedTheta)
            if self.mDspCore.DBG(2):
                plt.plot(np.degrees(self.mAnglesRange), powersForPlot)
                plt.title(self.mName + " - DOA estimation")
                plt.axvline(x=np.degrees(estimatedTheta), color='r', linestyle='-', linewidth=2, label="Estimated angle")
                plt.show()

    def Config(self, bypass, carrier_freq, ant_dist, mode, angles_range=None, theta=None):
        self.mByPass = bypass
        if mode not in ["doa", "beamforming"]:
            ExitError(self.mName + " - Chosen mode is not valid -> choose doa or beamforming")
        self.mFc = carrier_freq
        self.mD = ant_dist
        self.mMode = mode
        if theta is not None:
            self.mTheta = np.radians(theta)
        if angles_range is not None:
            self.mAnglesRange = np.radians(angles_range)
        self.mConfigDone = True

    def Help(self):
        print("BbBeamScan block Process:")
        print(" -> Performs beam scan beamforming or doa")  
        print("Config(bypass, carrier_freq, ant_dist, mode, angles_range = None, theta = None):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> carrier_freq: signals carrier frequency")
        print(" -> ant_dist: phased array antennas distance")
        print(" -> mode: doa or beamforming")
        print(" -> angles_range: angles for doa functionality, defines the algorithm resolution")
        print(" -> theta: Angle for beamforming")
