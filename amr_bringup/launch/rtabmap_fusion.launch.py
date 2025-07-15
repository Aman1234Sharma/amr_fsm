from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import GroupAction, IncludeLaunchDescription
from launch_ros.actions import PushRosNamespace
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([

        # Include amr_description display.launch.py
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('amr_description'),
                    'launch',
                    'display.launch.py'
                ])
            ])
        ),
        

        # Include Realsense2 Camera Launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('realsense2_camera'),
                    'launch',
                    'rs_launch.py'
                ])
            ]),
            launch_arguments={
                'enable_rgbd': 'true',
                'enable_sync': 'true',
                'align_depth.enable': 'true',
                'enable_color': 'true',
                'enable_depth': 'true',
                'rgb_camera.color_profile': '640x480x30',
                'depth_module.depth_profile': '640x480x30'
            }.items()
        ),

        # Include Roboteq Controller Launch, diff_tf.py publish tf from odom to base link
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('roboteq_controller'),
                    'launch',
                    'driver.py'
                ])
            ])
        ),

        # Include R2000 LiDAR Launch
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('pf_driver'),
                    'launch',
                    'r2000.launch.py'
                ])
            ])
        ),

        # RTAB-Map and RGBD Sync Group
        GroupAction([
            PushRosNamespace('rtabmap'),

            # RGBD Sync Node
            Node(
                package='rtabmap_sync',
                executable='rgbd_sync',
                name='rgbd_sync',
                output='screen',
                remappings=[
                    ('rgb/image', '/camera/camera/color/image_raw'),
                    ('depth/image', '/camera/camera/depth/image_rect_raw'),
                    ('rgb/camera_info', '/camera/camera/color/camera_info'),
                    ('rgbd_image', 'rgbd_image')
                ],
                parameters=[
                    {'approx_sync': True}
                ]
            ),

            # RTAB-Map Node
            Node(
                package='rtabmap_slam',
                executable='rtabmap',
                name='rtabmap',
                output='screen',
                arguments=['--delete_db_on_start'],
                parameters=[
                    {'frame_id': 'base_link'},
                    {'odom_frame_id':'odom'},
                    {'subscribe_depth': False},
                    {'subscribe_rgbd': True},
                    {'subscribe_scan': True},
                    {'queue_size': 10},
                    {'publish_tf':True},   # map to odom

                    # RTAB-Map Parameters
                    {'RGBD/NeighborLinkRefining': 'true'},
                    {'RGBD/ProximityBySpace': 'true'},
                    {'RGBD/ProximityByTime': 'false'},
                    {'RGBD/ProximityPathMaxNeighbors': '10'},
                    {'RGBD/AngularUpdate': '0.01'},
                    {'RGBD/LinearUpdate': '0.01'},
                    {'RGBD/OptimizeFromGraphEnd': 'false'},
                    {'RGBD/OptimizeMaxError': '4'},
                    {'Grid/FromDepth': 'false'},
                    {'Mem/STMSize': '30'},
                    {'RGBD/LocalRadius': '5'},
                    {'Icp/CorrespondenceRatio':'0.2'},
                    {'Reg/Force3DoF': 'true'},
                    {'Reg/Strategy': '1'},
                    {'Vis/MinInliers': '12'},
                    {'Icp/VoxelSize': '0.05'},
                    {'Icp/MaxCorrespondenceDistance': '0.15'}
                ],
                remappings=[
                    ('odom', '/roboteq/odom'),
                    ('scan', '/pf/scan'),
                    ('rgbd_image', 'rgbd_image')
                ]
            ),
        ])
    ])
