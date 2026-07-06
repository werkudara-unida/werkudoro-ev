# ROS 2 Integration

## Status

Not yet implemented. This doc describes the planned integration.

---

## Workspace Structure

```
colcon_ws/
├── src/
│   ├── werkudoro_ev/          # this repo (overlay)
│   ├── werkudoro_description/ # URDF, meshes
│   ├── werkudoro_gazebo/      # world files, launch
│   └── werkudoro_bringup/     # full stack launch
```

## Nodes

### Sensor Nodes

| Node | Subscribes | Publishes |
|------|-----------|-----------|
| `camera_node` | `/gazebo/camera/image_raw` | `/camera/image_raw` (sensor_msgs/Image) |
| `imu_node` | `/gazebo/imu` | `/imu/data` (sensor_msgs/Imu) |
| `encoder_node` | `/gazebo/odom` | `/odom` (nav_msgs/Odometry) |
| `lidar_node` | `/gazebo/lidar/points` | `/scan` (sensor_msgs/LaserScan) |

### Perception Nodes

| Node | Subscribes | Publishes |
|------|-----------|-----------|
| `lane_detection_node` | `/camera/image_raw` | `/lanes` (custom msg) |
| `object_detection_node` | `/camera/image_raw` | `/detections` (vision_msgs/Detection2DArray) |

### Control Nodes

| Node | Subscribes | Publishes |
|------|-----------|-----------|
| `teleop_node` | keyboard input | `/cmd_vel` (geometry_msgs/Twist) |
| `ackermann_node` | `/cmd_vel` | `/cmd_ackermann` (custom msg) |
| `pid_node` | `/pid/error` | `/cmd_steering`, `/cmd_throttle` |

### Localization Node

| Node | Subscribes | Publishes |
|------|-----------|-----------|
| `localization_node` | `/imu/data`, `/odom` | `/tf`, `/pose` (geometry_msgs/PoseStamped) |

### Planning Nodes

| Node | Subscribes | Publishes |
|------|-----------|-----------|
| `global_planner_node` | `/pose`, `/map` | `/plan` (nav_msgs/Path) |
| `local_planner_node` | `/plan`, `/scan` | `/cmd_vel` |

## Launch Files

```bash
# Full stack
ros2 launch werkudoro_bringup full_stack.launch.py

# Just sensors
ros2 launch werkudoro_bringup sensors.launch.py

# Teleop only
ros2 launch werkudoro_bringup teleop.launch.py
```

## Custom Messages

### AckermannCmd.msg
```
float64 steering_angle    # rad
float64 speed             # m/s
```

### Lane.msg
```
float64 slope
float64 intercept
bool valid
```

### Lanes.msg
```
Lane left
Lane right
float64 offset_from_center
```
