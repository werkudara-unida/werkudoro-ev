"""Local planner using dynamic window approach."""

import numpy as np
from dataclasses import dataclass


@dataclass
class LocalPlannerConfig:
    """Local planner parameters."""
    max_speed: float = 11.1          # m/s
    max_accel: float = 3.0           # m/s^2
    max_yaw_rate: float = np.radians(40)  # rad/s
    dt: float = 0.1                  # s
    predict_time: float = 2.0        # s
    heading_weight: float = 0.15
    clearance_weight: float = 1.0
    velocity_weight: float = 0.2


class LocalPlanner:
    """Dynamic Window Approach (DWA) local planner.

    References:
        - Fox, D., Burgard, W., & Thrun, S. (1997).
          The dynamic window approach to collision avoidance.
    """

    def __init__(self, config: LocalPlannerConfig | None = None):
        self.config = config or LocalPlannerConfig()

    def compute(
        self,
        x: float, y: float, yaw: float,
        v: float, omega: float,
        goal: tuple[float, float],
        obstacles: list[tuple[float, float]],
    ) -> tuple[float, float]:
        """Compute best (velocity, yaw_rate) command.

        Args:
            x, y, yaw: Current pose.
            v, omega: Current velocity and yaw rate.
            goal: (gx, gy) goal position.
            obstacles: List of (ox, oy) obstacle positions.

        Returns:
            (v, omega) best command.
        """
        cfg = self.config

        # dynamic window
        vs = [
            max(0.0, v - cfg.max_accel * cfg.dt),
            min(cfg.max_speed, v + cfg.max_accel * cfg.dt),
            max(-cfg.max_yaw_rate, omega - cfg.max_yaw_rate * cfg.dt),
            min(cfg.max_yaw_rate, omega + cfg.max_yaw_rate * cfg.dt),
        ]

        best_cost = float("inf")
        best_v, best_omega = v, omega

        # sample velocities
        for tv in np.linspace(vs[0], vs[1], 10):
            for tw in np.linspace(vs[2], vs[3], 10):
                # predict trajectory
                cost = self._trajectory_cost(x, y, yaw, tv, tw, goal, obstacles)
                if cost < best_cost:
                    best_cost = cost
                    best_v, best_omega = tv, tw

        return float(best_v), float(best_omega)

    def _trajectory_cost(
        self, x, y, yaw, v, omega, goal, obstacles
    ) -> float:
        """Cost of a predicted trajectory."""
        cfg = self.config
        x_, y_, yaw_ = x, y, yaw
        dist = 0.0

        steps = int(cfg.predict_time / cfg.dt)
        for _ in range(steps):
            x_ += v * np.cos(yaw_) * cfg.dt
            y_ += v * np.sin(yaw_) * cfg.dt
            yaw_ += omega * cfg.dt

            # obstacle cost
            for ox, oy in obstacles:
                d = np.sqrt((x_ - ox) ** 2 + (y_ - oy) ** 2)
                if d < 0.5:
                    return float("inf")  # collision

            dist += cfg.dt

        # goal heading cost
        goal_angle = np.arctan2(goal[1] - y_, goal[0] - x_)
        heading_err = abs(self._normalize_angle(goal_angle - yaw_))

        # clearance cost
        min_obs_dist = float("inf")
        for ox, oy in obstacles:
            d = np.sqrt((x_ - ox) ** 2 + (y_ - oy) ** 2)
            min_obs_dist = min(min_obs_dist, d)
        clearance = 1.0 / (min_obs_dist + 0.01)

        # goal distance cost
        goal_dist = np.sqrt((x_ - goal[0]) ** 2 + (y_ - goal[1]) ** 2)

        return (
            cfg.heading_weight * heading_err
            + cfg.clearance_weight * clearance
            + cfg.velocity_weight * goal_dist
        )

    @staticmethod
    def _normalize_angle(angle: float) -> float:
        while angle > np.pi:
            angle -= 2 * np.pi
        while angle < -np.pi:
            angle += 2 * np.pi
        return angle


def demo():
    """Quick check: planner should move toward goal."""
    planner = LocalPlanner()
    v, omega = planner.compute(
        x=0, y=0, yaw=0, v=1.0, omega=0.0,
        goal=(5.0, 0.0),
        obstacles=[],
    )
    assert v > 0, "should move forward"
    assert abs(omega) < 0.5, "should not swerve for straight goal"
    print("local_planner: all checks passed")


if __name__ == "__main__":
    demo()
