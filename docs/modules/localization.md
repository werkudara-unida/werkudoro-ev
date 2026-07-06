# Localization Module

## ekf.py

Extended Kalman Filter for 2D vehicle localization.

### Why EKF?

Fuses noisy sensor data (GPS, IMU, encoder) into a single pose estimate. EKF handles nonlinear models (unlike standard KF).

### State Vector

```
x = [x, y, yaw, v]
```

### Key Class

```python
ExtendedKalmanFilter(config=EKFConfig())
```

| Method | Description |
|--------|-------------|
| `initialize(x, y, yaw, v)` | Set initial state |
| `predict(dt)` | Propagate state forward |
| `update_gps(x, y)` | Correct with GPS measurement |
| `update_imu(yaw_rate, accel)` | Correct with IMU measurement |
| `state` | Current state as dict |

### How it works

**Predict:**
```
x_new = x + v·cos(yaw)·dt
y_new = y + v·sin(yaw)·dt
```
Covariance grows (uncertainty increases).

**Update:**
```
K = P·Hᵀ·(H·P·Hᵀ + R)⁻¹   (Kalman gain)
x = x + K·(z - H·x)          (correct state)
P = (I - K·H)·P              (reduce uncertainty)
```

### Sensor Fusion

| Sensor | Provides | Noise |
|--------|----------|-------|
| GPS | x, y | ±1-5m |
| IMU | yaw_rate, accel | drift over time |
| Encoder | v, Δx, Δy | accumulates error |

EKF combines them: GPS corrects position drift, IMU corrects yaw drift, encoder provides short-term accuracy.

### Config

```python
EKFConfig(
    dt=0.01,
    q_accel=0.5,       # process noise
    q_yaw_rate=0.1,
    q_speed=0.2,
    r_gps=1.0,         # measurement noise
    r_imu=0.1,
)
```

### Limitations

- 2D only (no z-axis)
- No loop closure (SLAM needed for that)
- Gaussian noise assumption (reality is messier)
