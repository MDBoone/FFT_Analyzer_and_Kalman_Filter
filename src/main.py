from signal_generator import SignalGenerator
from fft_analyzer import FFTAnalyzer
from kalman_filter import KalmanFilter1D
import plot_utils as plt_utils

# Initialize objects
fs = 1000
generator = SignalGenerator(sample_rate=fs)
fft = FFTAnalyzer(sample_rate=fs)
kf = KalmanFilter1D()

# Time array
t = generator.t

# Generate signals
target_signal = generator.generate_target_signal()
jammer_signal = generator.generate_jammer_signal()
composite = generator.generate_composite(noise_std=0.1)

# FFT
freqs, magnitudes = fft.compute_fft(composite)

# Kalman filter
filtered = kf.filter(composite)

#Plot individual components BEFORE combining
plt_utils.plot_signal(t, target_signal, title="Raw Target Signal (50 Hz)", label="Target 50 Hz")
plt_utils.plot_signal(t, jammer_signal, title="Raw Jammer Signal (200 Hz)", label="Jammer 200 Hz")

#Plot noise component
noise = composite - target_signal - jammer_signal
plt_utils.plot_signal(t, noise, title="White Gaussian Noise", label="Noise Component")

# Existing plots
plt_utils.plot_signal(t, composite, title="Composite Signal", label="Target + Jammer")
plt_utils.plot_signal(t, filtered, title="Kalman Filtered Signal", label="Filtered")
plt_utils.plot_fft(freqs, magnitudes, title="FFT of Composite Radar Signal")
