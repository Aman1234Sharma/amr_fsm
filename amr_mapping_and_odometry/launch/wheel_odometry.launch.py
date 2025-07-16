from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Paths to launch files
    roboteq_launch = os.path.join(
        get_package_share_directory('roboteq_controller'),
        'launch',
        'driver.py' 
    )

    amr_description_launch = os.path.join(
        get_package_share_directory('amr_description'),
        'launch',
        'display.launch.py'
    )
    
    return LaunchDescription([
        # 1. Roboteq Controller Driver
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(roboteq_launch)
        ),

        # 2. Robot Description / URDF / TF
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(amr_description_launch)
        )
    ])
