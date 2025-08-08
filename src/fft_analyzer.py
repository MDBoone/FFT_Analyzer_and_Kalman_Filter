import numpy as np

class FFTAnalyzer:
    def __init__(self, sample_rate=1000):
        self.sample_rate = sample_rate

    def compute_fft(self, signal):
        n = len(signal)
        fft_vals = np.fft.fft(signal)
        fft_freqs = np.fft.fftfreq(n, d=1/self.sample_rate)
        magnitudes = np.abs(fft_vals) / n
        
        # Only keep positive frequencies
        mask = fft_freqs >= 0
        return fft_freqs[mask], magnitudes[mask]