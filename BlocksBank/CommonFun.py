import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def ExitError(text):
    print("XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx")
    print("EXIT ERROR - " + text)
    print("XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx")   
    exit()
    
def WarningError(text):
    print("OoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo", flush = True)
    print("Warning - " + text, flush = True)
    print("OoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo", flush = True)  
    
def CommonHelp():
    print("Common functions:")
    print("-> ExitError(text): prints the input text then exits the program")
    print("-> WarningError(text): prints the input text")
    print("-> PlotFilterResponse(B, A = 1, name = None): plots filter mgnitude nd phase respons while A = [a1, a2 ...] is numerator coefficients and B = [b1, b2 ..] is denumerator")
    
def PlotFilterRespons(B, A = 1, name = None):   
    # Plot magnitude response
    freqs, h = signal.freqz(B, A)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(freqs, 20 * np.log10(abs(h)))
    if name is not None:
        plt.title(name + " Magnitude Response")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude [dB]")
    plt.grid()
    # Plot phase response
    plt.subplot(1, 2, 2)
    plt.plot(freqs, np.angle(h))
    if name is not None:
        plt.title(name + " Magnitude Response")
    plt.title(name + " Phase Response")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Phase [radians]")
    plt.grid()
    plt.tight_layout()
    plt.show()