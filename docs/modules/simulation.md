# Simulation Module

## gazebo_interface.py

Interface between Python stack and Gazebo simulator.

### Current State

Mock mode — returns fake sensor data. Allows full stack testing without Gazebo.

### Key Class

```python
GazeboInterface(mock=True)
```

| Method | Description |
|--------|-------------|
| `get_sensors()` | Get sensor readings |
| `send_control(steering, throttle)` | Send commands to vehicle |

### Mock Data

```python
SensorData(
    camera_image=np.zeros((480, 640, 3)),  # blank image
    imu_linear=(0, 0, 9.81),               # gravity only
    imu_angular=(0, 0, 0.1·sin(t)),        # gentle oscillation
    encoder_speed=1.0 + 0.5·sin(t),        # varying speed
    encoder_odometry=(t, 0, 0),            # moving forward
)
```

### ROS 2 Integration (Phase 2+)

When moved to Ubuntu with ROS 2:

```python
GazeboInterface(mock=False)
```

Will subscribe to:
- `/camera/image_raw` → camera_image
- `/imu/data` → imu_linear, imu_angular
- `/odom` → encoder_speed, encoder_odometry

Will publish to:
- `/cmd_ackermann` → steering, throttle

### Why mock?

- Develop on macOS without ROS 2
- Test algorithms in isolation
- CI/CD without simulator dependency
