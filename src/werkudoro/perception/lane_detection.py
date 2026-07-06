"""Lane detection using OpenCV."""

import cv2
import numpy as np
from dataclasses import dataclass


@dataclass
class Lane:
    """Detected lane parameters."""
    slope: float = 0.0
    intercept: float = 0.0
    valid: bool = False


class LaneDetector:
    """Simple lane detector using Canny edge + Hough transform.

    Args:
        canny_low: Lower Canny threshold.
        canny_high: Upper Canny threshold.
        roi_top_ratio: Top of ROI as fraction of image height.
    """

    def __init__(
        self,
        canny_low: int = 50,
        canny_high: int = 150,
        roi_top_ratio: float = 0.45,
    ):
        self.canny_low = canny_low
        self.canny_high = canny_high
        self.roi_top_ratio = roi_top_ratio

    def detect(self, frame: np.ndarray) -> tuple[Lane, Lane]:
        """Detect left and right lanes in a frame.

        Args:
            frame: BGR image (H, W, 3).

        Returns:
            Tuple of (left_lane, right_lane).
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, self.canny_low, self.canny_high)

        h, w = edges.shape
        mask = np.zeros_like(edges)
        roi = np.array([
            [(0, h), (w // 2 - 50, int(h * self.roi_top_ratio)),
             (w // 2 + 50, int(h * self.roi_top_ratio)), (w, h)]
        ])
        cv2.fillPoly(mask, roi, 255)
        masked = cv2.bitwise_and(edges, mask)

        lines = cv2.HoughLinesP(
            masked, 1, np.pi / 180, 50,
            minLineLength=50, maxLineGap=150
        )

        left_lane = Lane()
        right_lane = Lane()

        if lines is None:
            return left_lane, right_lane

        left_xs, left_ys = [], []
        right_xs, right_ys = [], []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 == x1:
                continue
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) < 0.3:
                continue
            if slope < 0:  # left lane
                left_xs.extend([x1, x2])
                left_ys.extend([y1, y2])
            else:  # right lane
                right_xs.extend([x1, x2])
                right_ys.extend([y1, y2])

        if len(left_xs) >= 2:
            coeffs = np.polyfit(left_ys, left_xs, 1)
            left_lane = Lane(slope=1.0 / coeffs[0], intercept=-coeffs[1] / coeffs[0], valid=True)

        if len(right_xs) >= 2:
            coeffs = np.polyfit(right_ys, right_xs, 1)
            right_lane = Lane(slope=1.0 / coeffs[0], intercept=-coeffs[1] / coeffs[0], valid=True)

        return left_lane, right_lane

    def lane_offset(self, left: Lane, right: Lane, frame_width: int) -> float:
        """Compute vehicle offset from lane center.

        Args:
            left: Left lane.
            right: Right lane.
            frame_width: Image width.

        Returns:
            Offset in meters (positive = right of center).
        """
        if not left.valid or not right.valid:
            return 0.0

        center = frame_width // 2
        left_x = int(left.slope * (frame_width * 0.75) + left.intercept)
        right_x = int(right.slope * (frame_width * 0.75) + right.intercept)
        lane_center = (left_x + right_x) // 2

        return (center - lane_center) / 100.0  # rough pixels-to-meters


def demo():
    """Quick check with a blank image."""
    detector = LaneDetector()
    blank = np.zeros((480, 640, 3), dtype=np.uint8)
    left, right = detector.detect(blank)
    assert not left.valid and not right.valid
    print("lane_detection: all checks passed")


if __name__ == "__main__":
    demo()
