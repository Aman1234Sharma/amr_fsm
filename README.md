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
---

## 🔌 Connecting to the AMR

Follow these steps to power on and connect to the AMR wirelessly via SSH:

1. 🔄 **Rotate the power knob** on the AMR to switch it on.
2. 📱 **Start your phone's mobile hotspot** with the following settings:
   - **SSID**: `IAFSM24`
   - **Password**: `iafsm#2017`
3. ⏳ **Wait 30–60 seconds** for the AMR to automatically connect to the hotspot.
4. 💻 On your laptop, **connect to the same Wi-Fi network** (`IAFSM24`).
5. 🔐 Open a terminal and run the following command to SSH into the AMR:
   ```bash
   ssh fsm-amr@192.168.43.227

⚙️ Note: The AMR is configured with a static IP 192.168.43.227, so you can reliably SSH into it after every boot.

You will be prompted to enter the password:
```bash
Password: iafsm#2017
```

## 2. **Set ROS 2 Environment Variables(For the new user, only one time step)**

### **On your laptop Laptop**:

1. **Set `ROS_DOMAIN_ID`**:
   - Use the same domain ID as the AMR to ensure both systems are communicating in the same DDS domain:

   ```bash
   export ROS_DOMAIN_ID=30  # Since on AMR ROS_DOMAIN_ID is already set as 30
   ```

2. **Set `ROS_HOSTNAME`**:
   - Replace `<pc-ip>` with the IP address of your laptop:

   ```bash
   export ROS_HOSTNAME=<pc-ip>  # Set to your laptop's IP address
   ```
By setting these environment variables, you ensure that both the **AMR robot** and **Ubuntu laptop** are communicating within the same **DDS domain** and are able to exchange messages across the network.


## 📁 Accessing Files in the Docker Container

Once logged in via SSH, you can access the files in the Docker container by running the following commands:
```bash
cd amr_fsm/src
./run.sh
source install/setup.bash
```

This will set up the environment to work with your AMR project files and dependencies.


## 🚀 Quick Start

```bash
# Launch full stack (navigation + odometry + visualization)
ros2 launch amr_bringup new_robot_bringup.launch.py
```
## 🖥️ Hardware Overview

### 🤖 Motor
- **Motor Driver**: Roboteq Brushless DC Motor Controller
- **Base Frame**: `base_link`
  
### ⚡ **CPU (Processor)**

- **Model**: Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz
- **Cores**: 4 cores, 8 threads
- **Base Clock**: 1.9 GHz
- **Max Clock**: 4.0 GHz
- **Architecture**: 64-bit

### 💾 **Memory (RAM)**

- **Total Memory**: 16 GB
  - **Channel A-DIMM0**: 8 GB DDR4 2667 MHz
  - **Channel B-DIMM0**: 8 GB DDR4 2667 MHz
- **Slots Used**: 2 out of 4 slots (Two empty slots for possible future upgrades)

### 📡 **Sensors**

- **LiDAR**: pepperl and fuchs lidar
  - **Model**: OMD60M-R2000-B23-V1V1D-1L 
  - **Sensor Type**: 2D LiDAR
  - **Range**: 0-60 meters
  - **Scan Rate**: 10-50 hz

- **Camera**: Intel RealSense D435i
  - **Sensor Type**: RGB-D Camera

  ## 🔗 Major Tech Stack Used

1. **[RTAB-Map ROS Wiki](http://wiki.ros.org/rtabmap_ros)**

2. **[Nav2 Documentation](https://docs.nav2.org/)**

3. **[Realsense ROS GitHub](https://github.com/IntelRealSense/realsense-ros)**



