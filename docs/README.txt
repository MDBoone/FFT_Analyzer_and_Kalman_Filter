**Radar Signal Simulation and Filtering with Kalman and FFT**
This document explains the theoretical foundation, implementation, and interpretation of a radar signal processing simulation that includes target detection, adversarial jamming, frequency analysis, 
and signal tracking using a Kalman filter. It is designed to help engineers and analysts understand how such a system works and how the outputs relate to real-world radar systems.

**1. Objective**
The is aim to simulate a radar return signal from a target at 50 Hz, introduce a jamming signal at 200 Hz, and then apply frequency domain analysis (FFT) and time-domain filtering (Kalman filter) to
isolate and interpret the original radar return. The goal is to emulate a common electronic warfare scenario and demonstrate fundamental signal processing techniques for mitigation.

**2. Signal Components**

**2.1 Target Signal (50 Hz)**
This is a simulated clean sine wave that represents a radar return from a moving target. It oscillates at 50 Hz and has a full amplitude swing between -1 and +1.

X-axis: Time (seconds) | Y-axis: Amplitude of the radar return signal

**2.2 Jamming Signal (200 Hz)**
The jammer simulates an adversarial signal meant to interfere with radar detection. It oscillates at a higher frequency (200 Hz) and is typically lower in amplitude (e.g., 0.8), but more disruptive 
due to its frequency.

X-axis: Time (seconds) | Y-axis: Amplitude of the jamming waveform

**2.3 Composite Signal**
This signal is the linear sum of the target and jamming signals. Due to constructive and destructive interference, the amplitude varies over time in a non-linear way.
When the signals align in phase: amplitudes add up (constructive interference)
When out of phase: amplitudes subtract (destructive interference)
Definition: Composite Signal — A signal formed by adding two or more waveforms together. In this case, it’s the result of combining the 50 Hz target and 200 Hz jammer.

X-axis: Time (seconds) | Y-axis: Composite amplitude (range varies, potentially up to ~1.8 or down to -1.8)

**3. FFT (Fast Fourier Transform)**
The FFT converts the time-domain composite signal into the frequency domain. This reveals the individual frequency components present in the signal.
A sharp peak at 50 Hz represents the target
A second peak at 200 Hz represents the jammer
Graph Interpretation: X-axis: Frequency (Hz) | Y-axis: Magnitude of the signal component at that frequency
This is useful for detecting if jamming is occurring, as unexpected spikes in high-frequency bands may indicate interference.

**4. Kalman Filter**
The Kalman Filter is a recursive estimator that predicts the next value in a sequence based on prior observations. It is ideal for tracking and filtering noisy or distorted signals.
In this simulation:
- The Kalman filter takes the noisy composite signal and attempts to estimate the underlying (true) signal
- Initially, the filter may overshoot or start with poor estimates
- Over time, it converges and tracks the 50 Hz target more accurately
Graph Interpretation: X-axis: Time (seconds) | Y-axis: Filtered signal amplitude
What it tells us:
- How quickly the filter adapts to noisy data
- Its ability to ignore high-frequency jamming components
- Confidence in tracking a stable, predictable signal (like a moving target)

**5. Application in Real Radar Systems**
This simulation reflects real-world radar signal processing in hostile environments:
- Target detection amid jamming and noise
- Electronic counter-countermeasures (ECCM) that aim to mitigate jammer effects
- Frequency analysis to identify and isolate threats
- State estimation using Kalman filters for smoother tracking
In practice, radar systems use combinations of these techniques to reliably identify and track targets even when under electronic attack.

**6. Summary of Graphs**
| Graph Title                | Purpose                                 | X-Axis         | Y-Axis             |
|---------------------------|-----------------------------------------|----------------|--------------------|
| Raw Target Signal (50 Hz)  | Visualizes pure radar return            | Time (s)       | Amplitude          |
| Raw Jammer Signal (200 Hz) | Shows adversarial signal interference   | Time (s)       | Amplitude          |
| Composite Signal           | Simulates real-world signal received    | Time (s)       | Amplitude (varies) |
| FFT Spectrum               | Reveals signal composition by frequency | Frequency (Hz) | Magnitude          |
| Kalman Filtered Signal     | Shows filtered estimation of target     | Time (s)       | Estimated Amplitude|

This system forms the core of a signal analysis tool that could be expanded with additional features such as noise modeling, multi-target tracking, or real-time visualization.
