from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Paths to included launch files
    pf_driver_launch = os.path.join(
        get_package_share_directory('pf_driver'),
        'launch',
        'r2000.launch.py'
    )

    amr_description_launch = os.path.join(
        get_package_share_directory('amr_description'),
        'launch',
        'display.launch.py'
    )

    roboteq_driver_launch = os.path.join(
        get_package_share_directory('roboteq_controller'),
        'launch',
        'driver.py'
    )

    return LaunchDescription([
        # 1. Launch the P+F R2000 LiDAR driver
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(pf_driver_launch)
        ),

        # 2. Start RTAB-Map's ICP Odometry Node
        Node(
            package='rtabmap_odom',
            executable='icp_odometry',
            name='icp_odometry',
            output='screen',
            parameters=[{'publish_tf': True}],
            remappings=[
                ('scan', 'pf/scan'),
                ('odom','lidar/odom')
            ]
        ),

        # 3. Launch robot URDF + static TFs
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(amr_description_launch)
        ),

        # 4. Launch Roboteq driver
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(roboteq_driver_launch)
        ),

        # 5. Launch filtered_laser_scan bounding_box_laser node
        Node(
            package='filtered_laser_scan',
            executable='bounding_box_laser',
            name='bounding_box_laser',
            output='screen'
        )
    ])
