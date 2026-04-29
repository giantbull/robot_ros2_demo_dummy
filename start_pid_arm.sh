#!/bin/bash
#!/bin/bash
source /opt/ros/jazzy/setup.bash

echo "======== 启动 PID 机械臂 ========"
echo "1. 启动 PID 控制器"
echo "2. 启动轨迹发生器"
echo "3. 启动机器人模型"
echo "4. 启动 RViz"
echo "================================"

cd ~/robot_ws

python3 src/robot_arm_control/pid_arm_controller.py &
sleep 1
python3 src/robot_arm_control/pid_target_publisher.py &
sleep 1
ros2 run robot_state_publisher robot_state_publisher src/robot_arm_control/urdf/rrbot_arm.urdf &
sleep 1
rviz2 &
