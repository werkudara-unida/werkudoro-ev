# werkudoro-ev

> Autonomous Electric Vehicle — built from scratch to understand every bolt and byte.

```
Camera → Object Detection → Localization → Path Planning → Controller → Gazebo
```

![trust me bro i'm an engineer](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHBwaDRnODR1eGQyMTkydXo5bGR4cnJsM29hano4cjF3Y3c0Z2FncSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1BeGcXm9dtRMhDAStl/giphy.gif)

*us building this autonomous stack, probably*

---

## What is this?

A from-scratch autonomous driving stack in ROS 2 + Gazebo. Not a tutorial project — a deep dive.
Every module is hand-coded to understand the *why*, not just the *how*.

## Stack

| Layer | Tool |
|-------|------|
| Package Manager | uv |
| Language | Python 3.11+ |
| ML | PyTorch · Ultralytics YOLO |
| CV | OpenCV |
| Math | NumPy · SciPy |
| Middleware | ROS 2 Jazzy |
| Simulator | Gazebo Harmonic |

## Modules

```
src/werkudoro/
├── vehicle/
│   ├── ackermann.py      ← steering kinematics
│   └── model.py          ← kinematic bicycle model
├── perception/
│   ├── lane_detection.py  ← Canny + Hough
│   └── object_detection.py ← YOLO wrapper
├── control/
│   ├── pid.py             ← PID with anti-windup
│   └── pure_pursuit.py    ← path tracker
├── planning/
│   ├── global_planner.py  ← A* on grid
│   └── local_planner.py   ← DWA
├── localization/
│   └── ekf.py             ← Extended Kalman Filter
└── sim/
    └── gazebo_interface.py ← mock → ROS2 later
```

## Quick Start

```bash
# clone
git clone git@github.com:werkudara-unida/werkudoro-ev.git
cd werkudoro-ev

# install deps
uv sync

# run all module tests
uv run python -c "
from werkudoro.vehicle.ackermann import demo; demo()
from werkudoro.vehicle.model import demo; demo()
from werkudoro.perception.lane_detection import demo; demo()
from werkudoro.control.pid import demo; demo()
from werkudoro.control.pure_pursuit import demo; demo()
from werkudoro.planning.global_planner import demo; demo()
from werkudoro.planning.local_planner import demo; demo()
from werkudoro.localization.ekf import demo; demo()
from werkudoro.sim.gazebo_interface import demo; demo()
print('ALL PASSED')
"
```

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | ✅ | Python foundation — all core modules |
| 2 | 🔜 | ROS 2 workspace + URDF |
| 3 | | Sensor nodes (camera, IMU, encoder) |
| 4 | | Control nodes (teleop, PID, pure pursuit) |
| 5 | | Perception nodes |
| 6 | | Localization (EKF, SLAM) |
| 7 | | Planning + Nav2 |
| 8 | | Full autonomous stack |
| 9 | | Polish + docs |

See [ROADMAP.md](ROADMAP.md) for full breakdown.

## Principles

- **Understand everything.** No black boxes. If it's in the code, we wrote it.
- **Simulation first.** Full stack in Gazebo before touching hardware.
- **Modular.** Each module is standalone. Mix and match.
- **Documented.** Every engineering decision explained.

## License

MIT
