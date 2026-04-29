#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import tkinter as tk
from tkinter import ttk

class ArmSliderGUI(Node):
    def __init__(self):
        super().__init__("arm_slider_gui")
        self.pub = self.create_publisher(JointState, "/joint_states", 10)
        self.j1 = 0.0
        self.j2 = 0.0

        # GUI 窗口
        self.root = tk.Tk()
        self.root.title("ROS2 机械臂滑块控制器")
        self.root.geometry("500x280")

        # 关节1 滑块
        ttk.Label(self.root, text="关节 1", font=("Arial", 14)).pack(pady=5)
        self.s1 = ttk.Scale(
            self.root, from_=-1.5, to=1.5, length=400, command=self.update_j1
        )
        self.s1.set(0.0)
        self.s1.pack()

        # 关节2 滑块
        ttk.Label(self.root, text="关节 2", font=("Arial", 14)).pack(pady=5)
        self.s2 = ttk.Scale(
            self.root, from_=-1.5, to=1.5, length=400, command=self.update_j2
        )
        self.s2.set(0.0)
        self.s2.pack()

        # 回零按钮
        ttk.Button(
            self.root, text="一键回零", command=self.go_home
        ).pack(pady=10)

        # 定时发布
        self.timer = self.create_timer(0.05, self.publish_joint)

    def update_j1(self, value):
        self.j1 = float(value)

    def update_j2(self, value):
        self.j2 = float(value)

    def go_home(self):
        self.j1 = 0.0
        self.j2 = 0.0
        self.s1.set(0.0)
        self.s2.set(0.0)

    def publish_joint(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ["single_rrbot_joint1", "single_rrbot_joint2"]
        msg.position = [self.j1, self.j2]
        self.pub.publish(msg)

    def run(self):
        while rclpy.ok():
            self.root.update()
            rclpy.spin_once(self, timeout_sec=0.01)
        self.root.destroy()

def main():
    rclpy.init()
    gui = ArmSliderGUI()
    gui.run()

if __name__ == "__main__":
    main()
