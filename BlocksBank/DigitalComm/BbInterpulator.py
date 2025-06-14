import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

class BbInterpulator(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "BbInterpulator"
        self.mIntFactor = None

    def Process(self):
        output = []
        for sample in self.mInput:
            output.append(sample)
            for i in range(self.mIntFactor - 1):
                output.append(0)
        self.mOutput = np.array(output)
        
    def Config(self, bypass, decFactor):
        self.mByPass = bypass
        self.mConfigDone = True
        self.mIntFactor = decFactor
        
    def Help(self):
        print("BbInterpulator block Process:")
        print(" -> simple delta interpulation")  
        print("Config(bypass, intFactor):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> intFactor = Interpulation rate")      