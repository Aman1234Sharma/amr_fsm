from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node, SetParameter
import os
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    localization = LaunchConfiguration('localization')

    parameters={
        'frame_id':'base_link',
        'odom_frame_id':'odom',
        'odom_tf_linear_variance':0.001,
        'odom_tf_angular_variance':0.001,
        'subscribe_depth': False,
        'subscribe_rgbd':True,
        'subscribe_scan':True,
        'approx_sync':True,
        'approx_sync_max_interval': 0.05,
        'sync_queue_size': 10,
        'RGBD/NeighborLinkRefining': 'true',
        'RGBD/ProximityBySpace':     'true',
        'RGBD/ProximityByTime':      'false',
        'RGBD/ProximityPathMaxNeighbors': '10',
        'Reg/Strategy':              '1',
        'Vis/MinInliers':            '12',
        'RGBD/OptimizeFromGraphEnd': 'false',
        'RGBD/OptimizeMaxError':     '4',
        'Reg/Force3DoF':             'true',
        'Grid/FromDepth':            'false',
        'Mem/STMSize':               '30',
        'RGBD/LocalRadius':          '5',
        'Icp/CorrespondenceRatio':   '0.2',
        'Icp/PM':                    'false',
        'Icp/PointToPlane':          'false',
        'Icp/MaxCorrespondenceDistance': '0.15',
        'Icp/VoxelSize':             '0.05'
    }
    
    remappings=[
         ('rgb/image',       '/camera/camera/color/image_raw'),
         ('depth/image',     '/camera/camera/aligned_depth_to_color/image_raw'),
         ('rgb/camera_info', '/camera/camera/color/camera_info'),
         ('scan',            '/pf/scan')
         ]
    
    config_rviz = os.path.join(
        get_package_share_directory('rtabmap_demos'), 'config', 'demo_robot_mapping.rviz'
    )

    # Paths to external launch files
    realsense_launch = os.path.join(
        get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')

    pfdriver_launch = os.path.join(
        get_package_share_directory('pf_driver'), 'launch', 'r2000.launch.py')

    amr_display_launch = os.path.join(
        get_package_share_directory('amr_description'), 'launch', 'display.launch.py')

    return LaunchDescription([

        # Launch arguments
        DeclareLaunchArgument('rtabmap_viz',  default_value='true',  description='Launch RTAB-Map UI (optional).'),
        DeclareLaunchArgument('rviz',         default_value='false', description='Launch RVIZ (optional).'),
        DeclareLaunchArgument('localization', default_value='false', description='Launch in localization mode.'),
        DeclareLaunchArgument('rviz_cfg', default_value=config_rviz,  description='Configuration path of rviz2.'),

        SetParameter(name='use_sim_time', value=False),

        # Include Realsense2 launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(realsense_launch),
            launch_arguments={
                'enable_rgbd': 'true',
                'enable_sync': 'true',
                'align_depth.enable': 'true',
                'enable_color': 'true',
                'enable_depth': 'true',
                'rgb_camera.color_profile': '640x480x60',
                'depth_module.depth_profile': '640x480x60'
                
            }.items()
        ),

        # Include PF Driver launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(pfdriver_launch)
        ),

        # Include AMR URDF visualization launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(amr_display_launch)
        ),

        # Include Roboteq Controller Launch 
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('roboteq_controller'),
                    'launch',
                    'driver.py'
                ])
            )
        ),

        # LiDAR Odometry Node (RTAB-Map ICP)
        Node(
            package='rtabmap_odom',
            executable='icp_odometry',
            name='icp_odometry',
            output='screen',
            parameters=[{'publish_tf': True}],
            remappings=[
                ('scan', 'pf/scan'),
                ('odom', 'lidar/odom')
            ]
        ),

        # RGBD Sync Node
        Node(
            package='rtabmap_sync', executable='rgbd_sync', output='screen',
            parameters=[parameters],
            remappings=remappings),

        # SLAM Node
        Node(
            condition=UnlessCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters],
            remappings=remappings,
            arguments=['-d']
            ),

        # Localization Node
        Node(
            condition=IfCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters, {
                'Mem/IncrementalMemory':'False',
                'Mem/InitWMWithAllNodes':'True'}],
            remappings=remappings),

        # RTAB-Map Visualization
        Node(
            package='rtabmap_viz', executable='rtabmap_viz', output='screen',
            condition=IfCondition(LaunchConfiguration("rtabmap_viz")),
            parameters=[parameters],
            remappings=remappings),

        # RViz2
        Node(
            package='rviz2', executable='rviz2', name="rviz2", output='screen',
            condition=IfCondition(LaunchConfiguration("rviz")),
            arguments=["-d", LaunchConfiguration("rviz_cfg")])
    ])
