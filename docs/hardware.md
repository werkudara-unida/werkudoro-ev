# Hardware Deployment

## Status

Deferred. This doc captures future considerations.

---

## Target Hardware

| Component | Model | Role |
|-----------|-------|------|
| Main computer | Jetson Orin Nano | AI inference, planning |
| MCU | ESP32 / STM32 | Motor control, sensor read |
| Camera | USB / CSI | Perception |
| IMU | MPU6050 / BNO055 | Orientation |
| Motor | DC geared | Drive |
| Encoder | Optical / Magnetic | Speed feedback |
| Battery | LiPo 3S-4S | Power |

## Deployment Flow

```
1. Validate full stack in Gazebo (current phase)
2. Port Python nodes to ROS 2 on Jetson
3. Flash ESP32 with motor control firmware
4. Wire sensors + motors
5. Tune PID on real hardware
6. Integrate perception + planning
7. Test in controlled environment
8. Road testing
```

## Key Differences: Sim vs Real

| Aspect | Simulation | Real |
|--------|-----------|------|
| Noise | Gaussian, configurable | Real-world, unpredictable |
| Latency | Deterministic | Variable (network, compute) |
| Physics | Simplified | Tire slip, friction, vibration |
| Sensors | Perfect calibration | Needs calibration |
| Safety | Unlimited retries | Hardware damage risk |

## ESP32 Firmware (planned)

```cpp
// Basic structure
void setup() {
    initMotorDriver();
    initEncoder();
    initIMU();
    initWiFi();  // for ROS 2 micro-ROS
}

void loop() {
    readSensors();
    if (newCommand) {
        applyMotorControl(command);
    }
    publishSensorData();
}
```

## Calibration

Real hardware needs calibration that simulation doesn't:
- IMU bias correction
- Encoder ticks-to-meters conversion
- Camera intrinsics/extrinsics
- Steering angle offset
- Motor response curve
