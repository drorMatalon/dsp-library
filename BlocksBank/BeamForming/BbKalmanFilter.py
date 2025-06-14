import numpy as np
from ..CommonFun import *
from ..BaseBlocks.BaseBlock import BaseBlock

class BbKalmanFilter(BaseBlock):

    def __init__(self, name, dspCore):
        super().__init__(name, dspCore)
        self.mType = "BbKalmanFilter"
        self.mX = None
        self.mP = None 
        self.mQ = None 
        self.mR = None
        self.mDt = None       

    def Process(self):
        F = np.array([[1, self.mDt],
                      [0, 1]])
        H = np.array([[1, 0]])
        I = np.eye(2)  
        output = []
        input_data = np.atleast_1d(self.mInput)
        for z in input_data:
            # ~~~~~~ Prediction step
            self.mX = F @ self.mX
            self.mP = F @ self.mP @ F.T + self.mQ
            # ~~~~~~ Update step
            y = z - H @ self.mX       
            S = H @ self.mP @ H.T + self.mR   
            K = self.mP @ H.T @ np.linalg.inv(S)
            # ~~~~~~ Estimation step            
            self.mX = self.mX + K @ y
            self.mP = (I - K @ H) @ self.mP
            # ~~~~~~ Return position
            output.append(self.mX[0, 0])
        self.mOutput = np.array(output)

    def Config(self, bypass, fs, measurement_variance, process_variance,
               init_pos, init_vel, init_pos_var, init_vel_var):
        self.mByPass = bypass
        self.mDt = 1 / fs
        self.mR = np.array([[measurement_variance]])
        self.mQ = process_variance * np.eye(2)
        self.mX = np.array([[init_pos],
                            [init_vel]])
        self.mP = np.array([[init_pos_var, 0],
                            [0, init_vel_var]])
        self.mConfigDone = True

    def Help(self):
        print("BbKalmanFilter block Process:")
        print(" -> Implements a 1D constant-velocity linear Kalman filter.")
        print("Config(bypass, fs, measurement_variance, process_variance, init_pos, init_vel, init_pos_var, init_vel_var):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> fs: Sampling rate [Hz]")
        print(" -> measurement_variance: Variance of noisy position measurements")
        print(" -> process_variance: Process model uncertainty (larger means less trust in model)")
        print(" -> init_pos: Initial position estimate")
        print(" -> init_vel: Initial velocity estimate")
        print(" -> init_pos_var: Initial uncertainty in position")
        print(" -> init_vel_var: Initial uncertainty in velocity")
