# Development Roadmap

Scope: Simulation only (Gazebo + ROS 2 Jazzy). No hardware deployment.

---

## Phase 1 — Python Foundation ✅

- [x] Project setup (uv, pyproject.toml)
- [x] Ackermann kinematics
- [x] Bicycle vehicle model
- [x] PID controller
- [x] Pure pursuit
- [x] A* global planner
- [x] DWA local planner
- [x] EKF localization
- [x] Lane detection (OpenCV)
- [x] Object detection (YOLO)
- [x] Mock Gazebo interface

---

## Phase 2 — ROS2 Workspace

- [ ] Install ROS 2 Jazzy + Gazebo Harmonic on Ubuntu
- [ ] Create colcon workspace
- [ ] Create URDF vehicle model
- [ ] Spawn robot in Gazebo
- [ ] Basic topic structure

---

## Phase 3 — Sensor Nodes

- [ ] Camera node (publish /camera/image_raw)
- [ ] IMU node (publish /imu/data)
- [ ] Encoder node (publish /odom)
- [ ] LiDAR node (publish /scan)

---

## Phase 4 — Control Nodes

- [ ] Teleop node (keyboard → cmd_vel)
- [ ] Ackermann controller node (cmd_vel → cmd_ackermann)
- [ ] PID node (error → throttle/steering)

---

## Phase 5 — Perception Nodes

- [ ] Lane detection node (image → lanes)
- [ ] Object detection node (image → detections)
- [ ] Traffic sign detection

---

## Phase 6 — Localization

- [ ] EKF node (fuse IMU + encoder + GPS)
- [ ] SLAM (optional)
- [ ] AMCL (optional)

---

## Phase 7 — Planning + Navigation

- [ ] Global planner node (A* → path)
- [ ] Local planner node (DWA → velocity)
- [ ] Nav2 integration
- [ ] Waypoint following

---

## Phase 8 — Full Autonomous Stack

- [ ] Integrate all nodes
- [ ] Obstacle avoidance
- [ ] End-to-end autonomous navigation
- [ ] Debugging + tuning

---

## Phase 9 — Polish

- [ ] Launch file (full stack)
- [ ] RViz2 visualization
- [ ] Bag recording
- [ ] Documentation
