
from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution, LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

    slam = LaunchConfiguration('slam')
    namespace = LaunchConfiguration('namespace')
    use_namespace = LaunchConfiguration('use_namespace')
    map_yaml_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')
    autostart = LaunchConfiguration('autostart')
    use_composition = LaunchConfiguration('use_composition')
    use_respawn = LaunchConfiguration('use_respawn')
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    urdf_file = LaunchConfiguration('urdf')

    declare_namespace_cmd = DeclareLaunchArgument(
            'namespace',
            default_value='',
            description='Top-level namespace'
            )

    declare_use_namespace_cmd = DeclareLaunchArgument(
            'use_namespace',
            default_value='False',
            description='Whether to apply a namespace to the navigation stack'
            )

    declare_slam_cmd = DeclareLaunchArgument(
            'slam',
            default_value='False',
            description='Whether to run a SLAM'
            )

    declare_map_yaml_cmd = DeclareLaunchArgument(
            'map',
            description='Full path to map file to load'
            )

    declare_use_sim_time_cmd = DeclareLaunchArgument(
            'use_sim_time',
            default_value='False',
            description='Use simulation clock if true'
            )

    declare_params_file_cmd = DeclareLaunchArgument(
            'params_file',
            description='Full path to the ROS2 parameters file to use for all launched nodes'
            )

    declare_autostart_cmd = DeclareLaunchArgument(
            'autostart',
            default_value='True',
            description='Automatically start up the nav2 stack'
            )

    declare_use_composition_cmd = DeclareLaunchArgument(
            'use_composition',
            default_value='False',
            description='Whether to use composed bringup'
            )

    declare_use_respawn_cmd = DeclareLaunchArgument(
            'use_respawn',
            default_value='False',
            description='Whether to respawn if a node crashes. Applied when composition is disabled'
            )

    declare_rviz_config_file_cmd = DeclareLaunchArgument(
            'rviz_config_file',
            description='Full path to the Rviz config file'
            )

    nav2_bringup_dir = FindPackageShare('nav2_bringup')

    start_robot_state_publisher_cmd = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=namespace,
            parameters=[{
                'use_sim_time': use_sim_time,
                'robot_description': Command(['xacro ', urdf_file]),
                }],
            remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')]
            )

    rviz_cmd = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([nav2_bringup_dir, 'launch', 'rviz_launch.py'])
                ),
            launch_arguments={
                'namespace': namespace,
                'use_namespace': use_namespace,
                'rviz_config': rviz_config_file,
                'use_sim_time': use_sim_time
                }.items()
            )

    bringup_cmd = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([nav2_bringup_dir, 'launch', 'bringup_launch.py'])
                ),
            launch_arguments={
                'namespace': namespace,
                'use_namespace': use_namespace,
                'slam': slam,
                'map': map_yaml_file,
                'use_sim_time': use_sim_time,
                'params_file': params_file,
                'autostart': autostart,
                'use_composition': use_composition,
                'use_respawn': use_respawn
                }.items()
            )

    return LaunchDescription([
        declare_namespace_cmd,
        declare_use_namespace_cmd,
        declare_slam_cmd,
        declare_map_yaml_cmd,
        declare_use_sim_time_cmd,
        declare_params_file_cmd,
        declare_autostart_cmd,
        declare_use_composition_cmd,
        declare_use_respawn_cmd,
        declare_rviz_config_file_cmd,

        start_robot_state_publisher_cmd,
        rviz_cmd,
        bringup_cmd,
        ])

