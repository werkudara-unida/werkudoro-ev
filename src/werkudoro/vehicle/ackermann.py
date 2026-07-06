"""Ackermann steering kinematics.

References:
    - https://en.wikipedia.org/wiki/Ackermann_steering_geometry
"""

import numpy as np


class AckermannKinematics:
    """Compute Ackermann steering angles for a 4-wheel vehicle.

    Args:
        wheelbase: Distance between front and rear axles (m).
        track_width: Distance between left and right wheels (m).
    """

    def __init__(self, wheelbase: float = 1.5, track_width: float = 1.2):
        self.wheelbase = wheelbase
        self.track_width = track_width

    def steering_angle(self, turning_radius: float) -> float:
        """Compute inner wheel steering angle from turning radius.

        Args:
            turning_radius: Radius of the turn circle (m). Use np.inf for straight.

        Returns:
            Steering angle in radians.
        """
        return np.arctan2(self.wheelbase, turning_radius)

    def wheel_angles(self, steering_angle: float) -> dict[str, float]:
        """Compute individual wheel angles from a single steering angle.

        Returns:
            Dict with front_left, front_right, rear_left, rear_right.
            Inner wheel has larger angle magnitude than outer wheel.
        """
        if abs(steering_angle) < 1e-6:
            return {
                "front_left": 0.0,
                "front_right": 0.0,
                "rear_left": 0.0,
                "rear_right": 0.0,
            }

        # cot(inner) = L / R_inner
        # cot(outer) = cot(inner) + T / L
        L = self.wheelbase
        T = self.track_width

        cot_inner = L / (L * np.tan(abs(steering_angle)))
        cot_outer = cot_inner + T / L
        angle_inner = np.arctan(1.0 / cot_inner)
        angle_outer = np.arctan(1.0 / cot_outer)

        if steering_angle > 0:  # turning left — left wheel is inner
            return {
                "front_left": angle_inner,
                "front_right": angle_outer,
                "rear_left": 0.0,
                "rear_right": 0.0,
            }
        else:  # turning right — right wheel is inner
            return {
                "front_left": -angle_outer,
                "front_right": -angle_inner,
                "rear_left": 0.0,
                "rear_right": 0.0,
            }

    def turning_radius(self, steering_angle: float) -> float:
        """Compute turning radius from steering angle.

        Returns:
            Turning radius (m). np.inf if steering is zero.
        """
        if abs(steering_angle) < 1e-6:
            return np.inf
        return self.wheelbase / np.tan(abs(steering_angle))


def demo():
    """Quick sanity check."""
    ack = AckermannKinematics(wheelbase=1.5, track_width=1.2)

    # straight
    angles = ack.wheel_angles(0.0)
    assert all(v == 0.0 for v in angles.values()), "straight should be zero"

    # turn left 30 deg — left wheel (inner) > right wheel (outer)
    left = ack.wheel_angles(np.radians(30))
    assert left["front_left"] > left["front_right"]

    # turn right 30 deg — right wheel (inner) has larger magnitude
    right = ack.wheel_angles(np.radians(-30))
    assert abs(right["front_right"]) > abs(right["front_left"])

    # radius
    r = ack.turning_radius(np.radians(30))
    assert r > 0

    print("ackermann: all checks passed")


if __name__ == "__main__":
    demo()
