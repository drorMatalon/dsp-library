import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock
import matplotlib.pyplot as plt

"""
Math background:
-> y ~ ax + n; recieved signal while R = y y^H = |x|^2 a a^H + n n^H
-> a is an eigen vector since Ra = (|x|^2 + sigma_n)a, other eigen vectors recieved when a a^H v = 0
-> all the other eigen vectors but  are orthogonal to a and do not carry signals energy
-> Music searches vor vectors that are orthogonal to all of the noise eigen vectors which are the ones with the smallest eigen values
"""

class BbMusic(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "BbMusic"
        self.mFc = None
        self.mD = None
        self.mAnglesRange = None

    def Process(self):
        antNum = self.mInput.shape[0]
        waveLength = 3e8 / self.mFc
        R = self.mInput @ self.mInput.conj().T
        eigenVal, eigenVec = np.linalg.eigh(R)
        noiseEigenVec = eigenVec[:, :-1] #Asuming only one incoming signal
        maxPower = -np.inf
        estimatedTheta = None
        powersForPlot = []
        for theta in self.mAnglesRange:
            steeringVector = np.exp(1j * 2 * np.pi * np.sin(theta) * np.arange(antNum) * self.mD / waveLength)
            power = 1.0 / np.linalg.norm(np.dot(noiseEigenVec.conj().T, steeringVector))**2        
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

    def Config(self, bypass, carrier_freq, ant_dist, angles_range):
        self.mByPass = bypass
        self.mFc = carrier_freq
        self.mD = ant_dist
        self.mAnglesRange = np.radians(angles_range)
        self.mConfigDone = True

    def Help(self):
        print("BbMusic block Process:")
        print(" -> Performs beam scan beamforming or doa")  
        print("Config(bypass, carrier_freq, ant_dist, angles_range):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> carrier_freq: signals carrier frequency")
        print(" -> ant_dist: phased array antennas distance")
        print(" -> angles_range: angles for doa functionality, defines the algorithm resolution")
