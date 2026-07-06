"""PID controller."""

import time


class PIDController:
    """Standard PID controller with anti-windup.

    Args:
        kp: Proportional gain.
        ki: Integral gain.
        kd: Derivative gain.
        output_limit: Max absolute output (clamps).
        integral_limit: Max absolute integral term (anti-windup).
    """

    def __init__(
        self,
        kp: float = 1.0,
        ki: float = 0.0,
        kd: float = 0.0,
        output_limit: float = 1.0,
        integral_limit: float = 1.0,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_limit = output_limit
        self.integral_limit = integral_limit

        self._integral = 0.0
        self._prev_error = 0.0
        self._prev_time: float | None = None

    def reset(self):
        """Reset internal state."""
        self._integral = 0.0
        self._prev_error = 0.0
        self._prev_time = None

    def update(self, error: float, dt: float | None = None) -> float:
        """Compute PID output.

        Args:
            error: Current error (setpoint - measured).
            dt: Timestep (s). If None, uses wall-clock time.

        Returns:
            Control output, clamped to output_limit.
        """
        now = time.monotonic()
        if dt is None:
            if self._prev_time is None:
                dt = 0.01
            else:
                dt = now - self._prev_time
        self._prev_time = now

        if dt <= 0:
            return 0.0

        # proportional
        p = self.kp * error

        # integral with anti-windup
        self._integral += error * dt
        self._integral = max(-self.integral_limit, min(self.integral_limit, self._integral))
        i = self.ki * self._integral

        # derivative (on error)
        d = self.kd * (error - self._prev_error) / dt if dt > 0 else 0.0
        self._prev_error = error

        # output
        output = p + i + d
        return max(-self.output_limit, min(self.output_limit, output))


def demo():
    """Sanity check: PID should converge to zero error."""
    pid = PIDController(kp=1.0, ki=0.1, kd=0.01, output_limit=10.0)

    # simulate plant: output directly changes state
    state = 0.0
    setpoint = 5.0

    for _ in range(500):
        error = setpoint - state
        ctrl = pid.update(error, dt=0.01)
        state += ctrl * 0.01

    assert abs(state - setpoint) < 0.5, f"PID did not converge: state={state}"
    print("pid: all checks passed")


if __name__ == "__main__":
    demo()
