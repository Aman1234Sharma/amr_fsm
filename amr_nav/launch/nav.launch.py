import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_amr_nav = get_package_share_directory('amr_nav')

    rviz_config_file = os.path.join(pkg_amr_nav, 'config', 'nav_rviz.rviz')
    amcl_param_file = os.path.join(pkg_amr_nav, 'config', 'amcl.yaml')
    planner_param_file = os.path.join(pkg_amr_nav, 'config', 'planner_server.yaml')
    controller_param_file = os.path.join(pkg_amr_nav, 'config', 'controller_server.yaml')
    bt_navigator_param_file = os.path.join(pkg_amr_nav, 'config', 'bt_navigator.yaml')
    behavior_param_file = os.path.join(pkg_amr_nav, 'config', 'behaviour_server.yaml')  

    return LaunchDescription([

        # Map Server
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[
                {'yaml_filename': '/workspaces/amr_ws/src/amr_nav/maps/precision_lab_map.yaml'},
                {'use_sim_time': False}
            ]
        ),

        # AMCL
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

        # Planner Server
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

        # Controller Server
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

        # BT Navigator
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

        # Behavior Server
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

        # Lifecycle Manager
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

        # RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen'
        )
    ])
