import matplotlib.pyplot as plt

def plot_signal(time, signal, title="Signal", label="Signal"):
    plt.plot(time, signal, label=label)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_fft(freqs, magnitudes, title="FFT Spectrum"):
    plt.plot(freqs, magnitudes)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()
