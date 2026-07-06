# Autonomous Electric Vehicle
## Technical Specification

---

## Vision

Build a fully autonomous electric vehicle simulation from scratch using ROS 2 and Gazebo,
with deep understanding of every subsystem — from kinematics to perception to planning.

Learning-first approach. No black boxes.

---

## Scope

Simulation only (Gazebo). Hardware deployment deferred.

---

## Goals

- Build every major subsystem ourselves
- Understand the math and physics behind each component
- Keep everything modular
- Reproducible experiments
- Open-source

---

## Target Platform

### Simulation (primary)

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic
- Python 3.11+
- uv (package management)

### Hardware (future consideration)

- Jetson Orin Nano
- Raspberry Pi 5
- ESP32

---

## Vehicle Type

- Ackermann Steering Vehicle
- Rear Wheel Drive
- Electric Motor
- Max Speed: 40 km/h (simulation)

---

## Sensors

### Mandatory

- RGB Camera
- IMU
- Wheel Encoder

### Optional

- LiDAR
- GPS
- Depth Camera

---

## Software Stack

### Development

| Layer | Tool |
|-------|------|
| Package Manager | uv |
| Language | Python |
| ML | PyTorch, Ultralytics YOLO |
| CV | OpenCV |
| Math | NumPy, SciPy |
| Visualization | Matplotlib |

### Simulation

| Layer | Tool |
|-------|------|
| Simulator | Gazebo Harmonic |
| Middleware | ROS 2 Jazzy |
| Visualization | RViz2 |

---

## Core Modules (built)

| Module | Status | Description |
|--------|--------|-------------|
| `vehicle/ackermann` | done | Ackermann steering kinematics |
| `vehicle/model` | done | Kinematic bicycle model |
| `perception/lane_detection` | done | Canny + Hough lane detector |
| `perception/object_detection` | done | YOLO wrapper |
| `control/pid` | done | PID with anti-windup |
| `control/pure_pursuit` | done | Path tracker |
| `planning/global_planner` | done | A* on occupancy grid |
| `planning/local_planner` | done | DWA local planner |
| `localization/ekf` | done | Extended Kalman Filter |
| `sim/gazebo_interface` | done | Mock interface (ROS2 later) |

---

## Core Features

- [x] Ackermann Steering Model
- [x] Vehicle Controller (PID)
- [x] Pure Pursuit Path Tracking
- [x] Lane Detection
- [x] Object Detection
- [x] Global Path Planning (A*)
- [x] Local Path Planning (DWA)
- [x] Localization (EKF)
- [ ] Teleoperation
- [ ] Camera Pipeline (ROS2)
- [ ] LiDAR Pipeline (ROS2)
- [ ] Traffic Sign Detection
- [ ] Mapping
- [ ] Navigation (Nav2)
- [ ] Obstacle Avoidance
- [ ] Autonomous Driving

---

## Performance Target

| Metric | Target |
|--------|--------|
| Simulation FPS | >30 FPS |
| Camera | 30 FPS |
| LiDAR | 10 Hz |
| Control Loop | 100 Hz |
| Localization Error | <10 cm |

---

## Non Functional Requirements

- Modular
- Extensible
- Deep understanding of every component
- Hardware-ready (code runs on sim, portable to real vehicle)
- Fully documented
