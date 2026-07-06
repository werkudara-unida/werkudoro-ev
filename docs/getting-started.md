# Getting Started

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Ubuntu 24.04 (for ROS 2 + Gazebo)

## Install

```bash
git clone git@github.com:werkudara-unida/werkudoro-ev.git
cd werkudoro-ev
uv sync
```

## Verify

```bash
uv run python -c "
from werkudoro.vehicle.ackermann import demo; demo()
from werkudoro.vehicle.model import demo; demo()
from werkudoro.control.pid import demo; demo()
from werkudoro.planning.global_planner import demo; demo()
from werkudoro.localization.ekf import demo; demo()
print('ALL PASSED')
"
```

## Project Structure

```
werkudoro-ev/
├── pyproject.toml          # deps (uv)
├── src/werkudoro/          # Python package
│   ├── vehicle/            # kinematics + model
│   ├── perception/         # lane + object detection
│   ├── control/            # PID + pure pursuit
│   ├── planning/           # A* + DWA
│   ├── localization/       # EKF
│   └── sim/                # Gazebo interface
├── docs/                   # this folder
├── urdf/                   # vehicle model (Phase 2)
├── worlds/                 # Gazebo worlds
└── launch/                 # ROS 2 launch files
```

## Next Steps

- Read [Architecture](architecture.md) for design decisions
- Read [Modules](modules/) for per-module docs
- Check [ROADMAP.md](../ROADMAP.md) for what's next
