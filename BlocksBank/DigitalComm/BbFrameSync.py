import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

class BbFrameSync(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "BbFrameSync"
        self.mPreamble = None
        self.mCyclicMode = None

    def Process(self):
        conv_res = np.correlate(self.mInput, self.mPreamble, mode="valid")
        preamble_start_idx = np.argmax(np.abs(conv_res))
        preamble_end_idx = preamble_start_idx + len(self.mPreamble)
        if preamble_end_idx > len(self.mInput):
            ExitError(self.mName + " - Preamble was not fully received")
        received_preamble = self.mInput[preamble_start_idx:preamble_end_idx]
        h_est = np.dot(received_preamble, self.mPreamble) / np.vdot(self.mPreamble, self.mPreamble) 
        
        if not self.mCyclicMode:
            frame = self.mInput[preamble_end_idx:] 
            frame_equalized = frame / h_est
            self.mOutput = frame_equalized
        else:
            frame = np.concatenate((self.mInput[preamble_end_idx:], self.mInput[:preamble_start_idx]))
            frame_equalized = frame / h_est
            self.mOutput = frame_equalized
        
        if self.mDspCore.DBG(2):
            received_preamble_normalizd = received_preamble / h_est
            noise = received_preamble_normalizd - self.mPreamble
            signal_power = np.mean(np.abs(received_preamble_normalizd) ** 2)
            noise_power = np.mean(np.abs(noise) ** 2)
            snr_linear = signal_power / (noise_power + 1e-12)
            snr_db = 10 * np.log10(snr_linear)
            print(self.mName + " - Estimated SNR based on preamble: " + str(snr_db) + " [linear factor of " + str(snr_linear) + "]")
        
    def Config(self, bypass, preamble, cyclic_mode = False):
        self.mByPass = bypass
        self.mConfigDone = True
        self.mPreamble = np.array(preamble) 
        self.mCyclicMode = cyclic_mode        
        
    def Help(self):
        print("BbFrameSync block Process:")
        print(" -> Find the input preamble, remove it shift the frame beggining to the start")
        print(" -> Performs firt order equaliztion of scalar multipication")        
        print("Config(bypass, preamble, cyclic_mode = False):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> preamble: The sequence to add to the beggining of the input frame")  
        print(" -> cyclic_mode: Shifts the signal cyclic after removing the preamble")        