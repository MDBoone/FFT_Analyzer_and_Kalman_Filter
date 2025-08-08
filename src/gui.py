# import tkinter as tk
# from tkinter import ttk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np
# from signal_generator import SignalGenerator
# from fft_analyzer import FFTAnalyzer
# from kalman_filter import KalmanFilter1D
# import plot_utils as plt_utils

# class RadarSignalApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Radar Signal Analyzer")

#         self.fs = 1000
#         self.generator = SignalGenerator(sample_rate=self.fs)
#         self.fft = FFTAnalyzer(sample_rate=self.fs)
#         self.kf = KalmanFilter1D()

#         self.target_freq = tk.DoubleVar(value=50)
#         self.jammer_freq = tk.DoubleVar(value=200)
#         self.noise_std = tk.DoubleVar(value=0.1)
#         self.include_jammer = tk.BooleanVar(value=True)

#         self._build_ui()

#     def _build_ui(self):
#         control_frame = ttk.Frame(self.root)
#         control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

#         ttk.Label(control_frame, text="Target Freq (Hz):").pack(side=tk.LEFT)
#         ttk.Entry(control_frame, textvariable=self.target_freq, width=5).pack(side=tk.LEFT)

#         ttk.Label(control_frame, text="Jammer Freq (Hz):").pack(side=tk.LEFT)
#         ttk.Entry(control_frame, textvariable=self.jammer_freq, width=5).pack(side=tk.LEFT)

#         ttk.Checkbutton(control_frame, text="Include Jammer", variable=self.include_jammer).pack(side=tk.LEFT)

#         ttk.Label(control_frame, text="Noise Std Dev:").pack(side=tk.LEFT)
#         ttk.Entry(control_frame, textvariable=self.noise_std, width=5).pack(side=tk.LEFT)

#         ttk.Button(control_frame, text="Generate & Plot", command=self.plot_all).pack(side=tk.RIGHT)

#         self.fig, self.ax = plt.subplots(figsize=(8, 5))
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
#         self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#     def plot_all(self):
#         self.ax.clear()

#         t = self.generator.t
#         target = self.generator.generate_target_signal(freq=self.target_freq.get())

#         if self.include_jammer.get():
#             jammer = self.generator.generate_jammer_signal(freq=self.jammer_freq.get())
#         else:
#             jammer = np.zeros_like(t)

#         noise = np.random.normal(0, self.noise_std.get(), size=t.shape)
#         composite = target + jammer + noise
#         fft_freqs, fft_mags = self.fft.compute_fft(composite)
#         filtered = self.kf.filter(composite)

#         self.ax.plot(t, composite, label="Composite")
#         self.ax.plot(t, filtered, label="Kalman Filtered", linestyle="--")
#         self.ax.set_title("Composite and Kalman Filtered Signal")
#         self.ax.set_xlabel("Time (s)")
#         self.ax.set_ylabel("Amplitude")
#         self.ax.legend()
#         self.ax.grid(True)
#         self.canvas.draw()

#         # Plot FFT in new figure
#         fig_fft, ax_fft = plt.subplots()
#         ax_fft.plot(fft_freqs, fft_mags)
#         ax_fft.set_title("FFT Spectrum")
#         ax_fft.set_xlabel("Frequency (Hz)")
#         ax_fft.set_ylabel("Magnitude")
#         ax_fft.grid(True)
#         plt.show()

# if __name__ == '__main__':
#     root = tk.Tk()
#     app = RadarSignalApp(root)
#     root.mainloop()