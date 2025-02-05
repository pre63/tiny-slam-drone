# Ultra-Low-Cost AI-Based Visual-SLAM Drone

## Project Overview  
This project aims to develop an ultra-low-cost autonomous drone that employs AI-powered simultaneous localization and mapping (SLAM) to enable GPS-free navigation. The design integrates an Arduino Nano 33 BLE Sense for sensor fusion and real-time processing, an ESP32-CAM for vision-based SLAM, and an F450 quadcopter frame as a robust mechanical platform. The entire software stack is implemented in Rust, leveraging its performance, memory safety, and concurrency features to handle real-time control, sensor fusion, and embedded AI inference. AirSim, a photorealistic simulator built on Unreal Engine, is chosen for simulation to validate the visual SLAM algorithms and autonomous control system before deployment on physical hardware.

### Software Architecture and Implementation  
The drone’s software is developed entirely in Rust to ensure high performance and robustness. The architecture is organized into several key areas:

- **Embedded Development:**  
  The firmware for both the Arduino Nano 33 BLE Sense and the ESP32-CAM is written using libraries such as `embedded-hal`, `nrf52840-hal`, and `esp-idf-sys`. These libraries provide hardware abstraction necessary for interfacing with sensors and peripherals.

- **Real-Time Flight Control:**  
  Real-time control loops are managed using the `rtic` framework, ensuring that motor control, sensor data acquisition, and other time-critical tasks are performed with minimal latency.

- **Sensor Fusion and SLAM:**  
  The onboard IMU data is processed using `nalgebra` and an EKF implementation (such as `ekf-rs`) to estimate the drone’s orientation and position. For computer vision, `opencv-rust` and `imageproc` are employed to implement feature extraction algorithms like ORB, with potential enhancements using deep learning-based methods such as SuperPoint.

- **AI Inference:**  
  The ESP32-CAM handles depth estimation and other AI inference tasks using TinyML models. Libraries such as `tflite-rs` or `tract` are utilized to optimize and run these models on the limited hardware.

- **Telemetry and Communication:**  
  Communication between the drone and the ground control station is achieved using `mavlink-rs` for MAVLink protocol handling and `serialport` for low-level data transmission.

### SLAM Pipeline  
The SLAM pipeline is designed to integrate visual data with inertial measurements for real-time environment mapping and autonomous navigation. The process is divided into several key stages:

1. **Feature Extraction:**  
   The system extracts visual features from the camera feed using ORB algorithms provided by `opencv-rust`. In scenarios requiring higher accuracy, a deep learning-based approach such as SuperPoint may be incorporated.

2. **Depth Estimation:**  
   A neural network model, such as MiDaS, is deployed on the ESP32-CAM using TinyML techniques to estimate scene depth from the monocular camera input.

3. **Pose Estimation:**  
   The extracted visual features and depth information are combined with inertial measurements from the Arduino Nano 33 BLE Sense using an Extended Kalman Filter (EKF). This fusion, implemented with `nalgebra`, provides robust real-time estimates of the drone’s pose.

4. **Path Planning and Navigation:**  
   The control system uses PID algorithms, potentially implemented via `pid-rs`, to adjust motor speeds based on the estimated position and orientation. Additional sensors (VL53L0X and HC-SR04) assist in altitude regulation and obstacle avoidance, ensuring safe navigation.

### Simulation Environment: AirSim with PX4 SITL  
Prior to deploying the system on hardware, extensive testing will be performed in a simulation environment using AirSim combined with PX4 SITL. AirSim offers a photorealistic simulation environment based on Unreal Engine, which is particularly well-suited for testing vision-based SLAM. The simulation process includes:

- Installing and configuring AirSim alongside PX4 SITL to simulate realistic flight dynamics and sensor outputs.
- Loading a quadrotor model equipped with virtual cameras and IMU sensors into AirSim.
- Implementing a Rust-based SLAM node to process the simulated camera feed in real time.
- Integrating MAVROS for telemetry and motor control, ensuring that simulated data closely mirrors expected real-world performance.
- Evaluating the SLAM pipeline and control algorithms in a series of obstacle-rich scenarios to validate autonomous navigation capabilities.

### Deployment Plan  
The deployment process is structured into multiple phases to ensure thorough testing and gradual integration:

1. **Module Development:**  
   Develop and test individual Rust-based modules, including the SLAM processing on the ESP32-CAM and sensor fusion on the Arduino Nano 33 BLE Sense.

2. **Simulation Testing:**  
   Integrate all modules within the AirSim simulation environment and perform comprehensive testing using PX4 SITL. This phase focuses on validating the performance of AI inference, sensor fusion, and flight control algorithms under realistic conditions.

3. **Hardware Integration:**  
   Once simulation results are satisfactory, deploy the software to the physical drone components. This includes flashing the firmware onto the Arduino and ESP32 boards and assembling the complete hardware platform.

4. **Field Testing and Optimization:**  
   Conduct controlled flight tests to gather telemetry and performance data. Analyze the data to optimize AI models, adjust control parameters, and refine sensor fusion algorithms. Iterative testing will address any discrepancies between simulation and real-world performance.

5. **Final Validation:**  
   After iterative improvements, perform final validation flights to ensure the system reliably achieves autonomous navigation and obstacle avoidance in diverse environments.

### Challenges and Considerations  
Several challenges must be addressed to ensure the success of this project. First, support for Rust in embedded flight controller environments is still developing; hence, low-level implementations for PWM control, IMU sensor fusion, and PID loops will need to be crafted using available Rust hardware abstraction libraries. Second, deploying AI inference on embedded hardware with Rust remains experimental, necessitating careful optimization of TinyML models using `tflite-rs` to guarantee real-time performance on the ESP32-CAM. Third, establishing robust communication between Rust-based flight software and PX4’s MAVLink protocol requires integrating `mavlink-rs` and ensuring reliable data exchange between the drone and the ground control station.


## Related Projects

1. **RustFlightX by jbcaron**: his open-source project focuses on developing an autonomous drone system for a 2-meter wingspan motor glider using Rust.t utilizes the ESP32 microcontroller with RTOS, emphasizing Rust's application in drone development.
2. **Arduino Nano Quadcopter**: n Arduino-based, 3D-printed nano quadcopter project that employs DC brushed motors and the Arduino Nano board.hile it doesn't utilize Rust or advanced SLAM techniques, it showcases the feasibility of building cost-effective drones with Arduino components.
3. **LSD-SLAM with ROS-based Drones**:  series demonstrating the implementation of Large-Scale Direct Monocular SLAM (LSD-SLAM) using ROS and Parrot AR.Drones within a Gazebo simulation environment.lthough this project doesn't employ Rust or the specified hardware, it provides insights into SLAM implementation on drones.

### Conclusion  
This project sets out to pioneer the integration of Rust-based embedded systems with AI-driven SLAM for ultra-low-cost autonomous drone navigation. By combining the strengths of Rust in real-time processing and memory safety with the photorealistic simulation capabilities of AirSim and the robust flight dynamics of PX4 SITL, the project promises a scalable and efficient solution for GPS-free autonomous flight. This comprehensive approach not only minimizes hardware costs but also pushes the boundaries of open-source, Rust-based embedded flight software, contributing valuable advancements to the field of autonomous aerial robotics.



## Bill of Materials (BOM)  
The following table details the components required for the drone, including specifications, quantities, and estimated costs:

| **Component**                             | **Specifications**                                                       | **Quantity** | **Estimated Cost (USD)** |
|-------------------------------------------|--------------------------------------------------------------------------|--------------|--------------------------|
| **Flight Controller & Processing**      |                                                                          |              |                          |
| Arduino Nano 33 BLE Sense                 | ARM Cortex-M4F, integrated 9-axis IMU (LSM9DS1), BLE 5.0                   | 1            | $30                      |
| ESP32-CAM                                 | OV2640 2MP camera, WiFi connectivity, low-power AI inference             | 1            | $10                      |
| **Frame & Mechanical Structure**          |                                                                          |              |                          |
| F450 Quadcopter Frame                     | Glass fiber composite, 450mm wheelbase                                   | 1            | $20                      |
| Landing Gear                              | Plastic, lightweight mounting components                                 | 1 set        | $5                       |
| **Motors & Propulsion**                   |                                                                          |              |                          |
| 2212 1000KV Brushless Motors              | Suitable for 3S/4S LiPo batteries, standard F450 configuration             | 4            | ~$40 (approximately $10 each) |
| 30A Electronic Speed Controllers (ESCs)   | BLHeli-S compatible, PWM control                                          | 4            | ~$40 (approximately $10 each) |
| 10-inch Propellers                        | 2-blade ABS design, compatible with 2212 motors                           | 2 pairs      | $10                      |
| **Power System**                          |                                                                          |              |                          |
| 3S LiPo Battery (2200mAh)                 | 11.1V, 30C discharge, provides power to the entire system                  | 1            | $25                      |
| 5V UBEC Step-Down Converter               | Regulates power for Arduino and ESP32-CAM                                 | 1            | $5                       |
| XT60 Connectors & Wiring                  | High-current connectors for reliable power distribution                   | 1 set        | $5                       |
| **Sensors & AI SLAM Components**          |                                                                          |              |                          |
| VL53L0X ToF Sensor                        | Short-range depth sensor for obstacle detection and SLAM integration      | 1            | $10                      |
| HC-SR04 Ultrasonic Sensor                 | For altitude hold and additional obstacle avoidance                       | 1            | $3                       |
| **Communication & Control**               |                                                                          |              |                          |
| PWM Motor Driver (MOSFET-based)           | Enables motor control via the Arduino                                   | 1            | $5                       |
| NRF24L01 Wireless Module                  | Low-power telemetry and remote control communication                      | 1            | $5                       |
| **Miscellaneous**                         |                                                                          |              |                          |
| Jumper Wires & Connectors                 | Dupont and JST connectors for internal wiring                             | 1 set        | $5                       |
| Heat Shrink Tubing & Solder               | For secure and reliable electrical connections                            | 1 set        | $5                       |

The total estimated cost for the complete system is approximately $223, providing an affordable platform for experimentation and the development of AI-driven autonomous flight capabilities.
