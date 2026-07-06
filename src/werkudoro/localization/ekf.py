"""Extended Kalman Filter for 2D vehicle localization."""

import numpy as np
from dataclasses import dataclass, field


@dataclass
class EKFConfig:
    """EKF configuration."""
    dt: float = 0.01
    # process noise (acceleration, yaw_rate, speed noise)
    q_accel: float = 0.5
    q_yaw_rate: float = 0.1
    q_speed: float = 0.2
    # measurement noise
    r_gps: float = 1.0
    r_imu: float = 0.1


class ExtendedKalmanFilter:
    """EKF fusing odometry + GPS + IMU.

    State: [x, y, yaw, v]

    Predict step uses a simple kinematic model.
    Update step fuses available measurements.
    """

    def __init__(self, config: EKFConfig | None = None):
        self.config = config or EKFConfig()
        self.x = np.zeros(4)  # state
        self.P = np.eye(4) * 0.1  # covariance
        self.initialized = False

    def initialize(self, x: float, y: float, yaw: float, v: float):
        """Set initial state."""
        self.x = np.array([x, y, yaw, v])
        self.P = np.eye(4) * 0.1
        self.initialized = True

    def predict(self, dt: float | None = None):
        """Predict step using kinematic model."""
        dt = dt or self.config.dt
        cfg = self.config

        # state transition (nonlinear)
        x, y, yaw, v = self.x
        x_new = x + v * np.cos(yaw) * dt
        y_new = y + v * np.sin(yaw) * dt
        yaw_new = yaw  # yaw assumed constant in prediction
        v_new = v

        self.x = np.array([x_new, y_new, yaw_new, v_new])

        # Jacobian of state transition
        F = np.array([
            [1, 0, -v * np.sin(yaw) * dt, np.cos(yaw) * dt],
            [0, 1,  v * np.cos(yaw) * dt, np.sin(yaw) * dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

        # process noise
        Q = np.diag([
            cfg.q_accel * dt ** 2,
            cfg.q_accel * dt ** 2,
            cfg.q_yaw_rate * dt,
            cfg.q_speed * dt,
        ])

        self.P = F @ self.P @ F.T + Q

    def update_gps(self, gps_x: float, gps_y: float):
        """Update with GPS measurement."""
        if not self.initialized:
            self.initialize(gps_x, gps_y, 0.0, 0.0)
            return

        cfg = self.config
        z = np.array([gps_x, gps_y])

        # measurement Jacobian
        H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ])

        R = np.eye(2) * cfg.r_gps

        # innovation
        y = z - H @ self.x
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)

        self.x = self.x + K @ y
        self.P = (np.eye(4) - K @ H) @ self.P

    def update_imu(self, yaw_rate: float, accel: float):
        """Update with IMU measurement (yaw rate + acceleration)."""
        if not self.initialized:
            return

        cfg = self.config

        # simple: use acceleration to update speed estimate
        self.x[3] += accel * cfg.dt

        # yaw rate is an observation of yaw change
        # (simplified - full version would use measurement model)
        self.x[2] += yaw_rate * cfg.dt

    @property
    def state(self) -> dict[str, float]:
        return {
            "x": float(self.x[0]),
            "y": float(self.x[1]),
            "yaw": float(self.x[2]),
            "v": float(self.x[3]),
        }


def demo():
    """Sanity check: EKF should track a constant velocity vehicle."""
    ekf = ExtendedKalmanFilter()
    ekf.initialize(0, 0, 0, 1.0)

    # simulate moving at 1 m/s for 100 steps
    true_x = 0.0
    for i in range(100):
        ekf.predict(dt=0.01)
        true_x += 1.0 * 0.01

        # GPS with noise
        ekf.update_gps(true_x + np.random.normal(0, 0.05), np.random.normal(0, 0.05))

    s = ekf.state
    assert abs(s["x"] - 1.0) < 0.2, f"expected x≈1.0, got {s['x']}"
    assert abs(s["v"] - 1.0) < 0.5, f"expected v≈1.0, got {s['v']}"
    print("ekf: all checks passed")


if __name__ == "__main__":
    demo()
