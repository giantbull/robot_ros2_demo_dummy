#!/usr/bin/env python3
import rclpy
import math
import time
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

# PID 控制器类
class PID:
    def __init__(self, kp, ki, kd, max_out=1.5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_out = max_out
        self.err_last = 0
        self.err_sum = 0

    def compute(self, target, current):
        err = target - current
        self.err_sum += err
        out = self.kp * err + self.ki * self.err_sum + self.kd * (err - self.err_last)
        self.err_last = err

        if out > self.max_out:
            out = self.max_out
        if out < -self.max_out:
            out = -self.max_out
        return out

# ROS2 PID 机械臂控制器
class PIDArmNode(Node):
    def __init__(self):
        super().__init__("pid_arm_controller")

        # 两个关节 PID（工业级参数）
        self.pid1 = PID(2.8, 0.08, 0.6)
        self.pid2 = PID(2.8, 0.08, 0.6)

        # 目标角度
        self.target_j1 = 0.0
        self.target_j2 = 0.0

        # 当前角度
        self.curr_j1 = 0.0
        self.curr_j2 = 0.0

        # 发布关节状态
        self.joint_pub = self.create_publisher(JointState, "/joint_states", 10)

        # 订阅目标角度（可从GUI或轨迹下发）
        self.create_subscription(
            Float64MultiArray, "/arm_target_pos", self.target_callback, 10
        )

        # 50Hz 控制周期
        self.timer = self.create_timer(0.02, self.pid_control_loop)
        self.get_logger().info("✅ ROS2 PID 机械臂控制器已启动！")

    def target_callback(self, msg):
        if len(msg.data) >= 2:
            self.target_j1 = msg.data[0]
            self.target_j2 = msg.data[1]

    # PID 主循环
    def pid_control_loop(self):
        # 计算 PID 输出
        out1 = self.pid1.compute(self.target_j1, self.curr_j1)
        out2 = self.pid2.compute(self.target_j2, self.curr_j2)

        # 积分限位（防抖动）
        self.curr_j1 += out1 * 0.02
        self.curr_j2 += out2 * 0.02

        # 发布到RViz
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ["single_rrbot_joint1", "single_rrbot_joint2"]
        msg.position = [self.curr_j1, self.curr_j2]
        self.joint_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = PIDArmNode()
    rclpy.spin(node)

if __name__ == "__main__":
    main()
