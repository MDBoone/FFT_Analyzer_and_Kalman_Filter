import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np

from signal_generator import SignalGenerator
from fft_analyzer import FFTAnalyzer
from kalman_filter import KalmanFilter1D
from drone_kalman_tracking_2d import DroneSimulator, KalmanFilter2D

class RadarSignalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Radar Signal Analyzer")

        self.fs = 1000
        self.generator = SignalGenerator(sample_rate=self.fs)
        self.fft = FFTAnalyzer(sample_rate=self.fs)
        self.kf = KalmanFilter1D()

        self.target_freq = tk.DoubleVar(value=50)
        self.jammer_freq = tk.DoubleVar(value=200)
        self.noise_std = tk.DoubleVar(value=0.1)
        self.include_jammer = tk.BooleanVar(value=True)

        self._build_ui()

    def _build_ui(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Target Freq (Hz):").pack(side=tk.LEFT)
        ttk.Entry(control_frame, textvariable=self.target_freq, width=5).pack(side=tk.LEFT)

        ttk.Label(control_frame, text="Jammer Freq (Hz):").pack(side=tk.LEFT)
        ttk.Entry(control_frame, textvariable=self.jammer_freq, width=5).pack(side=tk.LEFT)

        ttk.Checkbutton(control_frame, text="Include Jammer", variable=self.include_jammer).pack(side=tk.LEFT)

        ttk.Label(control_frame, text="Noise Std Dev:").pack(side=tk.LEFT)
        ttk.Entry(control_frame, textvariable=self.noise_std, width=5).pack(side=tk.LEFT)

        ttk.Button(control_frame, text="1D FFT + Filter", command=self.plot_signal_fft).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="2D Drone Tracking", command=self.plot_drone_tracking).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Animate Drone Tracking", command=self.animate_drone_tracking).pack(side=tk.RIGHT)

        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_signal_fft(self):
        self.ax.clear()

        t = self.generator.t
        target = self.generator.generate_target_signal(freq=self.target_freq.get())
        jammer = self.generator.generate_jammer_signal(freq=self.jammer_freq.get()) if self.include_jammer.get() else np.zeros_like(t)
        noise = np.random.normal(0, self.noise_std.get(), size=t.shape)
        composite = target + jammer + noise
        fft_freqs, fft_mags = self.fft.compute_fft(composite)
        filtered = self.kf.filter(composite)

        self.ax.plot(t, composite, label="Composite")
        self.ax.plot(t, filtered, label="Kalman Filtered", linestyle="--")
        self.ax.set_title("Composite and Kalman Filtered Signal")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

        # FFT in new window
        fig_fft, ax_fft = plt.subplots()
        ax_fft.plot(fft_freqs, fft_mags)
        ax_fft.set_title("FFT Spectrum")
        ax_fft.set_xlabel("Frequency (Hz)")
        ax_fft.set_ylabel("Magnitude")
        ax_fft.grid(True)
        plt.show()

    def plot_drone_tracking(self):
        self.ax.clear()
        sim = DroneSimulator(dt=0.1, total_time=10)
        kf2d = KalmanFilter2D(dt=0.1)

        estimates = [kf2d.update(z)[:2] for z in sim.measurements]
        estimates = np.array(estimates)

        self.ax.plot(sim.true_states[:, 0], sim.true_states[:, 1], label="True Path")
        self.ax.plot(sim.measurements[:, 0], sim.measurements[:, 1], label="Radar Measurements", linestyle=':', alpha=0.5)
        self.ax.plot(estimates[:, 0], estimates[:, 1], label="Kalman Filter Estimate", linestyle='--')
        self.ax.set_title("2D Drone Tracking with Kalman Filter")
        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Y Position")
        self.ax.legend()
        self.ax.grid(True)
        self.ax.axis("equal")
        self.canvas.draw()

    def animate_drone_tracking(self):
        sim = DroneSimulator(dt=0.1, total_time=10)
        kf2d = KalmanFilter2D(dt=0.1)
        estimates = [kf2d.update(z)[:2] for z in sim.measurements]
        estimates = np.array(estimates)

        fig, ax = plt.subplots()
        ax.set_xlim(np.min(sim.true_states[:, 0]) - 1, np.max(sim.true_states[:, 0]) + 1)
        ax.set_ylim(np.min(sim.true_states[:, 1]) - 1, np.max(sim.true_states[:, 1]) + 1)
        ax.set_title("2D Drone Tracking Animation")
        ax.set_xlabel("X Position")
        ax.set_ylabel("Y Position")
        ax.grid(True)
        ax.set_aspect("equal")

        true_line, = ax.plot([], [], label="True Path", color='blue')
        meas_scatter, = ax.plot([], [], 'ro', label="Measurement", markersize=4)
        est_line, = ax.plot([], [], label="Kalman Estimate", color='green')
        true_path = []
        est_path = []

        def update(frame):
            true_path.append(sim.true_states[frame, :2])
            est_path.append(estimates[frame])
            true_arr = np.array(true_path)
            est_arr = np.array(est_path)
            true_line.set_data(true_arr[:, 0], true_arr[:, 1])
            meas_scatter.set_data([sim.measurements[frame, 0]], [sim.measurements[frame, 1]])
            est_line.set_data(est_arr[:, 0], est_arr[:, 1])
            return true_line, meas_scatter, est_line

        ani = animation.FuncAnimation(fig, update, frames=len(sim.t), interval=100, blit=True)
        ax.legend()
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    root = tk.Tk()
    app = RadarSignalApp(root)
    root.mainloop()
