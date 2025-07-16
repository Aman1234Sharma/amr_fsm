# 🤖 amr_fsm – Autonomous Mobile Robot System (ROS 2 Humble)

A modular and extensible Autonomous Mobile Robot (AMR) software stack built on **ROS 2 Humble**. This project integrates LiDAR-based SLAM, RGB-D odometry, wheel odometry, sensor fusion, and navigation using Nav2. It is designed for real-world deployment and simulation alike.

---

## 🗂️ Repository Structure
amr_fsm/
├── amr_bringup/ # Legacy bring-up launch files
├── amr_description/ # Robot URDF + TF configuration
├── amr_mapping_and_odometry/ # Launch files for mapping, odometry
├── sensor_fusion/ # Sensor fusion with EKF
├── amr_nav/ # Nav2 planner/controller configs
├── filtered_laser_scan/ # Custom node to filter laser data
├── roboteq_controller/ # Motor driver interface
├── pf_driver/ # P+F R2000 LiDAR ROS 2 driver
├── realsense2_camera/ # RealSense RGB-D driver
└── ...
