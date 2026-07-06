# Vehicle Module

## ackermann.py

Ackermann steering geometry — computes individual wheel angles from a single steering input.

### Why Ackermann?

In a real car, inner wheel turns more than outer wheel. If both turned the same angle, tires would scrub. Ackermann geometry eliminates this.

### Key Class

```python
AckermannKinematics(wheelbase=1.5, track_width=1.2)
```

| Method | Input | Output |
|--------|-------|--------|
| `wheel_angles(steering_angle)` | rad | dict of 4 wheel angles |
| `turning_radius(steering_angle)` | rad | radius in meters |
| `steering_angle(turning_radius)` | meters | rad |

### Math

```
cot(outer) = cot(inner) + T / L
```
- `L` = wheelbase
- `T` = track_width
- `inner` = wheel on inside of turn

---

## model.py

Kinematic bicycle model — simplifies 4 wheels to 2 (front + rear).

### Why bicycle model?

The math is simpler and accurate enough for low-speed simulation. At high speeds, a dynamic model (with tire slip) would be needed.

### Key Class

```python
VehicleModel(wheelbase=1.5, max_speed=11.1, max_steering=35°)
```

| Method | Description |
|--------|-------------|
| `step(state, dt, accel, steering_rate)` | Advance one timestep |

### State

```python
VehicleState(x, y, yaw, v, steering)
```

### Equations

```
x'     = x + v·cos(yaw)·dt
y'     = y + v·sin(yaw)·dt
yaw'   = yaw + (v/L)·tan(steering)·dt
v'     = v + accel·dt
```
