import numpy as np
from ..CommonFun import *

class DspCore:

    def __init__(self):
        self.mType = "DspCore"
        self.mBlocksDict = {}
        self.mDBGLvl = 0
  
    # ===============
    # Blocks handling
    # ===============
  
    def RegisterBlock(self, block):
        if block.mName in self.mBlocksDict:
            ExitError("DSP core - Double decleration of " + str(block.mName))
        self.mBlocksDict[block.mName] = block
        
    def GetBlock(self, name):
        if name in self.mBlocksDict:
            return self.mBlocksDict[name]
        else:
            ExitError("DSP core - No block named " + str(name))

    def Connect(self, *BlockNameVec):
        if len(BlockNameVec) < 2:
            ExitError("DSP core - Not enough arrguments")
        for i in range(len(BlockNameVec) - 1):      
            PrevBlock = self.GetBlock(BlockNameVec[i])
            PrevBlock.ConnectNext(self.GetBlock(BlockNameVec[i + 1]))

    # ===================
    # Simulation handling
    # ===================
    
    def DBG(self, DBG_lvl, mode = "R"):
        if mode == "R":
            if self.mDBGLvl == DBG_lvl:
                return True
            else:
                return False
        if mode == "W":
            self.mDBGLvl = DBG_lvl
            return
        ExitError("DSP core - DBG function mode is not valid -> choose W or R")
        
    def Help(self):
        print("DspCore block interface:")
        print("-> Connect(*BlockName) - connects input blocks in the giver order")
        print("-> DBG(DBG_lvl, mode = \"R\"): mode = \"W\" - set DBG level, mode = \"R\" - True is the argument level is the set one")
        print("-> DBG levels: 0 - None, 1 - System proccess")
        print("-> GetBlock(name) - Returns blocks pointer")        