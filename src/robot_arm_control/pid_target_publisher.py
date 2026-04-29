#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class TargetPublisher(Node):
    def __init__(self):
        super().__init__("pid_target_publisher")
        self.pub = self.create_publisher(Float64MultiArray, "/arm_target_pos", 10)
        self.timer = self.create_timer(0.05, self.publish_circle)
        self.t = 0.0

    # 圆形轨迹
    def publish_circle(self):
        r = 0.6
        j1 = r * math.sin(self.t)
        j2 = r * math.cos(self.t)
        self.t += 0.04

        msg = Float64MultiArray()
        msg.data = [j1, j2]
        self.pub.publish(msg)

    # 正方形轨迹
    def publish_square(self):
        step = int(self.t * 5) % 4
        if step ==0: p=(0.6,0.6)
        elif step==1:p=(0.6,-0.6)
        elif step==2:p=(-0.6,-0.6)
        else:p=(-0.6,0.6)
        self.t+=0.02
        msg = Float64MultiArray()
        msg.data=p
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TargetPublisher()
    rclpy.spin(node)

if __name__ == "__main__":
    main()
