# Autonomous Mobile Robot (AMR) - ROS 2 Humble

This repository contains the ROS 2 Humble-based software stack developed for controlling and navigating an Autonomous Mobile Robot (AMR) designed at IAFSM. It includes everything from sensor drivers and state publishers to full navigation, mapping, and visualization.

---

## 📦 Package Overview

### 🧠 `amr_bringup`

- `new_robot_bringup.launch.py`: A unified launch file that starts the entire stack, including odometry, mapping/localization, sensor drivers, and navigation.
- Launching this file:
  - Initializes all essential nodes.
  - Enables users to send navigation goals via RViz or the `/navigate_to_pose` action interface.

---

### 🦾 `amr_description`

- `display.launch.py`: Launches RViz2 with TFs, robot model, and sensor visuals.
- Loads the robot’s URDF/Xacro description and starts TF broadcasting.

---

### 🗺️ `amr_mapping_and_odometry`

- Contains:
  - Individual odometry launch files for different odometry sources.
  - Mapping launch file for:
    - 2D Occupancy Grid Map
    - 3D Pointcloud Map

---

### 🤖 `amr_nav`

- `behaviour_tree/`:
  - Includes multiple behavior trees.
  - `nav2_recovery.xml`: Final recovery behavior tree used (based on Nav2 docs).
- `config/`:
  - YAML configuration files for:
    - Planner Server
    - Controller Server
    - Behavior Tree Server
    - Costmaps
    - Recovery Server
    - amcl
- `launch/nav.launch.py`: Most recent and stable launch file that brings up the complete navigation stack.
- `maps/`: Environment maps of:
  - IAFSM Lab
  - Precision Shop
  - Machine Shop

---

### 🧹 `filtered_laser_scan`

- Python scripts to remove robot's own corner edges from the LiDAR scan.
- Helps improve map clarity and localization stability.

---

### 🔧 Sensor and Driver Packages

- `pf_lidar_ros2_driver`:
  - ROS 2 driver for the ProFusion LiDAR used onboard the AMR.

- `realsense_ros`:
  - Official Intel RealSense ROS 2 wrapper for the D435i camera.

- `roboteq_motor_driver`:
  - Custom ROS 2 driver to interface with Roboteq motor controllers for mobile base control.

---

## 🚀 Quick Start

```bash
# Launch full stack (navigation + odometry + visualization)
ros2 launch amr_bringup new_robot_bringup.launch.py



