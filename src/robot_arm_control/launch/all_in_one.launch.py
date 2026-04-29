from launch import LaunchDescription
from launch.actions import ExecuteProcess
import os

def generate_launch_description():
    pkg_dir = os.path.expanduser("~/robot_ws/src/robot_arm_control")
    rviz_cfg = os.path.join(pkg_dir, "config", "myviz.rviz")

    return LaunchDescription([
        # 机器人模型
        ExecuteProcess(
            cmd=[
                "ros2", "run", "robot_state_publisher", "robot_state_publisher",
                os.path.join(pkg_dir, "urdf", "rrbot_arm.urdf")
            ],
            output="screen"
        ),
        # 关节状态
        ExecuteProcess(
            cmd=["ros2", "run", "joint_state_publisher"],
            output="screen"
        ),
        # PID控制器
        ExecuteProcess(
            cmd=["python3", os.path.join(pkg_dir, "pid_arm_controller.py")],
            output="screen"
        ),
        # 轨迹发布
        ExecuteProcess(
            cmd=["python3", os.path.join(pkg_dir, "pid_target_publisher.py")],
            output="screen"
        ),
        # GUI滑块
        ExecuteProcess(
            cmd=["python3", os.path.join(pkg_dir, "gui_slider.py")],
            output="screen"
        ),
        # 加载纯净配置的RViz
        ExecuteProcess(
            cmd=["rviz2", "-d", rviz_cfg],
            output="screen"
        ),
    ])
