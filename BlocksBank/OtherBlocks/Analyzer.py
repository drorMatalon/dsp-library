import numpy as np
import matplotlib.pyplot as plt
from ..CommonFun import *

class Analyzer:
    def __init__(self, name, DspCore):
        self.mName = name
        self.mDspCore = DspCore
        self.mDspCore.RegisterBlock(self)
        self.mType = "OgAnalyzer"
        self.mPlotMode = None
        self.mFs = None
        self.mInput = None

    def CallProcess(self):
        if self.mInput is None:
            ExitError(self.mName + " - No input!")
        self.Plot()

    def Config(self, mode, fs):
        self.mPlotMode = mode
        self.mFs = fs
        if mode not in ["amplitude", "constellation", "spectrum"]:
            ExitError(self.mName + " - chosen mode is not valid -> choose: amplitude, constellation, spectrum")

    def Plot(self):
        if self.mPlotMode == "amplitude":
            self.PlotAmplitude()
        elif self.mPlotMode == "constellation":
            self.PlotConstellation()
        elif self.mPlotMode == "spectrum":
            self.PlotFft()
        else:
            ExitError(self.mName + " - chosen mode is not valid -> choose: amplitude, constellation, spectrum")
        plt.draw()
        plt.pause(0.001)

    def PlotAmplitude(self):
        plt.clf()
        samplesNumber = len(self.mInput)
        time_axis = np.linspace(0, samplesNumber - 1, samplesNumber) / self.mFs
        plt.plot(time_axis, self.mInput.real, label="Real Part")
        plt.plot(time_axis, self.mInput.imag, label="Imaginary Part", linestyle='--')        
        plt.title(self.mName + " - Real and Imaginary Parts vs Time")
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.legend()

    def PlotConstellation(self):
        plt.clf()
        signal = np.array(self.mInput).astype(complex)
        I = signal.real
        Q = signal.imag
        plt.scatter(I, Q, alpha=0.5)
        plt.title(self.mName + " - Constellation Diagram")
        plt.xlabel("In-Phase (I)")
        plt.ylabel("Quadrature (Q)")
        plt.grid(True)

    def PlotFft(self):
        plt.clf()
        signal = np.array(self.mInput)
        spectrum = np.fft.fftshift(np.fft.fft(signal))
        freq = np.fft.fftshift(np.fft.fftfreq(len(signal), d=1/self.mFs))
        plt.subplot(2, 1, 1)
        plt.plot(freq, 20 * np.log10(np.abs(spectrum) + 1e-12))
        plt.title(self.mName + " - Spectrum Magnitude and Phase")
        plt.ylabel("Magnitude [dB]")
        plt.grid(True)
        plt.subplot(2, 1, 2)
        plt.plot(freq, np.angle(spectrum))
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Phase [rad]")
        plt.grid(True)

    def Help(self):
        print("Analyzer block interface:")
        print("Constructor(name, DspCore):")
        print("-> name - analyzer name")
        print("-> DspCore - DSP core")
        print("methods:")
        print("-> Config(mode, fs) - choose plot mode: amplitude, constellation, spectrum")