import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

class BbLpaCalibration(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "IgLinearPhasedArray"
        self.mFc = None
        self.mD = None
        self.mAntNum = None
        self.mTheta = None
        self.mMode = None
        self.mFixArr = None
        self.mTrainDone = False

    def Process(self):
        if self.mMode == "train":
            self.mFixArr = np.ones(self.mAntNum, dtype = complex)
            WarningError(self.mName + " - Make sure that the signal source is in front of the antennas array while traning (Theta = 0)")
            for i in range(self.mAntNum):
                signal = self.mInput[i,:]
                fft_signal = np.fft.fft(signal)
                index = np.argmax(np.abs(fft_signal))
                self.mFixArr[i] = fft_signal[index]
            self.mFixArr /= self.mFixArr[0]
            self.mOutput = self.mInput
            self.mTrainDone = True
            if self.mDspCore.DBG(2):
                print(self.mName + " - calibration scalars:")
                print("-> ", self.mFixArr)
        else:    
            if not self.mTrainDone:
                ExitError(self.mName + " - Train block before calibrating with it")
            self.mOutput = self.mInput / self.mFixArr[:, np.newaxis]

    def Config(self, bypass, ant_num, mode = "train"):
        self.mByPass = bypass
        self.mAntNum = ant_num
        if mode != "train" and mode != "use":
            ExitError(self.mName + " - Mode arrgument is not valid -> choose train or use")
        self.mMode = mode
        self.mConfigDone = True

    def Help(self):
        print("BbLpaCalibration block Process:")
        print(" -> Allows phase adding for antennas for calibration")
        print("Config(bypass, ant_num, mode = \"train\"):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> ant_num: number of antennas")
        print(" -> mode: \"train\" - train the block, \"use\" - apply calibration")
