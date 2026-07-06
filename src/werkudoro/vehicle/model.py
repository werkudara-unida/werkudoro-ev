"""Simple bicycle vehicle model for simulation."""

import numpy as np
from dataclasses import dataclass


@dataclass
class VehicleState:
    """Vehicle state: position, velocity, heading."""
    x: float = 0.0
    y: float = 0.0
    yaw: float = 0.0       # heading (rad)
    v: float = 0.0          # linear velocity (m/s)
    steering: float = 0.0   # steering angle (rad)

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.y, self.yaw, self.v, self.steering])


class VehicleModel:
    """Kinematic bicycle model.

    Args:
        wheelbase: Distance between axles (m).
        max_speed: Maximum speed (m/s).
        max_steering: Maximum steering angle (rad).
    """

    def __init__(
        self,
        wheelbase: float = 1.5,
        max_speed: float = 11.1,      # ~40 km/h
        max_steering: float = np.radians(35),
    ):
        self.wheelbase = wheelbase
        self.max_speed = max_speed
        self.max_steering = max_steering

    def step(
        self,
        state: VehicleState,
        dt: float,
        acceleration: float = 0.0,
        steering_rate: float = 0.0,
    ) -> VehicleState:
        """Advance the vehicle one timestep.

        Args:
            state: Current state.
            dt: Timestep (s).
            acceleration: Desired acceleration (m/s^2).
            steering_rate: Desired steering angle change (rad/s).

        Returns:
            New VehicleState.
        """
        # clamp inputs
        v = np.clip(state.v + acceleration * dt, -self.max_speed, self.max_speed)
        steering = np.clip(
            state.steering + steering_rate * dt,
            -self.max_steering,
            self.max_steering,
        )

        # kinematic bicycle model
        x = state.x + v * np.cos(state.yaw) * dt
        y = state.y + v * np.sin(state.yaw) * dt
        yaw = state.yaw + (v / self.wheelbase) * np.tan(steering) * dt

        return VehicleState(x=x, y=y, yaw=yaw, v=v, steering=steering)


def demo():
    """Sanity check."""
    model = VehicleModel()
    state = VehicleState()

    # drive straight
    for _ in range(100):
        state = model.step(state, dt=0.01, acceleration=1.0)

    assert state.v > 0.5, f"expected moving, got v={state.v}"
    assert abs(state.yaw) < 0.01, f"expected straight, got yaw={state.yaw}"

    # turn left
    for _ in range(200):
        state = model.step(state, dt=0.01, steering_rate=5.0)

    assert state.yaw > 0.1, f"expected turning left, got yaw={state.yaw}"

    print("vehicle_model: all checks passed")


if __name__ == "__main__":
    demo()
