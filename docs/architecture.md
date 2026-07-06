# Architecture

## Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Gazebo Simulator                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  Camera   │  │   IMU    │  │ Encoder  │  │ LiDAR  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  │
│       └──────────────┼────────────┼─────────────┘       │
│                      ▼            ▼                      │
│              ┌─────────────────────────┐                │
│              │       ROS 2 Layer       │                │
│              │  topics, services, tf   │                │
│              └───────────┬─────────────┘                │
└──────────────────────────┼──────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                  Python Stack (werkudoro)                │
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌────────────┐  │
│  │ Perception  │───►│ Localization│───►│  Planning  │  │
│  │  (vision)   │    │   (EKF)     │    │ (A* + DWA) │  │
│  └─────────────┘    └─────────────┘    └─────┬──────┘  │
│                                               │         │
│                                               ▼         │
│                                       ┌────────────┐   │
│                                       │  Control   │   │
│                                       │ (PID + PP) │   │
│                                       └─────┬──────┘   │
│                                             │           │
│                                             ▼           │
│                                     ┌──────────────┐   │
│                                     │  Ackermann   │   │
│                                     │  Kinematics  │   │
│                                     └──────┬───────┘   │
└────────────────────────────────────────────┼────────────┘
                                             │
                                             ▼
                                     ┌──────────────┐
                                     │   Gazebo     │
                                     │   Vehicle    │
                                     └──────────────┘
```

## Design Decisions

### Why Python first?

ROS 2 supports both C++ and Python. Python chosen for:
- Faster prototyping
- Easier debugging
- ML ecosystem (PyTorch, OpenCV) is Python-native
- C++ later for performance-critical nodes if needed

### Why separate Python modules from ROS 2 nodes?

Each module (e.g., `control/pid.py`) is a pure Python class. ROS 2 nodes will be thin wrappers that subscribe to topics, call these classes, and publish results.

Benefits:
- Testable without ROS 2
- Portable to other frameworks
- Clear separation of algorithm vs infrastructure

### Why mock Gazebo interface?

`sim/gazebo_interface.py` returns fake sensor data. This lets us develop and test the entire stack without Gazebo running. When we move to Ubuntu + ROS 2, we swap mock for real ROS 2 subscriptions.

## Data Flow

1. **Sensors** publish raw data (images, IMU, encoder)
2. **Perception** processes images → lanes, objects
3. **Localization** fuses IMU + encoder → pose estimate
4. **Planning** computes global path (A*) + local trajectory (DWA)
5. **Control** converts trajectory → steering + throttle commands
6. **Ackermann** converts commands → individual wheel angles
7. **Gazebo** receives commands, updates simulation, produces new sensor data

Loop runs at 100 Hz (control), perception at camera frame rate (~30 Hz).

## Naming Conventions

- `snake_case` for functions, variables, files
- `PascalCase` for classes
- Module files match class names: `pid.py` → `PIDController`
- Each module has a `demo()` function for standalone testing
