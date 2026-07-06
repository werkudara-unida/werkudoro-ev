# Planning Module

## global_planner.py

A* path planner on a 2D occupancy grid.

### Why A*?

Optimal, complete, well-understood. Guaranteed shortest path if heuristic is admissible.

### Key Class

```python
AStarPlanner(resolution=0.1, obstacle_threshold=128)
```

| Method | Input | Output |
|--------|-------|--------|
| `plan(grid, start, goal)` | 2D array, (row,col)×2 | list of (x,y) waypoints |

### Grid

```
0-127   = free space
128+    = obstacle
```

### Heuristic

Octile distance (8-directional grid):
```
h = max(dr, dc) + (√2 - 1) × min(dr, dc)
```

### Why not RRT/RRT*?

A* is deterministic and faster for known environments. RRT/RRT* are better for high-dimensional spaces or unknown environments — future consideration.

---

## local_planner.py

Dynamic Window Approach (DWA) local planner.

### Why DWA?

Reactive, handles dynamic obstacles, works in real-time. Standard in ROS 2 Nav2.

### Key Class

```python
LocalPlanner(config=LocalPlannerConfig())
```

| Method | Input | Output |
|--------|-------|--------|
| `compute(x, y, yaw, v, omega, goal, obstacles)` | state + goal + obstacles | (v, omega) command |

### How it works

1. **Dynamic window**: Compute reachable velocities given current state + acceleration limits
2. **Sample**: Try combinations of (v, ω) in the window
3. **Simulate**: For each sample, predict trajectory forward
4. **Score**: Weighted sum of:
   - Heading error to goal
   - Distance to nearest obstacle
   - Goal distance
5. **Select**: Lowest cost wins

### Config

```python
LocalPlannerConfig(
    max_speed=11.1,           # m/s (~40 km/h)
    max_accel=3.0,            # m/s²
    max_yaw_rate=40°/s,
    dt=0.1,                   # prediction timestep
    predict_time=2.0,         # how far to look ahead
    heading_weight=0.15,
    clearance_weight=1.0,
    velocity_weight=0.2,
)
```

### Limitations

- Local optimal only (no全局 awareness)
- Struggles in tight spaces with many obstacles
- Nav2's TEB planner handles complex scenarios better
