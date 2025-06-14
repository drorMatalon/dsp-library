from abc import ABC, abstractmethod
from ..CommonFun import *

class BaseBlock(ABC):
    
    def __init__(self, name, dspCore):
        self.mName = name
        self.mDspCore = dspCore
        self.mDspCore.RegisterBlock(self)
        self.mType = "BaseBlock"
        self.mInput = None
        self.mOutput = None
        self.mNextBlock = None
        self.mByPass = True
        self.mConfigDone = False


    # ==============
    # common methods
    # ==============

    def CallProcess(self):
        self.Validate()       
        if self.mByPass:
            self.mOutput = self.mInput
        else:
            if self.mDspCore.DBG(1):
                print(self.mName + " - Process called", flush = True)
            self.Process()
        if self.mNextBlock is not None:
            self.mNextBlock.mInput = self.mOutput
            self.mNextBlock.CallProcess()

    def ConnectNext(self, nextBlock):
        if nextBlock.mType[:2] == "Ig":
            WarningError(self.mName + " - Next block is an In Gate")
        if self.mType[:2] == "Og":
            WarningError(self.mName + " - Out Gate with next block")
        self.mNextBlock = nextBlock

    def Validate(self):
        if self.mInput is None:
            if self.mType[:2] != "Ig":
                ExitError(self.mName + " - No input")
        if self.mConfigDone == False:
            ExitError(self.mName + " - No configuration")  

    # =======================
    # unique abstract methods
    # =======================
    
    @abstractmethod
    def Process(self):
        pass

    @abstractmethod
    def Config(self, bypass):
        self.mByPass = bypass
        self.mConfigDone = True
        pass
        
    @abstractmethod
    def Help(self):
        print("BaseBlock block interface:")
        print("Constructor(name, dspCore):")
        print("-> name - block name to print in log")
        print("-> dspCore - DSP core")
        print("Methods:")
        print("-> ConnectNext(block) - connects the next BbBlock")
        print("-> CallProcess() - calling the block proces and when finishing calls the next block ones")
        print("-> Config(bypass) - load configuration")
        #prints the blocks interface