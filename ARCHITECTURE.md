# System Architecture

## Data Flow

```
         ┌──────────────┐
         │   Camera     │
         └──────┬───────┘
                ▼
    ┌───────────────────────┐
    │   Lane Detection      │
    │   Object Detection    │
    └───────────┬───────────┘
                │
                ▼
┌─────┐   ┌─────────────┐   ┌─────────┐
│ IMU ├──►│  Localization├◄──┤ Encoder │
│     │   │    (EKF)     │   │         │
└─────┘   └──────┬──────┘   └─────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Path Planning  │
        │  A* + DWA      │
        └───────┬────────┘
                │
                ▼
        ┌────────────────┐
        │   Control      │
        │  PID + Pure    │
        │  Pursuit       │
        └───────┬────────┘
                │
                ▼
        ┌────────────────┐
        │  Ackermann     │
        │  Kinematics    │
        └───────┬────────┘
                │
                ▼
        ┌────────────────┐
        │  Gazebo Sim    │
        │  (Vehicle)     │
        └────────────────┘
```

---

## Module Structure

```
src/werkudoro/
├── vehicle/
│   ├── ackermann.py      # Ackermann steering kinematics
│   └── model.py          # Kinematic bicycle model
├── perception/
│   ├── lane_detection.py  # Canny + Hough lane detector
│   └── object_detection.py # YOLO wrapper
├── control/
│   ├── pid.py             # PID with anti-windup
│   └── pure_pursuit.py    # Path tracker
├── planning/
│   ├── global_planner.py  # A* on occupancy grid
│   └── local_planner.py   # DWA local planner
├── localization/
│   └── ekf.py             # Extended Kalman Filter
└── sim/
    └── gazebo_interface.py # Mock → ROS2 later
```

---

## ROS2 Nodes (planned)

```
camera_node         → /camera/image_raw
imu_node            → /imu/data
encoder_node        → /odom
lidar_node          → /scan

teleop_node         → /cmd_vel
controller_node     → /cmd_ackermann
planner_node        → /plan
localization_node   → /tf, /pose

rviz_node           → visualization
```

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Package Manager | uv |
| Language | Python 3.11+ |
| ML | PyTorch, Ultralytics YOLO |
| CV | OpenCV |
| Math | NumPy, SciPy |
| Middleware | ROS 2 Jazzy |
| Simulator | Gazebo Harmonic |
| Visualization | RViz2 |
