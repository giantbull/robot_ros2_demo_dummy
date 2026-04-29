from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import os

def generate_launch_description():
    package_name = "robot_arm_control"
    from ament_index_python.packages import get_package_share_directory
    pkg_path = get_package_share_directory(package_name)
    urdf_path = os.path.join(pkg_path, "urdf", "rrbot_arm.urdf")

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": open(urdf_path).read()}],
            output="screen"
        ),

        Node(
            package="joint_state_publisher",
            executable="joint_state_publisher",
            output="screen"
        ),

        # 直接运行，不依赖 libexec
        ExecuteProcess(
            cmd=["ros2", "run", "robot_arm_control", "trajectory_server"],
            output="screen"
        ),

        ExecuteProcess(
            cmd=["ros2", "run", "robot_arm_control", "robot_state"],
            output="screen"
        ),

        # 启动 RViz，不加载旧配置
        Node(
            package="rviz2",
            executable="rviz2",
            output="screen"
        ),
    ])
