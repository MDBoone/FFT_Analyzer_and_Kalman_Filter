import numpy as np

class KalmanFilter1D:
    def __init__(self, process_variance=1e-5, measurement_variance=0.1**2):
        self.x = 0.0  # Estimate
        self.P = 1.0  # Estimation error
        self.Q = process_variance
        self.R = measurement_variance

    def filter(self, measurements):
        estimates = []
        for z in measurements:
            # Prediction step
            self.P += self.Q

            # Kalman gain
            K = self.P / (self.P + self.R)

            # Update step
            self.x += K * (z - self.x)
            self.P *= (1 - K)

            estimates.append(self.x)
        return np.array(estimates)
