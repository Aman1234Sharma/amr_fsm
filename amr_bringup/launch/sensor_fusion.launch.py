import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Shared launch paths
    pf_driver_launch = os.path.join(
        get_package_share_directory('pf_driver'), 'launch', 'r2000.launch.py')

    roboteq_launch = os.path.join(
        get_package_share_directory('roboteq_controller'), 'launch', 'driver.py')

    amr_description_launch = os.path.join(
        get_package_share_directory('amr_description'), 'launch', 'display.launch.py')

    ekf_config = os.path.join(
        get_package_share_directory('amr_bringup'), 'launch', 'ekf.yaml')

    # --- Optional: RealSense + RGBD Odometry (commented) ---
    # realsense_launch = os.path.join(
    #     get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')

    # visual_odom_params = [{
    #     'frame_id': 'base_link',
    #     'subscribe_depth': True,
    #     'subscribe_odom_info': True,
    #     'approx_sync': False,
    #     'wait_imu_to_init': True
    # }]
    # visual_odom_remappings = [
    #     ('imu', '/imu/data'),
    #     ('rgb/image', '/camera/color/image_raw'),
    #     ('rgb/camera_info', '/camera/color/camera_info'),
    #     ('depth/image', '/camera/aligned_depth_to_color/image_raw'),
    #     ('/odom', '/camera/odom')
    # ]

    return LaunchDescription([
        # --- Wheel Odometry ---
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(roboteq_launch)
        ),

        # --- LiDAR Driver ---
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(pf_driver_launch)
        ),

        # --- Filtered Laser Scan Node ---
        Node(
            package='filtered_laser_scan',
            executable='bounding_box_laser',
            name='bounding_box_laser',
            output='screen'
        ),

        # --- LiDAR Odometry (ICP) ---
        Node(
            package='rtabmap_odom',
            executable='icp_odometry',
            name='icp_odometry',
            output='screen',
            parameters=[{'publish_tf': False}],
            remappings=[
                ('scan', 'pf/scan'),
                ('odom', 'lidar/odom')
            ]
        ),

        # --- EKF Node (robot_localization) ---
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_config]
        ),

        # --- Optional: RealSense + VSLAM ---
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(realsense_launch),
        #     launch_arguments={
        #         'camera_namespace': '',
        #         'enable_gyro': 'true',
        #         'enable_accel': 'true',
        #         'unite_imu_method': LaunchConfiguration('unite_imu_method'),
        #         'align_depth.enable': 'true',
        #         'enable_sync': 'true',
        #         'rgb_camera.profile': '640x360x30',
        #         'publish_tf': 'true'
        #     }.items()
        # ),

        # Node(
        #     package='rtabmap_odom',
        #     executable='rgbd_odometry',
        #     output='screen',
        #     parameters=visual_odom_params,
        #     remappings=visual_odom_remappings
        # ),

        # Node(
        #     package='imu_filter_madgwick',
        #     executable='imu_filter_madgwick_node',
        #     output='screen',
        #     parameters=[{
        #         'use_mag': False,
        #         'world_frame': 'enu',
        #         'publish_tf': False
        #     }],
        #     remappings=[('imu/data_raw', '/camera/imu')]
        # ),

        # --- Robot Description / Static TFs ---
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(amr_description_launch)
        ),
    ])
