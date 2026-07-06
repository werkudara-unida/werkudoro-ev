"""Object detection using Ultralytics YOLO."""

import numpy as np
from dataclasses import dataclass
from ultralytics import YOLO


@dataclass
class Detection:
    """Single object detection."""
    class_id: int
    class_name: str
    confidence: float
    bbox: tuple[float, float, float, float]  # x1, y1, x2, y2
    position: tuple[float, float] = (0.0, 0.0)  # world coordinates


class ObjectDetector:
    """YOLO-based object detector.

    Args:
        model_name: YOLO model name (e.g., 'yolov8n.pt').
        confidence_threshold: Minimum confidence for detection.
        classes: List of class IDs to detect. None = all.
    """

    def __init__(
        self,
        model_name: str = "yolov8n.pt",
        confidence_threshold: float = 0.5,
        classes: list[int] | None = None,
    ):
        self.model = YOLO(model_name)
        self.confidence_threshold = confidence_threshold
        self.classes = classes

    def detect(self, frame: np.ndarray) -> list[Detection]:
        """Detect objects in a frame.

        Args:
            frame: BGR image (H, W, 3).

        Returns:
            List of Detection objects.
        """
        results = self.model.predict(
            frame,
            conf=self.confidence_threshold,
            classes=self.classes,
            verbose=False,
        )

        detections = []
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = self.model.names[cls_id]
                detections.append(
                    Detection(
                        class_id=cls_id,
                        class_name=cls_name,
                        confidence=conf,
                        bbox=(float(x1), float(y1), float(x2), float(y2)),
                    )
                )

        return detections


def demo():
    """Quick check without loading a model (just import test)."""
    print("object_detection: import OK")


if __name__ == "__main__":
    demo()
