import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Paths to other launch files
    pf_driver_launch = os.path.join(
        get_package_share_directory('pf_driver'), 'launch', 'r2000.launch.py')

    roboteq_launch = os.path.join(
        get_package_share_directory('roboteq_controller'), 'launch', 'driver.py')

    amr_description_launch = os.path.join(
        get_package_share_directory('amr_description'), 'launch', 'display.launch.py')

    # Config files
    pkg_amr_nav = get_package_share_directory('amr_nav')
    rviz_config_file = os.path.join(pkg_amr_nav, 'config', 'nav_rviz.rviz')
    amcl_param_file = os.path.join(pkg_amr_nav, 'config', 'amcl.yaml')
    planner_param_file = os.path.join(pkg_amr_nav, 'config', 'planner_server.yaml')
    controller_param_file = os.path.join(pkg_amr_nav, 'config', 'controller_server.yaml')
    bt_navigator_param_file = os.path.join(pkg_amr_nav, 'config', 'bt_navigator.yaml')
    behavior_param_file = os.path.join(pkg_amr_nav, 'config', 'behaviour_server.yaml')
    ekf_config = os.path.join(
        get_package_share_directory('sensor_fusion'), 'config', 'ekf.yaml')

    return LaunchDescription([

        # --- Wheel Odometry (Roboteq) ---
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(roboteq_launch)
        ),

        # --- LiDAR Driver (PF Driver) ---
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

        # --- ICP Odometry from LiDAR ---
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

        # --- EKF Localization ---
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_config]
        ),

        # --- Static TFs and URDF Model ---
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(amr_description_launch)
        ),

        # --- Nav2 Map Server ---
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[
                {'yaml_filename': os.path.join(pkg_amr_nav, 'maps', 'precision_lab_map.yaml')},
                {'use_sim_time': False}
            ]
        ),

        # --- Nav2 AMCL Localization ---
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[
                amcl_param_file,
                {'use_sim_time': False}
            ]
        ),

        # --- Nav2 Planner Server ---
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[
                planner_param_file,
                {'use_sim_time': False}
            ]
        ),

        # --- Nav2 Controller Server ---
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[
                controller_param_file,
                {'use_sim_time': False}
            ]
        ),

        # --- Nav2 BT Navigator ---
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[
                bt_navigator_param_file,
                {'use_sim_time': False}
            ]
        ),

        # --- Nav2 Behavior Server ---
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            output='screen',
            parameters=[
                behavior_param_file,
                {'use_sim_time': False}
            ]
        ),

        # --- Nav2 Lifecycle Manager ---
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_nav',
            output='screen',
            parameters=[
                {'use_sim_time': False},
                {'autostart': True},
                {
                    'node_names': [
                        'map_server',
                        'amcl',
                        'planner_server',
                        'controller_server',
                        'bt_navigator',
                        'behavior_server'
                    ]
                }
            ]
        ),

        # --- RViz Visualization ---
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen'
        )
    ])
