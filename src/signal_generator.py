import numpy as np

class SignalGenerator:
    def __init__(self, sample_rate=1000, duration=1):
        self.fs = sample_rate #increase sample rate for better resolution but uses more memory. Decrease for less memory but lower resolution
        self.t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    def generate_target_signal(self, freq=50, amplitude=1.0):
        return amplitude * np.sin(2 * np.pi * freq * self.t)

    def generate_jammer_signal(self, freq=200, amplitude=0.8, phase=np.pi/4):
        return amplitude * np.sin(2 * np.pi * freq * self.t + phase)

    def generate_composite(self, target_freq=50, jammer_freq=200, noise_std=0.1):
        target = self.generate_target_signal(target_freq)
        jammer = self.generate_jammer_signal(jammer_freq)
        noise = np.random.normal(0, noise_std, size=self.t.shape)
        return target + jammer + noise
