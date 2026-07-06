# Control Module

## pid.py

PID controller with anti-windup.

### Why PID?

The most common controller in robotics. Simple, effective, well-understood. For autonomous vehicles, PID handles:
- Speed control (throttle)
- Steering correction

### Key Class

```python
PIDController(kp=1.0, ki=0.0, kd=0.0, output_limit=1.0, integral_limit=1.0)
```

| Method | Description |
|--------|-------------|
| `update(error, dt)` | Compute control output |
| `reset()` | Zero internal state |

### Terms

- **P** (proportional): Reacts to current error. `kp * error`
- **I** (integral): Eliminates steady-state error. `ki * ∫error·dt`
- **D** (derivative): Dampens oscillation. `kd * d(error)/dt`

### Anti-Windup

Integral term is clamped to `integral_limit`. Without this, integral grows unbounded when actuator saturates, causing overshoot.

### Tuning

1. Start with `kp=1.0, ki=0, kd=0`
2. Increase `kp` until oscillation
3. Add `kd` to dampen
4. Add `ki` to eliminate steady-state error

---

## pure_pursuit.py

Pure pursuit path tracker.

### Why Pure Pursuit?

Simple, robust, works well at varying speeds. Used in self-driving cars since the 90s.

### Key Class

```python
PurePursuit(config=PurePursuitConfig())
```

| Method | Description |
|--------|-------------|
| `set_path(waypoints)` | Set path to follow (Nx2 array) |
| `compute(x, y, yaw, speed)` | Return (steering, throttle) |

### How it works

1. Find point on path at lookahead distance from vehicle
2. Compute curvature to reach that point: `κ = 2·sin(α) / L`
3. Convert curvature to steering angle: `δ = atan(κ·wheelbase)`
4. Slow down in sharp turns

### Adaptive Lookahead

Lookahead distance increases with speed:
```
L = base + speed × factor
```
This prevents weaving at low speed and cutting corners at high speed.

### Config

```python
PurePursuitConfig(
    lookahead_distance=2.0,  # base lookahead (m)
    min_lookahead=0.5,
    max_lookahead=5.0,
    speed_factor=0.5,         # lookahead += speed × factor
)
```
