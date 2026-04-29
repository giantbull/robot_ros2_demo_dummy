#!/usr/bin/env python3
import rclpy
import time
from rclpy.action import ActionServer
from rclpy.node import Node
from sensor_msgs.msg import JointState
from control_msgs.action import FollowJointTrajectory
from std_srvs.srv import Trigger

class TrajectoryServer(Node):
    def __init__(self):
        super().__init__("trajectory_server")

        # 限位
        self.JOINT_MIN = -1.5
        self.JOINT_MAX = 1.5
        self.SPEED = 0.8       # 运动速度（越小越快）
        self.emergency_stop = False

        # 发布关节状态
        self.joint_pub = self.create_publisher(JointState, "/joint_states", 10)

        # 服务：回零 / 急停
        self.create_service(Trigger, "/robot/home", self.callback_home)
        self.create_service(Trigger, "/robot/emergency_stop", self.callback_emergency)

        # 动作服务
        self.action_server = ActionServer(
            self, FollowJointTrajectory, "/follow_joint_trajectory", self.execute_callback
        )

        self.get_logger().info("✅ 复杂动作控制器已启动！")

    # 角度限制
    def limit(self, angle):
        return max(self.JOINT_MIN, min(angle, self.JOINT_MAX))

    # 发布角度
    def pub(self, j1, j2):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ["single_rrbot_joint1", "single_rrbot_joint2"]
        msg.position = [self.limit(j1), self.limit(j2)]
        self.joint_pub.publish(msg)

    # 回零
    def callback_home(self, req, res):
        self.get_logger().info("🏠 回原点")
        self.pub(0.0, 0.0)
        res.success = True
        return res

    # 急停
    def callback_emergency(self, req, res):
        self.emergency_stop = True
        self.get_logger().error("🛑 紧急停止")
        self.pub(0.0, 0.0)
        res.success = True
        return res

    # ==========================
    # ✅ 这里写【复杂动作序列】
    # ==========================
    def execute_callback(self, goal_handle):
        self.get_logger().info("🚀 开始执行复杂动作！")
        self.emergency_stop = False

        # ==============================================
        # 🔥 复杂动作：一串连续坐标 (关节1, 关节2)
        # 你可以随便加、随便改、随便删！
        # ==============================================
        trajectory_points = [
            (0.0, 0.0),     # 起点
            (0.4, 0.0),     # 右摆
            (0.4, 0.5),     # 右上
            (-0.4, 0.5),    # 左上
            (-0.4, -0.5),   # 左下
            (0.4, -0.5),    # 右下
            (0.4, 0.0),     # 回右
            (0.0, 0.0),     # 回中
            (0.0, 0.0),     # 停止
        ]

        # 一步步走
        for i, (j1, j2) in enumerate(trajectory_points):
            if self.emergency_stop or goal_handle.is_cancel_requested:
                self.pub(0,0)
                goal_handle.canceled()
                self.get_logger().warn("❌ 动作已取消")
                return FollowJointTrajectory.Result()

            self.pub(j1, j2)
            self.get_logger().info(f"运动中 →  {i+1}/{len(trajectory_points)}  (j1={j1:.2f}, j2={j2:.2f})")
            time.sleep(self.SPEED)

        self.get_logger().info("✅ 复杂动作执行完成！")
        goal_handle.succeed()
        return FollowJointTrajectory.Result()

def main(args=None):
    rclpy.init(args=args)
    server = TrajectoryServer()
    rclpy.spin(server)

if __name__ == "__main__":
    main()
