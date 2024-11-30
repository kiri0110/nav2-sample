from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
import os
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    namespace = LaunchConfiguration('namespace')
    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='false', description='Use simulation (Gazebo) clock if true')
    namespace_arg = DeclareLaunchArgument('namespace', default_value='', description='Top-level namespace')
    return LaunchDescription([
        use_sim_time_arg,
        namespace_arg,
        Node(
            package='nav2_map_server',
            executable='map_server',
            output='screen',
            name='map_server_amcl',
            parameters=[{
                'yaml_filename': PathJoinSubstitution([FindPackageShare('navigation'), 'map', 'pre_robocon_2024_field.yaml']),
                'topic_name': 'map_amcl',
                'use_sim_time': use_sim_time
            }],
            namespace=namespace
        ),
    ])
