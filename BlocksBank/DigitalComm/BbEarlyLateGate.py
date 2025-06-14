import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

class BbEarlyLateGate(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "BbEarlyLateGate"
        self.mSps = None
        self.mGap = None
        self.mStep = None

    def Process(self):
        out = []
        pulseNum = len(self.mInput) // self.mSps
        delay = self.mSps // 2
        
        for i in range(pulseNum):
            center = i * self.mSps + round(delay)        # Estimated optimal sample
            early  = round(center - self.mGap / 2)       # Early sample (before peak)
            late   = round(center + self.mGap / 2)       # Late sample (after peak)

            EarlySamp = self.mInput[early]               # Early sample value
            OnTimeSamp = self.mInput[center]             # On-time sample value
            LateSamp = self.mInput[late]                 # Late sample value
            out.append(OnTimeSamp)

            error = np.abs(LateSamp) - np.abs(EarlySamp) # Error - 0 if the center sample is on the symetry axis
            if self.mDspCore.DBG(4):
                print(f"Pulse {i}: OnTimeSamp = {OnTimeSamp:.3f}, EarlySamp = {EarlySamp:.3f}, LateSamp = {LateSamp:.3f}, Error = {error:.3f}, Delay = {delay:.3f}")
            delay = np.clip(delay + self.mStep * error, -self.mSps // 2, self.mSps // 2 - 1)  # Delay update
            
        self.mOutput = np.array(out)
        
    def Config(self, bypass, sps, gap, step):
        self.mByPass = bypass
        self.mConfigDone = True
        self.mSps = sps
        self.mGap = gap
        self.mStep = step

        
    def Help(self):
        print("BbEarlyLateGate block Process:")
        print(" -> Ealy late gate time synchronize algorithm, requiers symmetrical pulse shape")  
        print("Config(bypass, sps, gap, step):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> sps: samples per symbole") 
        print(" -> gap: gap between early and late samples")
        print(" -> step: delay[i+1] = delay[i] + step * error")