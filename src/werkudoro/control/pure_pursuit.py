"""Pure pursuit path tracker."""

import numpy as np
from dataclasses import dataclass


@dataclass
class PurePursuitConfig:
    """Pure pursuit parameters."""
    lookahead_distance: float = 2.0   # m
    min_lookahead: float = 0.5        # m
    max_lookahead: float = 5.0        # m
    speed_factor: float = 0.5         # lookahead scales with speed


class PurePursuit:
    """Pure pursuit controller for path tracking.

    References:
        - Coulter, R.C. (1992). Implementation of the Pure Pursuit
          Path Tracking Algorithm.
    """

    def __init__(self, config: PurePursuitConfig | None = None):
        self.config = config or PurePursuitConfig()
        self._path: np.ndarray | None = None
        self._target_idx = 0

    def set_path(self, path: np.ndarray):
        """Set the path to follow.

        Args:
            path: Nx2 array of (x, y) waypoints.
        """
        self._path = path
        self._target_idx = 0

    def _find_lookahead_point(
        self, x: float, y: float, lookahead: float
    ) -> tuple[float, float] | None:
        """Find the point on path at lookahead distance from vehicle."""
        if self._path is None or len(self._path) < 2:
            return None

        for i in range(self._target_idx, len(self._path)):
            px, py = self._path[i]
            dist = np.sqrt((px - x) ** 2 + (py - y) ** 2)
            if dist >= lookahead:
                self._target_idx = i
                return (px, py)

        # fallback: last point
        self._target_idx = len(self._path) - 1
        return tuple(self._path[-1])

    def compute(
        self, x: float, y: float, yaw: float, speed: float
    ) -> tuple[float, float]:
        """Compute steering and throttle commands.

        Args:
            x, y: Vehicle position.
            yaw: Vehicle heading (rad).
            speed: Current speed (m/s).

        Returns:
            (steering_angle, throttle) tuple.
        """
        # adaptive lookahead
        lookahead = np.clip(
            self.config.lookahead_distance + speed * self.config.speed_factor,
            self.config.min_lookahead,
            self.config.max_lookahead,
        )

        target = self._find_lookahead_point(x, y, lookahead)
        if target is None:
            return 0.0, 0.0

        tx, ty = target

        # transform target to vehicle frame
        dx = tx - x
        dy = ty - y
        local_x = dx * np.cos(yaw) + dy * np.sin(yaw)
        local_y = -dx * np.sin(yaw) + dy * np.cos(yaw)

        # pure pursuit curvature: κ = 2 * α / L²
        # where α = atan2(local_y, local_x), L = lookahead
        alpha = np.arctan2(local_y, local_x)
        curvature = 2.0 * np.sin(alpha) / lookahead

        # steering angle (bicycle model)
        wheelbase = 1.5
        steering = np.arctan(curvature * wheelbase)

        # throttle: slow down in turns
        throttle = np.clip(1.0 - abs(steering) * 2, 0.3, 1.0)

        return float(steering), float(throttle)


def demo():
    """Sanity check: follow a straight line."""
    pp = PurePursuit()
    path = np.array([[i * 0.5, 0.0] for i in range(20)])
    pp.set_path(path)

    # start at origin, heading right
    steering, throttle = pp.compute(0.0, 0.0, 0.0, 1.0)
    assert abs(steering) < 0.1, f"straight should have small steering, got {steering}"
    assert throttle > 0

    print("pure_pursuit: all checks passed")


if __name__ == "__main__":
    demo()
