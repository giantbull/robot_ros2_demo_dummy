from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_name = "robot_arm_control"
    pkg_dir = get_package_share_directory(pkg_name)
    urdf_path = os.path.join(pkg_dir, "urdf", "rrbot_arm.urdf")

    return LaunchDescription([
        # 1. 机器人模型发布
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': open(urdf_path).read()}],
            output='screen'
        ),

        # 2. 关节状态发布
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            output='screen'
        ),

        # 3. PID 闭环控制器
        ExecuteProcess(
            cmd=["python3", os.path.join(pkg_dir, "../pid_arm_controller.py")],
            output="screen"
        ),

        # 4. 轨迹目标发生器(圆形连续运动)
        ExecuteProcess(
            cmd=["python3", os.path.join(pkg_dir, "../pid_target_publisher.py")],
            output="screen"
        ),

        # 5. RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        ),
    ])
