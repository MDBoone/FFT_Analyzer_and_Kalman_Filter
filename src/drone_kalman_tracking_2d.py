import numpy as np

class DroneSimulator:
    def __init__(self, dt=0.1, total_time=10):
        self.dt = dt
        self.time_steps = int(total_time / dt)
        self.t = np.linspace(0, total_time, self.time_steps)

        self.true_states = np.zeros((self.time_steps, 4))  # [x, y, vx, vy]
        self.measurements = np.zeros((self.time_steps, 2))
        self._simulate_trajectory()

    def _simulate_trajectory(self):
        state = np.array([0.0, 0.0, 1.0, 0.5])  # Initial [x, y, vx, vy]
        for i in range(self.time_steps):
            state[0] += state[2] * self.dt
            state[1] += state[3] * self.dt
            state[2] += np.random.normal(0, 0.05)
            state[3] += np.random.normal(0, 0.05)
            self.true_states[i] = state.copy()
            self.measurements[i] = [
                state[0] + np.random.normal(0, 0.5),
                state[1] + np.random.normal(0, 0.5),
            ]

class KalmanFilter2D:
    def __init__(self, dt):
        self.x = np.zeros(4)  # [x, y, vx, vy]
        self.P = np.eye(4)
        self.F = np.array([[1, 0, dt, 0],
                           [0, 1, 0, dt],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]])
        self.R = np.eye(2) * 0.25
        self.Q = np.eye(4) * 0.01

    def update(self, z):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)

        self.x = self.x + K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P
        return self.x.copy()