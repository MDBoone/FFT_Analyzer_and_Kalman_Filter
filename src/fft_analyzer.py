import numpy as np

class FFTAnalyzer:
    def __init__(self, sample_rate):
        self.fs = sample_rate

    def compute_fft(self, signal):
        fft_vals = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), d=1/self.fs)
        return freqs[:len(freqs)//2], np.abs(fft_vals)[:len(freqs)//2]
