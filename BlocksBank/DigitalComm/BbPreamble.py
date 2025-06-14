import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

class BbPreamble(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "BbPreamble"
        self.mPreamble = None

    def Process(self):
        self.mOutput = np.concatenate((self.mPreamble, self.mInput)) 
        
    def Config(self, bypass, preamble):
        self.mByPass = bypass
        self.mConfigDone = True
        self.mPreamble = np.array(preamble)           
        
    def Help(self):
        print("BbPreamble block Process:")
        print(" -> Adds preamble to the beggining of a frame")  
        print("Config(bypass, preamble):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> preamble: The sequence to add to the beggining of the input frame")      