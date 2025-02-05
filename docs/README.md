# Project Documentation

This project implements an ultra-low-cost AI-based SLAM drone system with the following components:

- **Simulator Module (Rust):** Integrates with AirSim (HTTP API) and PX4 SITL (UDP MAVLink) for sensor and control simulation.
- **Training Module (Python):** Trains a TinyML model using JAX, Brax, and Flax on a custom drone environment and integrates AirSim data.
- **Controller Module (Rust):** Provides full implementations for flight control, sensor fusion (3D Kalman filter), visual SLAM (ORB feature detection and solvePnP pose estimation), grid-based A* path planning, camera calibration (chessboard detection), and diagnostics (file logging with timestamps).
- **Unreal Project:** Hosts the drone vehicle and a cityscape simulation.
  
Further documentation will detail system architecture, calibration procedures, advanced SLAM algorithms, control loop tuning, telemetry, testing, and continuous integration workflows.
