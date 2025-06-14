from .BaseBlock import BaseBlock
from ..CommonFun import *

class BbTemplateBlock(BaseBlock):
    
    def __init__(self, name, simCore, operation):
        super().__init__(name, simCore)
        self.mType = "BbDec"
        self.mDecFactor = None
        self.mByPass = False
        self.mConfigDone = True
        self.mOperation = operation

    # =======================
    # unique abstract methods
    # =======================
    
    def Process(self):
        self.mOperation(self)

    def Config(self, bypass):
        pass
        
    def Help(self):
        print("BbTemplateBlock interface:")
        print("Constructor(name, dspCore, process):")
        print("-> name - block name to print in log")
        print("-> dspCore - DSP core")
        print("-> opertion() - process function")