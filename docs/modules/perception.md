# Perception Module

## lane_detection.py

Simple lane detector using Canny edge detection + Hough line transform.

### Pipeline

```
BGR → Grayscale → Gaussian Blur → Canny → ROI Mask → HoughLinesP → Lane fit
```

### Key Class

```python
LaneDetector(canny_low=50, canny_high=150, roi_top_ratio=0.45)
```

| Method | Input | Output |
|--------|-------|--------|
| `detect(frame)` | BGR image | (left_lane, right_lane) |
| `lane_offset(left, right, width)` | lanes + image width | offset in meters |

### Lane

```python
Lane(slope, intercept, valid)
```

### How it works

1. **Canny**: Finds edges in grayscale image
2. **ROI Mask**: Keeps only the road region (trapezoid at bottom of image)
3. **HoughLinesP**: Finds line segments in edges
4. **Classify**: Lines with negative slope → left lane, positive → right
5. **Fit**: Polynomial fit to get lane parameters

### Limitations

- Works on straight/slightly curved roads
- Struggles with shadows, worn markings, curves
- Full solution: deep learning (CNN-based) — future phase

---

## object_detection.py

YOLO-based object detector using Ultralytics.

### Key Class

```python
ObjectDetector(model_name='yolov8n.pt', confidence_threshold=0.5)
```

| Method | Input | Output |
|--------|-------|--------|
| `detect(frame)` | BGR image | list of Detection |

### Detection

```python
Detection(class_id, class_name, confidence, bbox, position)
```

### Supported Classes

YOLOv8 default: 80 COCO classes (person, car, truck, traffic light, stop sign, etc.)

### Model Sizes

| Model | Speed | Accuracy |
|-------|-------|----------|
| yolov8n | fastest | lowest |
| yolov8s | fast | low |
| yolov8m | medium | medium |
| yolov8l | slow | high |
| yolov8x | slowest | highest |

Default: `yolov8n` for simulation. Upgrade for real-world accuracy.
