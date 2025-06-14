import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

class BbDecimator(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "BbDecimator"
        self.mDecFactor = None
        self.mCnt = 0

    def Process(self):
        self.mOutput = []
        for sample in self.mInput:
            self.mCnt += 1
            if (self.mCnt) % self.mDecFactor == 0:
                self.mCnt = 0
                self.mOutput.append(sample)
        if self.mOutput is None:
            ExitError(self.mName + " - Desimation rate is higher than the input length")
        self.mOutput = np.array(self.mOutput)
        
    def Config(self, bypass, decFactor, offset = 0):
        self.mByPass = bypass
        self.mConfigDone = True
        self.mDecFactor = decFactor
        self.mCnt = offset
        
    def Help(self):
        print("BbDecimator block Process:")
        print(" -> simple decimator")  
        print("Config(bypass, decFctor, offset = 0):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> decFactor = Decimation rate") 
        print(" -> offset = Decimation offset")