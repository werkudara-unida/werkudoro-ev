"""Gazebo interface — placeholder for ROS 2 integration.

This module will contain the ROS 2 nodes and Gazebo plugin interfaces.
For now, it provides a mock interface for testing without Gazebo.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class SensorData:
    """Mock sensor data from Gazebo."""
    camera_image: np.ndarray | None = None
    imu_linear: tuple[float, float, float] = (0.0, 0.0, 0.0)
    imu_angular: tuple[float, float, float] = (0.0, 0.0, 0.0)
    encoder_speed: float = 0.0
    encoder_odometry: tuple[float, float, float] = (0.0, 0.0, 0.0)


class GazeboInterface:
    """Interface to Gazebo simulation.

    On Ubuntu with ROS 2, this will subscribe to Gazebo topics.
    For now, provides mock data for development.
    """

    def __init__(self, mock: bool = True):
        self.mock = mock
        self._step = 0

    def get_sensors(self) -> SensorData:
        """Get current sensor readings."""
        if self.mock:
            return self._mock_sensors()
        # TODO: ROS 2 subscriptions
        raise NotImplementedError("ROS 2 interface not yet implemented")

    def send_control(self, steering: float, throttle: float):
        """Send control commands to the vehicle."""
        if self.mock:
            return  # no-op in mock mode
        # TODO: Publish to /cmd_ackermann topic
        raise NotImplementedError("ROS 2 interface not yet implemented")

    def _mock_sensors(self) -> SensorData:
        """Generate mock sensor data for development."""
        self._step += 1
        t = self._step * 0.01

        return SensorData(
            camera_image=np.zeros((480, 640, 3), dtype=np.uint8),
            imu_linear=(0.0, 0.0, 9.81),
            imu_angular=(0.0, 0.0, 0.1 * np.sin(t)),
            encoder_speed=1.0 + 0.5 * np.sin(t),
            encoder_odometry=(t * 1.0, 0.0, 0.0),
        )


def demo():
    """Quick check with mock mode."""
    gz = GazeboInterface(mock=True)
    data = gz.get_sensors()
    assert data.camera_image is not None
    assert len(data.imu_linear) == 3
    gz.send_control(0.0, 0.5)
    print("gazebo_interface: mock OK")


if __name__ == "__main__":
    demo()
