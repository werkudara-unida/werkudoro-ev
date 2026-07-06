# TODO

## Simulation Setup

- [ ] Install ROS 2 Jazzy on Ubuntu server
- [ ] Install Gazebo Harmonic
- [ ] Create ROS2 workspace
- [ ] Create URDF vehicle model
- [ ] Configure Gazebo physics
- [ ] Spawn robot in Gazebo

## Vehicle (Python — done)

- [x] Ackermann kinematics
- [x] Bicycle vehicle model

## Sensors (Python — done)

- [x] Lane detection (OpenCV)
- [x] Object detection (YOLO)

## Sensors (ROS2 — pending)

- [ ] Camera node
- [ ] IMU node
- [ ] Encoder node
- [ ] LiDAR node

## Control (Python — done)

- [x] PID controller
- [x] Pure pursuit

## Control (ROS2 — pending)

- [ ] Teleop node
- [ ] Ackermann controller node
- [ ] CmdAckermann publisher

## Planning (Python — done)

- [x] A* global planner
- [x] DWA local planner

## Localization (Python — done)

- [x] EKF

## Localization (ROS2 — pending)

- [ ] EKF node (robot_localization)
- [ ] SLAM (optional)
- [ ] AMCL (optional)

## Perception (ROS2 — pending)

- [ ] Lane detection node
- [ ] Object detection node
- [ ] Traffic sign detection

## Navigation (ROS2 — pending)

- [ ] Nav2 integration
- [ ] Waypoint following
- [ ] Obstacle avoidance
- [ ] Full autonomous navigation

## Integration

- [ ] Launch file (full stack)
- [ ] RViz2 visualization
- [ ] Bag recording for debugging
