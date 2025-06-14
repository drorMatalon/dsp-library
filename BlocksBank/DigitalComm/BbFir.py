import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

class BbFir(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "BbFir"
        self.mTaps = []
        self.mCoeff = None

    def Process(self):
        output = []
        for sampleIdx in range(self.mInput.shape[0]):
            self.mTaps.append(self.mInput[sampleIdx])
            self.mTaps.pop(0)
            np_taps = np.array(self.mTaps)
            output.append(np.dot(self.mCoeff, np_taps))
        self.mOutput = np.array(output)
        
    def Config(self, bypass, coefficients):
        self.mByPass = bypass
        if not isinstance(coefficients, np.ndarray):
            ExitError(self.mName + " - input coefficients is not a numpy array")
        if coefficients.size > 1:
            self.mCoeff = coefficients[::-1].copy()
        else:
            self.mCoeff = coefficients.copy()
        self.mTaps = np.zeros(coefficients.size).tolist()
        self.mConfigDone = True
        
    def Help(self):
        print("BbFir block Process:")
        print(" -> FIR filter")  
        print("Config(bypass, coefficients):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> coefficients = FIR coefficients")      